import pandas as pd


file_path = r"database\bersih2.csv"
disease_symptoms_df = pd.read_csv(file_path)

def prediksi_penyakit_dengan_dfs_backtracking(set_gejala, data):
    if len(set_gejala) < 3:
        print("Peringatan: Masukkan minimal 3 gejala untuk memprediksi penyakit.")
        return []

    kolom_gejala = [kolom for kolom in data.columns if 'Symptom' in kolom]

    set_gejala = {gejala.lower().strip() for gejala in set_gejala}
    penyakit_yang_cocok = {}

    def dfs_backtrack(gejala_sekarang, penyakit, gejala_tercocok, index):
        if gejala_tercocok >= 3:
            penyakit_yang_cocok[penyakit] = gejala_tercocok
            return True
        if index >= len(gejala_sekarang):
            return False

        cocok = gejala_sekarang[index] in set_gejala

        if dfs_backtrack(gejala_sekarang, penyakit, gejala_tercocok + cocok, index + 1):
            return True

        return dfs_backtrack(gejala_sekarang, penyakit, gejala_tercocok, index + 1)

    for _, row in data.iterrows(): # O(n)
        penyakit = row['Disease'] 
        gejala_sekarang = [str(row[gejala]).lower().strip() for gejala in kolom_gejala if pd.notnull(row[gejala])]

        dfs_backtrack(gejala_sekarang, penyakit, 0, 0)

    if penyakit_yang_cocok:
        kecocokan_terbanyak = max(penyakit_yang_cocok.values())

        kecocokan_terbaik = [penyakit for penyakit, jumlah in penyakit_yang_cocok.items() if jumlah == kecocokan_terbanyak]
        return kecocokan_terbaik

    return []

gejala_sample = {"stomach_pain", "cough", "chest_pain"}

penyakit_prediksi = prediksi_penyakit_dengan_dfs_backtracking(gejala_sample, disease_symptoms_df)

