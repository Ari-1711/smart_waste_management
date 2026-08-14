<div align="center">

[🇮🇩 Baca dalam Bahasa Indonesia](README.md) | [🇬🇧 Read in English](README.en.md)

# ♻️ Smart Waste Management: Klasifikasi Berbasis AI

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org)
[![TensorFlow](https://img.shields.io/badge/TensorFlow-2.x-FF6F00.svg?style=for-the-badge&logo=tensorflow&logoColor=white)](https://www.tensorflow.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B.svg?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io)
[![Keras](https://img.shields.io/badge/Keras-D00000.svg?style=for-the-badge&logo=keras&logoColor=white)](https://keras.io)
[![Kaggle Dataset](https://img.shields.io/badge/Kaggle-Dataset-20BEFF.svg?style=for-the-badge&logo=kaggle&logoColor=white)](https://www.kaggle.com/datasets/techsash/waste-classification-data)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)

**Aplikasi Web Deep Learning yang Siap untuk Edge AI dalam Pemilahan Otomatis Sampah Organik vs. Anorganik.**

[**🚀 Jalankan Live Demo**](https://smartwastemanagement-bvasn5fbt3szlfmmnvvd6f.streamlit.app/)

</div>

---

> [!NOTE]  
> **Pemberitahuan Live Demo (Streamlit Cloud)**  
> Jika Anda mengakses live demo untuk pertama kalinya atau setelah tidak aktif beberapa saat, aplikasi mungkin membutuhkan waktu untuk "bangun" (wake up) dari mode sleep *cold-start*. **Anda mungkin perlu memuat ulang (refresh/reload) halaman satu kali jika terasa terhenti atau *time out* di awal.** Ini adalah perilaku standar dari siklus hidup container gratis di Streamlit Community Cloud, bukan sebuah error *runtime* atau *bug* aplikasi.

---

## 🚀 Ringkasan Eksekutif & Elevator Pitch

Proyek ini menghadirkan alur kerja Machine Learning yang menyeluruh dengan memanfaatkan Transfer Learning (MobileNetV2) untuk mengklasifikasikan limbah menjadi kategori **Organik** dan **Anorganik (Recyclable)**. Dibangun dengan fokus pada penerapan di dunia nyata, model ini mencapai akurasi level produksi dengan tetap mempertahankan jejak komputasi yang ringan agar cocok untuk integrasi *Edge AI* di masa depan. Solusi ini dibungkus dalam aplikasi web interaktif Streamlit, yang mendemonstrasikan inferensi real-time mulus dan pengalaman pengguna yang prima.

### 📊 Metrik Kinerja Utama

| Metrik | Nilai | Dampak |
| :--- | :--- | :--- |
| **Akurasi Validasi** | `93.88%` | Keandalan tinggi untuk sistem pemilahan otomatis. |
| **Validation Loss** | `0.1641` | Generalisasi model yang kuat dengan risiko overfitting minimal. |
| **Rata-rata F1-Score** | `94.00%` | Keseimbangan presisi dan recall pada kedua kelas limbah. |
| **Tingkat Keyakinan Inferensi** | `91% - 99.69%` | Prediksi yang sangat tegas pada data tak terlihat di dunia nyata. |
| **Volume Data** | `22,564 Gambar` | Dilatih pada dataset Kaggle yang tangguh dan bervariasi. |

---

## 🗄️ Spesifikasi & Kutipan Dataset

Proyek ini menggunakan **[Waste Classification Data](https://www.kaggle.com/datasets/techsash/waste-classification-data)** terkemuka dari Kaggle.

- **Total Gambar:** 22.564 citra resolusi tinggi.
- **Kelas:** Klasifikasi Biner (Organik `O` vs. Anorganik/Recyclable `R`).
- **Strategi Pemisahan Data:** 
  - **Set Pelatihan (80%):** Digunakan untuk mengoptimalkan parameter model.
  - **Set Validasi (20%):** Disisihkan untuk evaluasi tak bias dan penyesuaian hyperparameter selama pelatihan.

---

## 🧠 Arsitektur & Alur Kerja Menyeluruh

Alur kerja arsitektur proyek ini dirancang dengan tahapan sistematis sebagai berikut:
**Preprocessing Citra** ➔ **Transfer Learning MobileNetV2** (Base layers frozen + Custom Top: GAP2D & Sigmoid) ➔ **Pelatihan Eksperimental Max 25 Epoch** (Komparasi Patience 3, 5, 7, 10) ➔ **Seleksi Model Terbaik** (Patience 10) ➔ **Pengujian Citra Baru** ➔ **Integrasi & Deployment Streamlit**.

![Architecture & Workflow Diagram](docs/assets/flow.png)

---

## 🔬 Benchmark Eksperimen & Pertimbangan Teknik (*Engineering Trade-Offs*)

Seluruh skenario pelatihan dieksekusi dengan konfigurasi hiperparameter dasar: **Batas maksimal 25 epoch**, pengoptimal **Adam**, dan fungsi objektif **Binary Crossentropy**. Untuk mengoptimalkan efisiensi dan mencegah overfitting, kami melakukan analisis komparatif ketat menggunakan *callback* **Early Stopping** dengan memantau `val_accuracy` serta mengaktifkan parameter `restore_best_weights=True`.

### Analisis *Patience* pada Early Stopping

| Patience | Epoch Terhenti | Best Epoch | Train Acc | Val Accuracy | Train Loss | Val Loss | Kesimpulan |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| `3` | 18 | 15 | 93.36% | 93.84% | 0.1776 | 0.1652 | Efisien secara komputasi (mengunci bobot terbaik di epoch 15). |
| `5` | 16 | 11 | 93.36% | 93.66% | 0.1773 | 0.1716 | Berhenti prematur pada optimum lokal. |
| `7` | 22 | 15 | 93.36% | 93.84% | 0.1776 | 0.1652 | Stabil, memulihkan bobot yang identik dengan Patience 3. |
| **`10`** | **25** | **25** | **93.73%** | **93.88%** | **0.1677** | **0.1641** | **Performa terbaik mutlak (loss validasi terendah).** |

**Analisis *First-Principles* Perangkat Lunak:**
Dalam skenario *Edge AI*, komputasi pelatihan bukan masalah besar dibandingkan latensi inferensi. Namun, selama fase pelatihan, mengatur nilai *patience* ke 10 terbukti menghasilkan performa paling optimal (loss terendah). Terdapat *trade-off* komputasi yang jelas: margin peningkatan akurasi dari Patience 7 (93.84% pada epoch 22 dengan best epoch 15) ke Patience 10 (93.88% pada epoch 25) hanya sebesar 0.04%. Sedikit peningkatan akurasi tersebut memerlukan eksekusi penuh hingga batas 25 epoch untuk meminimalkan *validation loss* ke 0.1641, sedangkan konfigurasi toleransi lebih ketat (seperti Patience 3 dan 7) sudah berhasil mengunci akurasi 93.84% lebih awal. *Patience* 10 memungkinkan pengoptimal (Adam) untuk menavigasi titik minimum lokal dengan lebih efektif, menghasilkan performa terbaik secara mutlak.

---

## 🎯 Evaluasi Model

Model ini mendemonstrasikan keseimbangan luar biasa, secara efektif mencegah bias yang sering terjadi terhadap kelas mayoritas.

### Laporan Klasifikasi (Validation Set)

| Kelas | Precision | Recall | F1-Score |
| :--- | :---: | :---: | :---: |
| **Organik (O)** | 0.96 | 0.93 | **0.94** |
| **Anorganik (R)** | 0.92 | 0.95 | **0.93** |
| *Macro Avg / Overall* | *0.94* | *0.94* | **0.94** |

---

## 💻 Fitur Aplikasi Web & Panduan Instalasi Lokal

Aplikasi Streamlit dirancang dengan interaksi intuitif serta *error handling* yang tangguh.
- **Fitur:** Unggah File (JPG/PNG), Input Kamera Langsung, Inferensi *Real-time*, Indikator Keyakinan Visual, Memuat Model dari Cache (`@st.cache_resource`) untuk eksekusi yang cepat.

### Petunjuk Persiapan Lokal

1. **Clone Repositori:**
   ```bash
   git clone https://github.com/Ari-1711/smart-waste-management.git
   cd smart-waste-management
   ```

2. **Buat Virtual Environment (Sangat Disarankan):**
   ```bash
   python -m venv venv
   # Di Windows:
   venv\Scripts\activate
   # Di macOS/Linux:
   source venv/bin/activate
   ```

3. **Instal Dependensi:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Jalankan Aplikasi Streamlit:**
   ```bash
   streamlit run app.py
   ```

---

## 📂 Struktur Direktori Proyek

```text
smart_waste_management/
│
├── .agents/                   # Konfigurasi skill dan agent kustom
├── .codex/                    # Konfigurasi hooks untuk agent
├── data/                      # Folder penyimpan dataset dan gambar hasil pemrosesan
├── docs/                      
│   └── assets/                # Aset dokumentasi (contoh: diagram alur)
├── models/
│   └── mobilenetv2_waste.keras # Bobot model Keras yang telah dilatih (frozen)
├── notebooks/
│   └── swm_model.ipynb        # Notebook berisi arsitektur model, pelatihan, dan evaluasi
├── src/
│   └── predictor.py           # Logika inferensi dan fungsi prapemrosesan gambar
├── app.py                     # Titik masuk utama aplikasi web Streamlit
├── requirements.txt           # File dependensi proyek
├── .gitignore                 # Aturan ignore Git
├── README.en.md               # Dokumentasi utama proyek (Versi Inggris)
└── README.md                  # Dokumentasi utama proyek (Versi Indonesia - Anda di sini)
```

---

## 👥 Penulis, Peran & Rincian Kontribusi

Proyek ini berawal dari riset akademis di **Universitas Mercu Buana** dan dikembangkan lebih lanjut menjadi aplikasi web siap pakai.

- **Ari Hermawan** — *Lead ML Engineer & Streamlit Developer*
  - Merancang arsitektur model, prapemrosesan (*preprocessing*), dan pipeline augmentasi.
  - Merancang kerangka percobaan *Early Stopping* dan melatih model.
  - Mengembangkan, mengoptimalkan, dan melakukan deployment aplikasi web interaktif menggunakan Streamlit.
- **Royhan Achmad** — *Academic Researcher*
  - Melakukan tinjauan pustaka secara komprehensif (literature reviews) dan menyusun landasan teoretis.
  - Mengelola pemformatan referensi dan menyusun dokumentasi laporan akademik.
- **Adistya Firdaus** — *Academic Researcher*
  - Memimpin validasi dataset dan pemeriksaan integritas data.
  - Menjalankan pelaporan komparatif dan merampungkan dokumentasi teknis akhir.
- **Essy Malay Sari Sakti, S.Kom., M.M.S.I.** — *Advisor / Dosen Pembimbing*
  - Memberikan panduan strategis, pengawasan akademik, dan validasi seluruh proyek.

---

## 🛠️ *Tech Stack* & Rencana Pengembangan Masa Depan

**Teknologi Inti:**
- **Bahasa:** Python 3.10+
- **Deep Learning:** TensorFlow 2.x, Keras, MobileNetV2
- **Pemrosesan Data:** NumPy, Pillow (PIL)
- **Frontend / Deployment:** Streamlit, Streamlit Community Cloud

**Rencana Masa Depan (*Roadmap*):**
1. **Edge Deployment:** Mengoptimalkan model memanfaatkan TensorFlow Lite untuk di-deploy pada perangkat *Edge IoT* yang terbatas sumber daya (misalnya: NVIDIA Jetson Nano, Raspberry Pi) dan diintegrasikan langsung dengan tempat sampah fisik.
2. **Ekspansi Multi-Kelas:** Memperluas dataset dan melatih ulang model untuk mengklasifikasikan sub-kategori limbah (contoh: Kaca, Plastik, Kertas, Logam, E-Waste) guna mendukung proses daur ulang yang lebih terperinci.
3. **Continuous Learning:** Mengimplementasikan lingkaran umpan balik (feedback loop) dalam web app untuk mengumpulkan gambar yang salah diklasifikasikan demi pelatihan ulang model di masa mendatang.
