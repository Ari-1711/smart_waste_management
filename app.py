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
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Outfit', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    /* Status Pill */
    .status-pill {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 4px 12px;
        background: rgba(16, 185, 129, 0.12);
        border: 1px solid rgba(16, 185, 129, 0.25);
        color: #10b981;
        border-radius: 9999px;
        font-size: 0.82rem;
        font-weight: 600;
        letter-spacing: 0.3px;
        margin-bottom: 12px;
    }

    /* Result Cards */
    .result-card-organic {
        background: linear-gradient(135deg, #059669 0%, #10b981 100%);
        color: #ffffff;
        padding: 24px;
        border-radius: 16px;
        box-shadow: 0 12px 30px rgba(16, 185, 129, 0.25);
        text-align: center;
        margin-bottom: 20px;
        animation: fadeIn 0.4s cubic-bezier(0.16, 1, 0.3, 1);
    }

    .result-card-inorganic {
        background: linear-gradient(135deg, #2563eb 0%, #3b82f6 100%);
        color: #ffffff;
        padding: 24px;
        border-radius: 16px;
        box-shadow: 0 12px 30px rgba(59, 130, 246, 0.25);
        text-align: center;
        margin-bottom: 20px;
        animation: fadeIn 0.4s cubic-bezier(0.16, 1, 0.3, 1);
    }

    .result-title {
        font-size: 1.6rem;
        font-weight: 700;
        margin: 0 0 6px 0;
        color: #ffffff;
    }

    .confidence-score {
        font-size: 3rem;
        font-weight: 800;
        letter-spacing: -1.5px;
        line-height: 1.1;
        margin: 10px 0;
    }

    .confidence-label {
        font-size: 0.88rem;
        font-weight: 500;
        opacity: 0.92;
        margin: 0;
    }

    /* Empty state guide card */
    .guide-card {
        background: rgba(255, 255, 255, 0.02);
        border: 1px dashed rgba(255, 255, 255, 0.15);
        border-radius: 16px;
        padding: 24px;
        margin-top: 10px;
    }

    .guide-step {
        display: flex;
        align-items: flex-start;
        gap: 12px;
        margin-bottom: 16px;
    }

    .guide-step:last-child {
        margin-bottom: 0;
    }

    .step-num {
        background: rgba(255, 255, 255, 0.1);
        color: #ffffff;
        width: 26px;
        height: 26px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 700;
        font-size: 0.85rem;
        flex-shrink: 0;
    }

    .step-text {
        font-size: 0.95rem;
        line-height: 1.5;
        opacity: 0.9;
    }

    /* Keyframes animation */
    @keyframes fadeIn {
        from {
            opacity: 0;
            transform: translateY(8px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    /* Tab styling customization */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }

    .stTabs [data-baseweb="tab"] {
        height: 46px;
        white-space: pre-wrap;
        border-radius: 10px;
        font-weight: 600;
    }

    /* Responsive adjustment */
    @media (max-width: 768px) {
        .confidence-score {
            font-size: 2.3rem;
        }
        .result-title {
            font-size: 1.35rem;
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

# 4. Header & Status Pill
st.markdown('<div class="status-pill">⚡ Model Active • MobileNetV2 Ready</div>', unsafe_allow_html=True)
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
                        <div class="result-title">🌱 {label}</div>
                        <div class="confidence-score">{confidence:.1f}%</div>
                        <p class="confidence-label">Tingkat Keyakinan (Confidence Score)</p>
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
                        <div class="result-title">♻️ {label}</div>
                        <div class="confidence-score">{confidence:.1f}%</div>
                        <p class="confidence-label">Tingkat Keyakinan (Confidence Score)</p>
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
            st.markdown(
                """
                <div class="guide-card">
                    <div class="guide-step">
                        <div class="step-num">1</div>
                        <div class="step-text">Pilih tab <b>📁 Upload Foto</b> atau <b>📷 Gunakan Kamera</b> di sebelah kiri.</div>
                    </div>
                    <div class="guide-step">
                        <div class="step-num">2</div>
                        <div class="step-text">Berikan sampel gambar sampah yang ingin dianalisis.</div>
                    </div>
                    <div class="guide-step">
                        <div class="step-num">3</div>
                        <div class="step-text">Hasil prediksi AI & rekomendasi pengolahan akan otomatis ditampilkan di sini.</div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

st.divider()
st.caption("Smart Waste Management System | Powered by TensorFlow & Streamlit")