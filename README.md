# symptom-checker
Symptom-based disease prediction and nearest hospital finder using Tkinter GUI. Utilizes DFS backtracking for diagnosis and Euclidean distance for hospital navigation.
Sistem Prediksi Penyakit dan Pencarian Rumah Sakit Terdekat dengan GUI
Aplikasi ini merupakan sistem berbasis Python yang menggabungkan prediksi penyakit menggunakan algoritma DFS Backtracking dan pencarian rumah sakit terdekat berdasarkan lokasi kecamatan, lengkap dengan antarmuka grafis (GUI) berbasis Tkinter.

🚀 Fitur Utama
Prediksi Penyakit dengan DFS Backtracking

Menggunakan dataset bersih2.csv yang berisi daftar penyakit dan gejalanya.

Pengguna dapat memilih minimal 3 gejala dari listbox GUI.

Sistem memprediksi penyakit yang paling mungkin berdasarkan kecocokan gejala melalui algoritma pencarian DFS dan pencocokan minimum 3 gejala.

Pencarian Rumah Sakit Terdekat

Berdasarkan pilihan lokasi kecamatan dari dropdown.

Menggunakan koordinat fiktif (grid sederhana) untuk menghitung jarak Euclidean ke setiap rumah sakit.

Menampilkan hasil berupa nama rumah sakit terdekat dan estimasi jarak.

Menyediakan fitur visualisasi graph menggunakan networkx dan matplotlib.

Tersedia opsi untuk membuka rute langsung ke Google Maps.

GUI Interaktif

Antarmuka pengguna dibuat menggunakan Tkinter.

Desain halaman meliputi tampilan awal, input gejala, hasil prediksi, pencarian rumah sakit, dan tampilan graf.

Dilengkapi dengan tombol navigasi seperti "Beranda", "Kembali", dan "Hubungi Dokter".

🧠 Algoritma
DFS Backtracking

Digunakan untuk mengeksplorasi setiap kemungkinan pencocokan antara gejala pengguna dengan gejala pada setiap penyakit dalam dataset.

Hanya penyakit dengan minimal 3 gejala yang cocok akan ditampilkan sebagai hasil prediksi.

Graph-Based Nearest Hospital Finder

Struktur graf digunakan untuk memodelkan lokasi rumah sakit.

Algoritma pencarian jarak terpendek berbasis perhitungan manual jarak Euclidean.
