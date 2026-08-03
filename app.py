import os
from PIL import Image
import streamlit as st
from src.predictor import load_model_waste, predict_image

# 1. Konfigurasi Halaman Web
st.set_page_config(
    page_title="Smart Waste Classifier", page_icon="♻️", layout="centered"
)

# Hitung path absolut folder root proyek secara dinamis
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "models", "mobilenetv2_waste.keras")


# 2. Load model dengan cache
@st.cache_resource
def get_model():
    return load_model_waste(MODEL_PATH)


model = get_model()

# 3. Tampilan Header Utama
st.title("♻️ Smart Waste Management System")
st.write(
    "Aplikasi AI berbasis **MobileNetV2** untuk mengklasifikasikan sampah menjadi **Organik** atau **Anorganik** beserta tingkat keyakinannya."
)

st.divider()

# 4. Pengecekan Ketersediaan Model
if model is None:
    st.error(
        "❌ File model tidak ditemukan! Pastikan 'mobilenetv2_waste.keras' ada di dalam folder 'models/'."
    )
else:
    # 5. Widget Upload Gambar
    uploaded_file = st.file_uploader(
        "Unggah Foto Sampah (JPG, JPEG, PNG)...", type=["jpg", "jpeg", "png"]
    )

    if uploaded_file is not None:
        # Buka gambar yang diunggah
        image = Image.open(uploaded_file).convert("RGB")

        # Layout 2 Kolom: Kolom kiri untuk Gambar, Kolom kanan untuk Hasil
        col1, col2 = st.columns([1, 1])

        with col1:
            st.image(
                image, caption="Gambar yang Diunggah", use_container_width=True
            )

        with col2:
            st.subheader("Hasil Analisis AI:")
            with st.spinner("Sedang menganalisis gambar..."):
                label, confidence, category = predict_image(model, image)

            # Tampilkan Progress Bar Persentase
            conf_percentage = float(confidence) / 100.0

            if category == "R":
                st.success(f"### ♻️ {label}")
                st.write(f"**Keyakinan (Confidence):** {confidence:.2f}%")
                st.progress(conf_percentage)
                st.info(
                    "💡 **Saran:** Sampah anorganik/recyclable dapat didaur ulang. Pisahkan dari sampah basah!"
                )
            else:
                st.success(f"### 🍂 {label}")
                st.write(f"**Keyakinan (Confidence):** {confidence:.2f}%")
                st.progress(conf_percentage)
                st.info(
                    "💡 **Saran:** Sampah organik dapat diolah menjadi kompos atau pupuk tanaman."
                )

st.divider()
st.caption("Dikembangkan untuk Portofolio Machine Learning | Powered by Streamlit")