# 📂 Raw Dataset Information

Folder ini digunakan untuk menyimpan dataset mentah gambar sampah yang belum diolah.

---

## 📌 Sumber Dataset

* **Nama Dataset:** Waste Classification Data
* **Sumber:** Kaggle
* **Penyedia:** TechSash
* **URL Dataset:** [https://www.kaggle.com/datasets/techsash/waste-classification-data](https://www.kaggle.com/datasets/techsash/waste-classification-data)

---

## 📥 Cara Mengunduh & Menyiapkan Data

### Cara 1: Menggunakan Kagglehub (Otomatis / Direkomendasikan)
Dataset dapat diunduh otomatis melalui skrip Python saat training menggunakan `kagglehub`:

```python
import kagglehub

path = kagglehub.dataset_download("techsash/waste-classification-data")
print("Dataset diunduh ke:", path)

```

---

### Cara 2: Manual (Unduh dari Kaggle)

1. Buka link [Kaggle Waste Classification Data](https://www.kaggle.com/datasets/techsash/waste-classification-data).
2. Klik tombol **Download** (memerlukan akun Kaggle).
3. Ekstrak file zip yang diunduh ke dalam folder `data/raw/`.

---

## 📁 Struktur Folder Data yang Diharapkan

Setelah diunduh dan diekstrak, pastikan struktur folder di `data/raw/` terlihat seperti berikut:

```text
data/raw/
├── README.md
└── DATASET/
    ├── TEST/
    │   ├── O/   (Gambar sampah organik)
    │   └── R/   (Gambar sampah anorganik/recyclable)
    └── TRAIN/
        ├── O/   (Gambar sampah organik)
        └── R/   (Gambar sampah anorganik/recyclable)

```

---

> ⚠️ **Catatan Penting:**
> Gambar dalam folder ini diabaikan oleh Git (`.gitignore`) karena ukurannya yang besar. Hanya file `README.md` ini yang akan tersimpan di repositori GitHub.

```

---

### 💡 Jangan Lupa Update File `.gitignore` Utama

Supaya gambar-gambar dari Kaggle tersebut **tidak ikut terunggah** saat kamu `git push`, pastikan kamu menambahkan aturan berikut di file `.gitignore` yang ada di root folder repositori (`smart_waste_management/.gitignore`):

```text
# Abaikan semua isi folder data/raw
data/raw/*

# Pengecualian: Tetap simpan file README.md di data/raw/
!data/raw/README.md

# Abaikan juga folder data hasil download Kagglehub jika tersimpan lokal
/kaggle/

```