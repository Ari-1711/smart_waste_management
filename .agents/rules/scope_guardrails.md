---
trigger: always_on
---

# AGENT GUARDRAILS & FOCUS SCOPE

## 🛑 STRICT RESTRICTIONS (DO NOT MODIFY)
1. **NO TOUCH ZONE - MODELS & NOTEBOOKS**:
   - DILARANG KERAS mengubah, menghapus, merename, atau membuat ulang file apa pun di dalam direktori `models/` (termasuk `models/mobilenetv2_waste.keras`).
   - DILARANG KERAS menyentuh atau mengubah isi file di dalam direktori `notebooks/` (termasuk `notebooks/swm_model.ipynb`).
   - Jangan pernah menjalankan script training ulang atau melakukan refactoring pada model ML.

## 🎯 PERMITTED SCOPE OF WORK
Agent HANYA DIIZINKAN mengedit file berikut:
- `app.py`
- `src/predictor.py` (hanya logika pemanggilan/preprocessing inference, BUKAN arsitektur model)
- `requirements.txt`
- `.agents/` atau file konfigurasi UI/Styling

## 🚀 PRIMARY GOALS
1. **Optimize UI/UX (Streamlit)**:
   - Buat tampilan Streamlit modern, rapi, dan intuitif (gunakan layout 2 kolom, kartu metrik confidence score, visual indikator warna Organik vs Anorganik).
2. **Maximize Performance & Fast Load**:
   - Wajib membungkus pemuatan model Keras menggunakan `@st.cache_resource` agar model hanya dimuat 1 kali ke RAM dan terhindar dari *timeout crash* saat server *waking up* dari status sleep.
   - Pindahkan logika berat ke fungsi ter-cache.
3. **Handle Connection & File Input Edge Cases**:
   - Berikan error handling yang baik untuk `st.file_uploader` dan `st.camera_input` agar UI tidak crash jika terjadi *disconnect* / *idle session*.