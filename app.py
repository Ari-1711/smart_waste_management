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

# 2. Custom Design System: Tinted Dark Eco Theme & Responsive Layout
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600;700;800&display=swap');

    /* Global Typography & Theme Colors */
    html, body, [class*="css"] {
        font-family: 'Outfit', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    }

    .stApp {
        background-color: #0b131f;
        color: #f8fafc;
    }

    /* Top Status Indicator Pill */
    .status-pill {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        padding: 6px 14px;
        background: rgba(16, 185, 129, 0.12);
        border: 1px solid rgba(16, 185, 129, 0.3);
        color: #34d399;
        border-radius: 9999px;
        font-size: 0.85rem;
        font-weight: 600;
        letter-spacing: 0.4px;
        margin-bottom: 16px;
    }

    /* Result Card - Organik (Emerald) */
    .result-card-organic {
        background: linear-gradient(145deg, #065f46 0%, #059669 100%);
        border: 1px solid rgba(52, 211, 153, 0.3);
        color: #ffffff;
        padding: 28px 24px;
        border-radius: 16px;
        box-shadow: 0 16px 32px rgba(5, 150, 105, 0.25);
        text-align: center;
        margin-bottom: 24px;
        animation: fadeIn 0.4s cubic-bezier(0.16, 1, 0.3, 1);
    }

    /* Result Card - Anorganik (Cyan / Indigo) */
    .result-card-inorganic {
        background: linear-gradient(145deg, #1e3a8a 0%, #2563eb 100%);
        border: 1px solid rgba(96, 165, 250, 0.3);
        color: #ffffff;
        padding: 28px 24px;
        border-radius: 16px;
        box-shadow: 0 16px 32px rgba(37, 99, 235, 0.25);
        text-align: center;
        margin-bottom: 24px;
        animation: fadeIn 0.4s cubic-bezier(0.16, 1, 0.3, 1);
    }

    .result-title {
        font-size: 1.75rem;
        font-weight: 800;
        margin: 0 0 6px 0;
        color: #ffffff;
        letter-spacing: -0.5px;
    }

    .confidence-score {
        font-size: 3.4rem;
        font-weight: 800;
        letter-spacing: -1.5px;
        line-height: 1;
        margin: 12px 0 8px 0;
    }

    .confidence-label {
        font-size: 0.9rem;
        font-weight: 500;
        opacity: 0.92;
        margin: 0;
    }

    /* Empty State Guide Card */
    .guide-card {
        background: rgba(15, 23, 42, 0.6);
        border: 1px dashed rgba(255, 255, 255, 0.15);
        border-radius: 16px;
        padding: 26px;
        margin-top: 10px;
    }

    .guide-step {
        display: flex;
        align-items: flex-start;
        gap: 14px;
        margin-bottom: 18px;
    }

    .guide-step:last-child {
        margin-bottom: 0;
    }

    .step-num {
        background: rgba(16, 185, 129, 0.2);
        border: 1px solid rgba(16, 185, 129, 0.4);
        color: #34d399;
        width: 28px;
        height: 28px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 700;
        font-size: 0.88rem;
        flex-shrink: 0;
    }

    .step-text {
        font-size: 0.98rem;
        line-height: 1.5;
        color: #cbd5e1;
    }

    /* Clean Container & Camera Styling */
    [data-testid="stCameraInput"] {
        width: 100% !important;
    }

    [data-testid="stCameraInput"] > div {
        width: 100% !important;
        max-width: 100% !important;
        border-radius: 16px !important;
        overflow: hidden !important;
        background: rgba(15, 23, 42, 0.6) !important;
        border: 1px solid rgba(255, 255, 255, 0.12) !important;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.2) !important;
        padding: 8px !important;
    }

    [data-testid="stCameraInput"] video {
        width: 100% !important;
        height: auto !important;
        aspect-ratio: 4 / 3 !important;
        object-fit: cover !important;
        border-radius: 12px !important;
    }

    /* Thumb-friendly Shutter Button */
    [data-testid="stCameraInput"] button {
        width: 100% !important;
        padding: 14px 20px !important;
        font-size: 1rem !important;
        font-weight: 700 !important;
        border-radius: 12px !important;
        background: linear-gradient(135deg, #10b981 0%, #059669 100%) !important;
        color: #ffffff !important;
        border: none !important;
        margin-top: 10px !important;
        box-shadow: 0 4px 16px rgba(16, 185, 129, 0.35) !important;
        transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1) !important;
        cursor: pointer !important;
    }

    [data-testid="stCameraInput"] button:hover {
        background: linear-gradient(135deg, #059669 0%, #047857 100%) !important;
        box-shadow: 0 6px 20px rgba(16, 185, 129, 0.45) !important;
    }

    [data-testid="stCameraInput"] button:active {
        transform: translateY(1px) !important;
    }

    /* Custom Streamlit Tabs Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: rgba(15, 23, 42, 0.5);
        padding: 6px;
        border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 0.08);
    }

    .stTabs [data-baseweb="tab"] {
        height: 44px;
        border-radius: 8px;
        font-weight: 600;
        font-size: 0.95rem;
        color: #94a3b8;
    }

    .stTabs [aria-selected="true"] {
        background-color: rgba(16, 185, 129, 0.15) !important;
        color: #34d399 !important;
        border: 1px solid rgba(16, 185, 129, 0.3) !important;
    }

    /* Keyframes Animation */
    @keyframes fadeIn {
        from {
            opacity: 0;
            transform: translateY(10px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    /* Responsive Adjustments for Mobile Screens */
    @media (max-width: 768px) {
        .confidence-score {
            font-size: 2.6rem;
        }
        .result-title {
            font-size: 1.45rem;
        }
        [data-testid="stCameraInput"] video {
            aspect-ratio: 3 / 4 !important;
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
    # Main Content Area Layout (Input vs Result)
    col_input, col_result = st.columns([1, 1], gap="large")

    image = None

    with col_input:
        st.subheader("📸 Input Sampah")
        st.write("Unggah foto atau ambil gambar menggunakan kamera perangkat:")

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