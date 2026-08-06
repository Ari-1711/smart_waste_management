import os
from PIL import Image
import streamlit as st
import streamlit.components.v1 as components
from src.predictor import load_model_waste, predict_image

# 1. Konfigurasi Halaman Web
st.set_page_config(
    page_title="Smart Waste Classifier AI",
    page_icon="♻️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# SCRIPT DETEKSI AUTO-SLEEP & AUTO-RELOAD (JAVASCRIPT INJECTION)
components.html(
    """
    <script>
    // Deteksi saat pengguna kembali membuka tab yang sudah ditinggal lama
    document.addEventListener("visibilitychange", function() {
        if (document.visibilityState === "visible") {
            const streamlitDoc = window.parent.document;
            const connectionStatus = streamlitDoc.querySelector('[data-testid="stStatusWidget"]');
            
            // Jika terdeteksi offline / disconnect
            if (connectionStatus && (connectionStatus.innerText.includes("Offline") || connectionStatus.innerText.includes("Connecting"))) {
                alert("Sesi kamu terputus/tertidur (Auto-Sleep). Halaman akan dimuat ulang otomatis...");
                window.parent.location.reload();
            }
        }
    });

    // Deteksi event offline
    window.addEventListener('offline', function() {
        alert("Koneksi terputus. Silakan klik OK untuk mereload halaman.");
        window.parent.location.reload();
    });
    </script>
    """,
    height=0,
)

# 2. Custom CSS untuk Styling UI Modern & Responsif
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif;
    }

    /* Card styling */
    .custom-card {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.12);
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 20px;
        backdrop-filter: blur(10px);
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.1);
    }

    /* Result Cards */
    .result-card-organic {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        color: #ffffff;
        padding: 20px;
        border-radius: 16px;
        box-shadow: 0 10px 25px rgba(56, 239, 125, 0.25);
        text-align: center;
        margin-bottom: 20px;
    }

    .result-card-inorganic {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        color: #ffffff;
        padding: 20px;
        border-radius: 16px;
        box-shadow: 0 10px 25px rgba(42, 82, 152, 0.25);
        text-align: center;
        margin-bottom: 20px;
    }

    .confidence-score {
        font-size: 2.8rem;
        font-weight: 800;
        letter-spacing: -1px;
        margin: 8px 0;
    }

    .badge-label {
        display: inline-block;
        padding: 6px 16px;
        border-radius: 50px;
        font-size: 0.9rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1px;
        background: rgba(255, 255, 255, 0.25);
        margin-bottom: 10px;
    }

    /* Tab styling customization */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }

    .stTabs [data-baseweb="tab"] {
        height: 48px;
        white-space: pre-wrap;
        border-radius: 12px;
        font-weight: 600;
    }

    /* Responsive adjustment for small screens */
    @media (max-width: 768px) {
        .confidence-score {
            font-size: 2.2rem;
        }
        .custom-card {
            padding: 16px;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# 3. Path Model & Caching
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "models", "mobilenetv2_waste.keras")


@st.cache_resource
def get_model():
    return load_model_waste(MODEL_PATH)


model = get_model()

# 4. Header & Banner Notifikasi (UI/UX)
st.title("♻️ Smart Waste Management System")
st.caption("Aplikasi AI Berbasis MobileNetV2 untuk Klasifikasi Sampah Organik vs Anorganik")

# Banner Notifikasi Auto-Sleep & Waking Up
with st.expander("⚡ **Petunjuk Server & Koneksi (Mode Sleep / Waking Up)**", expanded=False):
    st.info(
        "ℹ️ **Informasi Server Waking Up:** Jika server merespons lambat saat pertama dibuka, "
        "hal itu terjadi karena server dalam mode *waking up* (membangunkan model AI dari status sleep).\n\n"
        "💡 **Petunjuk Koneksi:** Jika aplikasi tidak merespons saat ditinggal lama, "
        "cukup reload/refresh halaman browser kamu (**F5** atau swipe down di HP)."
    )

st.divider()

# 5. Penanganan Pengecekan Ketersediaan Model
if model is None:
    st.error(
        "❌ **Error Model:** File model tidak ditemukan di `models/mobilenetv2_waste.keras`. "
        "Pastikan file model Keras sudah berada pada direktori yang benar."
    )
else:
    # Main Content Area
    col_input, col_result = st.columns([1, 1], gap="medium")

    image = None

    with col_input:
        st.subheader("📸 Input Sampah")
        st.write("Unggah gambar atau gunakan kamera perangkat kamu:")

        tab_upload, tab_camera = st.tabs(["📁 Upload Foto", "📷 Gunakan Kamera"])

        with tab_upload:
            uploaded_file = st.file_uploader(
                "Pilih foto sampah (JPG, JPEG, PNG)...",
                type=["jpg", "jpeg", "png"],
                key="uploader",
            )
            if uploaded_file is not None:
                try:
                    image = Image.open(uploaded_file).convert("RGB")
                except Exception as e:
                    st.error("Gagal membaca file gambar. Silakan coba file lain.")

        with tab_camera:
            camera_file = st.camera_input("Ambil foto secara langsung", key="camera")
            if camera_file is not None:
                try:
                    image = Image.open(camera_file).convert("RGB")
                except Exception as e:
                    st.error("Gagal mengambil foto dari kamera.")

        if image is not None:
            st.image(
                image,
                caption="Preview Gambar Input",
                use_container_width=True,
            )

    with col_result:
        st.subheader("📊 Hasil Analisis AI")

        if image is not None:
            with st.spinner("⚡ AI sedang menganalisis sampel sampah..."):
                label, confidence, category = predict_image(model, image)

            conf_percentage = float(confidence) / 100.0

            if category == "O":  # Organik
                st.markdown(
                    f"""
                    <div class="result-card-organic">
                        <span class="badge-label">🌱 KLASIFIKASI SAMPAH</span>
                        <h2 style="margin: 0; color: white;">{label}</h2>
                        <div class="confidence-score">{confidence:.1f}%</div>
                        <p style="margin: 0; opacity: 0.9;">Tingkat Keyakinan (Confidence Score)</p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                st.progress(conf_percentage)
                st.success(
                    "💡 **Saran Pengolahan (Organik):**\n"
                    "- Dapat diolah menjadi **kompos cair/padat** atau pupuk tanaman.\n"
                    "- Pisahkan dari bahan plastik/anorganik agar pembusukan alami optimal."
                )

            elif category == "R":  # Anorganik / Recyclable
                st.markdown(
                    f"""
                    <div class="result-card-inorganic">
                        <span class="badge-label">♻️ KLASIFIKASI SAMPAH</span>
                        <h2 style="margin: 0; color: white;">{label}</h2>
                        <div class="confidence-score">{confidence:.1f}%</div>
                        <p style="margin: 0; opacity: 0.9;">Tingkat Keyakinan (Confidence Score)</p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                st.progress(conf_percentage)
                st.info(
                    "💡 **Saran Pengolahan (Anorganik):**\n"
                    "- Sampah dapat **didaur ulang** (Recyclable).\n"
                    "- Bersihkan sisa kotoran/cairan sebelum disetorkan ke bank sampah atau daur ulang."
                )
            else:
                st.error("❌ Gagal menganalisis gambar. Silakan coba unggah ulang.")
        else:
            st.info(
                "👈 **Langkah Penggunaan:**\n"
                "1. Pilih tab **📁 Upload Foto** atau **📷 Gunakan Kamera** di sebelah kiri.\n"
                "2. Berikan sampel gambar sampah.\n"
                "3. Hasil klasifikasi & rekomendasi pengolahan akan langsung muncul di sini!"
            )

st.divider()
st.caption("Smart Waste Management System | Powered by TensorFlow & Streamlit")