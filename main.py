import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from PIL import Image, ImageTk
import webbrowser
from DFS import prediksi_penyakit_dengan_dfs_backtracking
from RS import setup_hospitals
import pandas as pd
import math
import networkx as nx
import matplotlib.pyplot as plt

import matplotlib
matplotlib.use('TkAgg')  # Atau backend lain yang Anda gunakan


kecamatan_coords = {
    "Gubeng": (10, 10),
    "Sukolilo": (11, 12),
    "Mulyorejo": (12, 9),
    "Rungkut": (9, 8),
    "Gunung Anyar": (11, 7),
    "Tenggilis Mejoyo": (9, 7),
    "Kenjeran": (12, 12),
    "Bulak": (12, 11),
    "Tandes": (3, 5),
    "Sambikerep": (2, 6),
    "Lakarsantri": (1, 7),
    "Benowo": (1, 9),
    "Pakal": (2, 10),
    "Asemrowo": (4, 8),
    "Wonokromo": (7, 6),
    "Wonocolo": (8, 4),
    "Karang Pilang": (6, 3),
    "Jambangan": (8, 5),
    "Wiyung": (5, 6),
    "Gayungan": (6, 4),
    "Dukuh Pakis": (5, 5),
    "Krembangan": (6, 10),
    "Pabean Cantian": (7, 9),
    "Semampir": (9, 11),
    "Genteng": (9, 8),
    "Tegalsari": (8, 9),
    "Simokerto": (10, 8),
    "Bubutan": (8, 10),
    "Tambaksari": (10, 10),

}

try:
    data = pd.read_csv(r"database\bersih2.csv")
except FileNotFoundError:
    print("Error: File bersih2.csv tidak ditemukan.")
    data = None

# Data Gejala
symptoms_list = []

# Fungsi Navigasi
def show_window(target_window):
    for window in windows:
        window.withdraw()
    target_window.deiconify()

# Fungsi Tambah dan Hapus Gejala
def add_symptom():
    selected_indices = listbox_symptoms.curselection()
    if not selected_indices:
        messagebox.showerror("Error", "Pilih gejala dari daftar!")
        return

    for index in selected_indices:
        symptom = listbox_symptoms.get(index)
        if symptom not in symptoms_list:
            symptoms_list.append(symptom)

    update_symptom_display()
    listbox_symptoms.selection_clear(0, tk.END)  # Hapus seleksi setelah ditambahkan

def remove_symptom():
    if symptoms_list:
        symptoms_list.pop()
        update_symptom_display()
    else:
        messagebox.showinfo("Info", "Tidak ada gejala untuk dihapus.")

def update_symptom_display():
    symptom_display.config(text=", ".join(symptoms_list))

# Fungsi Prediksi Penyakit
def predict_disease():
    if data is None:
        messagebox.showerror("Error", "Dataset tidak ditemukan. Pastikan file bersih2.csv ada.")
        return

    if len(symptoms_list) < 1:
        messagebox.showerror("Error", "Masukkan minimal 1 gejala!")
        return

    diseases = prediksi_penyakit_dengan_dfs_backtracking(set(symptoms_list), data)
    if diseases:
        disease_result.config(text=f"Penyakit yang Diprediksi: {', '.join(diseases)}")
    else:
        disease_result.config(text="Tidak ada prediksi penyakit.")
    show_window(window_3)

# Fungsi Cari Rumah Sakit

def find_hospital():
    global closest_hospital, user_position, graph, closest_distance

    # Ambil kecamatan dari dropdown
    kecamatan = kecamatan_var.get()
    if not kecamatan:
        messagebox.showerror("Error", "Pilih kecamatan dari daftar!")
        return

    # Pastikan kecamatan ada dalam data
    if kecamatan not in kecamatan_coords:
        messagebox.showerror("Error", "Kecamatan tidak ditemukan dalam data.")
        return

    # Siapkan koordinat pengguna dan data graf rumah sakit
    user_position = kecamatan_coords[kecamatan]
    graph = setup_hospitals()

    # Cari rumah sakit terdekat
    closest_hospital = None
    closest_distance = float("inf")
    for hospital, position in graph.hospitals.items():
        distance = math.sqrt((position[0] - user_position[0])**2 + (position[1] - user_position[1])**2)
        if distance < closest_distance:
            closest_distance = distance
            closest_hospital = hospital

    if not closest_hospital:
        messagebox.showinfo("Hasil", "Tidak ada rumah sakit yang ditemukan.")
        return

    # Tampilkan hasil di window_5
    result_label.config(
        text=f"Rumah Sakit Terdekat: {closest_hospital}\nJarak: {closest_distance:.2f} km"
    )
    show_window(window_5)

    # Visualisasikan rute
    visualize_graph(graph, user_position, closest_hospital, closest_distance)


def visualize_graph(graph, user_position, closest_hospital, closest_distance): 
    import networkx as nx
    import matplotlib.pyplot as plt

    # Membuat graph menggunakan NetworkX
    G = nx.Graph()
    for node1, neighbors in graph.edges.items():
        for node2, weight in neighbors:
            G.add_edge(node1, node2, weight=weight)

    # Posisi node (hospitals adalah dictionary dengan posisi setiap node)
    pos = graph.hospitals

    # Menentukan warna node
    node_colors = [
        'green' if node == closest_hospital else 'red'
        for node in G.nodes
    ]

    # Plot graf
    plt.figure(figsize=(12, 8))
    nx.draw(
        G, pos, with_labels=True, 
        node_color=node_colors, node_size=500, font_size=10, font_color='white'
    )

    # Menampilkan label bobot edge
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

    # Menampilkan posisi user dan rumah sakit terdekat
    plt.scatter(user_position[0], user_position[1], color='blue', s=100, label='User')
    plt.scatter(
        pos[closest_hospital][0], pos[closest_hospital][1], 
        color='green', s=150, label='Rumah Sakit Terdekat'
    )

    # Menambahkan legenda dan judul
    plt.legend()
    plt.title(f"Rumah Sakit Terdekat: {closest_hospital} (Jarak: {closest_distance:.2f})")
    plt.show()
    plt.savefig("output_graph.png")


    
def view_graph():
    if not closest_hospital or not user_position:
        messagebox.showerror("Error", "Data rumah sakit atau lokasi tidak tersedia.")
        return
    visualize_graph(graph, user_position, closest_hospital, closest_distance)
    
def open_google_maps():
    if not closest_hospital:
        messagebox.showerror("Error", "Rumah sakit belum ditemukan.")
        return

    # Mapping rumah sakit ke link Google Maps
    hospital_links = {
        "RSUD Bhakti Dharma Husada": "https://maps.app.goo.gl/z7TteVzaLgLhxzYf9",
        "National Hospital Surabaya": "https://maps.app.goo.gl/wd3ZmgmYL8xotcd28",
        "RSIA Cempaka Putih Permata": "https://maps.app.goo.gl/GkPHBdXZBiP749X79",
        "RSIA Kendangsari Surabaya": "https://maps.app.goo.gl/T3C5gEfR9xuAMq3fA",
        "Rumah Sakit Islam Surabaya Jemursari":"https://maps.app.goo.gl/xPEJfwR4tGJXBJwd7",
        "RS Bhayangkara Surabaya H.S Samsoeri Mertojoso": "https://maps.app.goo.gl/q8nTht96WVHg3hLN9",
        "RSU. Bhakti Rahayu Surabaya" : "https://maps.app.goo.gl/ftukedhsZ6HAgBGu8",
        "RSPAL dr RAMELAN SURABAYA" : "https://maps.app.goo.gl/kw412NdL1Swa5D8i7",
        "RS UBAYA":"https://maps.app.goo.gl/X6ytodSYBc1A3TfZ6",
        "Rumah Sakit Islam Surabaya": "https://maps.app.goo.gl/DfYkPN4ZRCSRuSf8A",
        "Mayapada Hospital Surabaya (MHSB)" : "https://maps.app.goo.gl/P6E5h8PtPptvN6Yr7",
        "Rumah Sakit Katolik St. Vincentius a Paulo" : "https://maps.app.goo.gl/ZRrBS1Nc6mB9MTzX9",
        "Rumah Sakit William Booth Surabaya" : "https://maps.app.goo.gl/ycrCWZ2biuxyNyGs7",
        "Rumah Sakit Darmo" : "https://maps.app.goo.gl/SNf8qy4zXXbURtYf8",
        "Rumah Sakit Umum Siloam Surabaya" : "https://maps.app.goo.gl/Tbgjk2PifYVkuQw77",
        "RSUD Dr. Soetomo":"https://maps.app.goo.gl/njr46LDfCqvKZAdq8",
        "RS Husada Utama":"https://maps.app.goo.gl/vTKCuT5cnApsruk66",
        "Rumah Sakit Adi Husada Undaan":'https://maps.app.goo.gl/8A4znQYBkZUoHgTF7',
        "Rumah Sakit PHC Surabaya":"https://maps.app.goo.gl/W99sEvFatebxWZa36",
        "Mitra Keluarga Surabaya":"https://maps.app.goo.gl/LRQeQTXGi9mBvnBF6",
    }

    link = hospital_links.get(closest_hospital, None)
    if link:
        webbrowser.open(link)
    else:
        messagebox.showerror("Error", "Link untuk rumah sakit ini tidak tersedia.")

bg_color = "#FFFFFF"
root = tk.Tk()
root.geometry("1366x768")
root.resizable(False, False)
root.attributes('-toolwindow', True)
root.config(bg=bg_color)
root.withdraw()

windows = []
# Window 0 - Halaman Awal
window_0 = tk.Toplevel(root)
window_0.geometry("1366x768")
window_0.config(bg=bg_color)
windows.append(window_0)

# Background Image untuk window 0
bg_0 = ImageTk.PhotoImage(Image.open(r"image\0.png"))
tk.Label(window_0, image=bg_0, bd=0).pack()

# Tombol "Mulai" di tengah
tk.Button(
    window_0, 
    text="Mulai", 
    bg=bg_color, 
    fg="black", 
    relief="flat", 
    bd=0, 
    font=("Montserrat", 15, "bold"), 
    command=lambda: show_window(window_1)  # Beralih ke window 1
).place(x=740, y=418)  # Koordinat tengah window

# Window 1 - Welcome Page
window_1 = tk.Toplevel(root)
window_1.geometry("1366x768")
window_1.config(bg=bg_color)
windows.append(window_1)

bg_1 = ImageTk.PhotoImage(Image.open(r"image\1.png"))
tk.Label(window_1, image=bg_1, bd=0).pack()  # bd=0 menghapus border pada label

tk.Button(window_1, text="Cek Penyakit", bg=bg_color, fg="black", relief="flat", bd=0, command=lambda: show_window(window_2)).place(x=525, y=398)
tk.Button(window_1, text="Cari RS Terdekat", bg=bg_color, fg="black", relief="flat", bd=0, command=lambda: show_window(window_4)).place(x=746, y=398)

# Window 2 - Input Gejala
window_2 = tk.Toplevel(root)
window_2.geometry("1366x768")
window_2.config(bg=bg_color)
windows.append(window_2)

bg_2 = ImageTk.PhotoImage(Image.open(r"image\2.png"))
tk.Label(window_2, image=bg_2, bd=0).pack()

# Listbox untuk memilih gejala
listbox_symptoms = tk.Listbox(window_2, selectmode=tk.MULTIPLE, width=38, height=15, bg=bg_color, fg="black", selectbackground="#B0D9FF")
listbox_symptoms.place(x=336, y=260)

# Scrollbar untuk Listbox
scrollbar = tk.Scrollbar(window_2, orient="vertical", command=listbox_symptoms.yview)
scrollbar.place(x=627, y=260, height=301)
listbox_symptoms.config(yscrollcommand=scrollbar.set)

# # Entry untuk menambah gejala (manual)
# entry_symptom = tk.Entry(window_2, bg=bg_color, fg="black", width=50, bd=0, highlightthickness=0)
# entry_symptom.place(x=200, y=370)

# Isi Listbox dengan gejala dari dataset
try:
    data = pd.read_csv(r"database\bersih2.csv")
    symptom_columns = [col for col in data.columns if "Symptom" in col]
    symptoms_from_data = set()
    for col in symptom_columns:
        symptoms_from_data.update(data[col].dropna().str.lower().str.strip().unique())
    for symptom in sorted(symptoms_from_data):
        listbox_symptoms.insert(tk.END, symptom)
except FileNotFoundError:
    print("File bersih2.csv tidak ditemukan.")

# Tombol untuk menambah gejala
tk.Button(window_2, text="Tambah Gejala", bg=bg_color, fg="black", relief="flat", bd=0, command=add_symptom).place(x=900, y=428)

# Tombol untuk menghapus gejala
tk.Button(window_2, text="Kurang Gejala", bg=bg_color, fg="black", relief="flat", bd=0, command=remove_symptom).place(x=750, y=428)

# Label untuk menampilkan gejala yang dipilih
symptom_display = tk.Label(window_2, text="", bg=bg_color, fg="black", width=40, height=4, relief="flat", bd=0)
symptom_display.place(x=700, y=290)

# Tombol untuk melihat hasil prediksi
tk.Button(window_2, text="Lihat Hasil", bg=bg_color, fg="black", relief="flat", bd=0, command=predict_disease).place(x=838, y=500)

# Tombol navigasi
tk.Button(window_2, text="Kembali", bg=bg_color, fg="black", relief="flat", bd=0, command=lambda: show_window(window_1)).place(x=257, y=45)
tk.Button(window_2, text="Beranda", bg=bg_color, fg="black", relief="flat", bd=0, command=lambda: show_window(window_1)).place(x=134, y=45)

# Window 3 - Hasil Prediksi
window_3 = tk.Toplevel(root)
window_3.geometry("1366x768")
window_3.config(bg=bg_color)
windows.append(window_3)

bg_3 = ImageTk.PhotoImage(Image.open(r"image\3.png"))
tk.Label(window_3, image=bg_3, bd=0).pack()

disease_result = tk.Label(window_3, text="", bg=bg_color, fg="black", wraplength=400, justify="left", relief="flat", bd=0)
disease_result.place(x=589, y=330)

tk.Button(window_3, text="Hubungi Dokter", bg=bg_color, fg="black", relief="flat", bd=0, command=lambda: webbrowser.open("https://wa.me/6281217234242")).place(x=540, y=460)
tk.Button(window_3, text="Cek RS Terdekat", bg=bg_color, fg="black", relief="flat", bd=0, command=lambda: show_window(window_4)).place(x=720, y=460)
tk.Button(window_3, text="Kembali", bg=bg_color, fg="black", relief="flat", bd=0, command=lambda: show_window(window_2)).place(x=257, y=45)
tk.Button(window_3, text="Beranda", bg=bg_color, fg="black", relief="flat", bd=0, command=lambda: show_window(window_1)).place(x=134, y=45)

# Window 4 - Cari RS Terdekat
window_4 = tk.Toplevel(root)
window_4.geometry("1366x768")
window_4.config(bg=bg_color)
windows.append(window_4)

# Background Image
bg_4 = ImageTk.PhotoImage(Image.open(r"image\4.png"))
tk.Label(window_4, image=bg_4, bd=0).pack()

# Dropdown untuk memilih kecamatan
kecamatan_var = tk.StringVar()
kecamatan_dropdown = ttk.Combobox(window_4, textvariable=kecamatan_var)
kecamatan_dropdown['values'] = list(kecamatan_coords.keys())
kecamatan_dropdown.place(x=582, y=365)  # Letakkan di posisi yang terlihat
kecamatan_dropdown.state(['readonly'])  # Dropdown hanya bisa memilih dari daftar

tk.Button(window_4, text="Cari Rumah Sakit Terdekat", bg=bg_color, fg="black", relief="flat", bd=0, command=find_hospital).place(x=595, y=420)
tk.Button(window_4, text="Kembali", bg=bg_color, fg="black", relief="flat", bd=0, command=lambda: show_window(window_3)).place(x=257, y=45)
tk.Button(window_4, text="Beranda", bg=bg_color, fg="black", relief="flat", bd=0, command=lambda: show_window(window_1)).place(x=134, y=45)

# Window 5 - Hasil RS Terdekat
window_5 = tk.Toplevel(root)
window_5.geometry("1366x768")
window_5.config(bg=bg_color)
windows.append(window_5)

bg_5 = ImageTk.PhotoImage(Image.open(r"image\5.png"))
tk.Label(window_5, image=bg_5, bd=0).pack()

# Label untuk menampilkan nama RS dan jarak
result_label = tk.Label(window_5, text="", bg="white", fg="black", font=("Arial", 12), highlightthickness=0)
result_label.place(relx=0.5, rely=0.5, anchor="center")

# Tombol untuk melihat graf
tk.Button(
    window_5,
    text="Lihat Graph",
    bg=bg_color,
    fg="black",
    relief="flat",
    font=("Arial", 11),
    command=view_graph
).place(x=560, y=450)

# Tombol untuk membuka Google Maps
tk.Button(
    window_5,
    text="Buka Google Maps",
    bg=bg_color,
    fg="black",
    relief="flat",
    font=("Arial", 11),
    command=open_google_maps
).place(x=690, y=450)

# Tombol kembali
tk.Button(window_5, text="Kembali", bg=bg_color, fg="black", relief="flat", bd=0, command=lambda: show_window(window_4)).place(x=257, y=45)
tk.Button(window_5, text="Beranda", bg=bg_color, fg="black", relief="flat", bd=0, command=lambda: show_window(window_1)).place(x=134, y=45)

# Mulai aplikasi

show_window(window_0)
root.mainloop()