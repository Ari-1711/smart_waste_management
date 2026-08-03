# ♻️ Smart Waste Management System

[Live Demo: 🚀 Akses Dashboard Interaktif Streamlit](https://smartwastemanagement-bvasn5fbt3szlfmmnvvd6f.streamlit.app/)

Sistem klasifikasi jenis sampah (Organik vs Anorganik/Recyclable) berbasis Deep Learning Transfer Learning MobileNetV2 yang terintegrasi dengan antarmuka web interaktif Streamlit untuk klasifikasi instan beserta saran pengolahan limbah.

---

## 📌 Problem & Business Context

Pengelolaan limbah cair dan padat di lingkungan perkotaan maupun industri sering terkendala oleh kesalahan pemilahan sampah di tingkat awal. Pemilahan manual memakan waktu dan rentan *human error*. 

Proyek ini bertujuan menyediakan solusi pengenalan jenis sampah berbasis Computer Vision yang ringan, cepat, dan presisi tinggi agar dapat diterapkan secara langsung pada antarmuka web maupun perangkat IoT/kamera pintar.

---

## 🔑 Key Features

* **Transfer Learning MobileNetV2:** Menggunakan arsitektur jaringan saraf terkonvolusi (*CNN*) teroptimasi yang ringan untuk klasifikasi citra biner cepat.
* **Cached Model Inference:** Menerapkan strategi caching resource Streamlit (`@st.cache_resource`) untuk pemuatan model `.keras` yang efisien tanpa membebani RAM server.
* **Real-Time Confidence Score:** Menampilkan tingkat keyakinan prediksi AI (%) dalam bentuk visualisasi *progress bar*.
* **Dynamic Categorization & Recommendations:** Memberikan label klasifikasi otomatis beserta panduan pengelolaan spesifik (daur ulang untuk Anorganik, pengomposan untuk Organik).
* **Interactive Web Dashboard:** Aplikasi antarmuka berbasis Streamlit dengan fitur unggah gambar (`.jpg`, `.jpeg`, `.png`) dan tata letak responsif.

---

## 🛠️ Repository Structure

```text
smart_waste_management/
├── data/                  # Petunjuk/rujukan dataset gambar
├── models/
│   └── mobilenetv2_waste.keras   # Model Deep Learning terlatih (.keras)
├── notebooks/
│   └── swm_model.ipynb           # Notebook pelatihan & evaluasi MobileNetV2
├── src/
│   └── predictor.py              # Logika pemuatan model & pemrosesan inferensi
├── app.py                        # Streamlit Web Application Main Entry
├── requirements.txt              # Daftar dependensi & pustaka Python
└── README.md                     # Dokumentasi proyek

```

---

## 🚀 How to Run Locally

1. **Clone repositori ini:**
```bash
git clone [https://github.com/Ari-1711/smart_waste_management.git](https://github.com/Ari-1711/smart_waste_management.git)
cd smart_waste_management

```


2. **Buat dan aktifkan Virtual Environment (Direkomendasikan):**
* **Windows:**
```cmd
python -m venv venv
venv\Scripts\activate

```


* **Mac/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate

```




3. **Instal dependensi:**
```bash
pip install --upgrade pip
pip install -r requirements.txt

```


*Jika terjadi kendala saat menginstal via `requirements.txt`, instal library utama secara langsung:*
```bash
pip install streamlit tensorflow-cpu pillow numpy

```


4. **Jalankan aplikasi Streamlit:**
```bash
streamlit run app.py

```


*(Atau gunakan `python -m streamlit run app.py` jika perintah `streamlit` tidak terdeteksi di terminal).*

---

## 👤 Penulis

**Ari Hermawan**

* GitHub: [@Ari-1711](https://www.google.com/search?q=https://github.com/Ari-1711)
* Live Web App: [Smart Waste Management App](https://smartwastemanagement-bvasn5fbt3szlfmmnvvd6f.streamlit.app/)

```

---

### Perintah Git untuk Update README ke GitHub

Jalankan perintah ini di terminal untuk langsung memperbarui repositorimu:

```cmd
git add README.md
git commit -m "docs: restructure README matching portfolio standard"
git push origin main

```
