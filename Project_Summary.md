---
tags: [machine-learning, computer-vision, streamlit, project-summary]
date: 2026-08-14
---

# Smart Waste Management - Project Summary

Ini adalah rangkuman otomatis struktur dan isi proyek yang disimpan untuk memori (Obsidian Vault).

## Struktur Utama & Analisis File

### 1. `app.py`
- **Fungsi:** Titik masuk utama aplikasi web Streamlit.
- **Fitur Kunci:**
  - Desain UI/UX khusus menggunakan Custom CSS (Tema *Tinted Dark Eco*), layout grid responsif, font *Outfit*, animasi *fadeIn*, dan kartu status *(Organic/Inorganic)* yang atraktif.
  - Terdapat mekanisme auto-reload (JavaScript injection) yang memantau *VisibilityState* dan *Offline Events* untuk menanggulangi siklus *sleep* Streamlit Community Cloud.
  - Input dari **Upload File** maupun **Kamera Langsung** (mendukung format RGB Image).
  - Mekanisme caching resource model melalui dekorator `@st.cache_resource`.

### 2. `src/predictor.py`
- **Fungsi:** Mengatur logika inferensi dan pemuatan model.
- **Alur Kerja:**
  - `load_model_waste()`: Memuat model `.keras` (MobileNetV2) dengan parameter `compile=False` agar bebas dari error metric custom. Menggunakan try-except untuk error handling yang aman saat runtime Streamlit.
  - `predict_image()`: 
    - Melakukan preprocessing standar ImageNet (Resize 224x224, expand_dims untuk membuat batch tensor).
    - Melakukan pemanggilan `model.predict`.
    - Klasifikasi probabilitas (Threshold 0.5):
      - `Score > 0.5` => Anorganik (Recyclable, 'R')
      - `Score <= 0.5` => Organik (Organic, 'O')
    - Mengembalikan label manusiawi, skor kepercayaan, dan kode kategori.

### 3. `requirements.txt`
- **Dependensi Utama:**
  - `streamlit` (UI Web App)
  - `tensorflow-cpu` (Inference efisien tanpa GPU overhead di sisi server)
  - `pillow`, `numpy`, `pandas`, `scikit-learn` (Pemrosesan Data & Citra)
  - `python-dotenv`, `starlette==0.38.6` (Konfigurasi & Backend server bawaan)

### 4. Folder Tambahan (`data`, `models`, `notebooks`)
- **`models/`**: Tempat penyimpanan bobot model final `mobilenetv2_waste.keras`.
- **`data/`**: Direktori dataset Kaggle dan output processing yang digunakan secara luring.
- **`notebooks/`**: Berisi `swm_model.ipynb` sebagai wadah eksperimen model awal (Training, komparasi Early Stopping, dsb).

## Catatan Tambahan (Kesesuaian `README.md`)
- `README.md` telah disinkronisasikan dan divalidasi. 
- Folder `data/` telah ditambahkan ke skema *"Project Directory Tree"* pada `README.md` agar merepresentasikan secara presisi *state* direktori proyek saat ini.
- Link Github yang Anda ubah menjadi repositori `Ari-1711` sudah tercatat.
