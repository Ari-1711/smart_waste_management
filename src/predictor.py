import os
import numpy as np
import tensorflow as tf
from PIL import Image
import streamlit as st

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_MODEL_PATH = os.path.join(BASE_DIR, "models", "mobilenetv2_waste.keras")


@st.cache_resource(show_spinner="Memuat Model AI...")
def load_model_waste(model_path=None):
    if model_path is None:
        model_path = DEFAULT_MODEL_PATH

    if not os.path.isabs(model_path):
        model_path = os.path.join(BASE_DIR, model_path)

    if not os.path.exists(model_path):
        print(f"[DEBUG] File fisik TIDAK ADA di path: {model_path}")
        return None

    try:
        # Tambahkan compile=False agar tidak error jika ada custom metric/optimizer dari training
        model = tf.keras.models.load_model(model_path, compile=False)
        print(f"[DEBUG] Model berhasil dimuat dari: {model_path}")
        return model
    except Exception as e:
        # Tampilkan error sebenarnya di log Streamlit
        st_error_msg = f"Gagal memuat model TensorFlow: {e}"
        print(f"[DEBUG ERROR] {st_error_msg}")
        return None


def predict_image(model, image):
    """Menerima input gambar dari PIL, mengubah ukuran ke 224x224,
    dan mengembalikan label prediksi serta persentase keyakinan.
    """
    try:
        # Pastikan gambar format RGB
        if image.mode != "RGB":
            image = image.convert("RGB")

        # Resize gambar sesuai input MobileNetV2
        img = image.resize((224, 224))

        # Konversi gambar ke array numpy
        img_array = tf.keras.utils.img_to_array(img)

        # Tambahkan dimensi batch menjadi (1, 224, 224, 3)
        img_batch = np.expand_dims(img_array, axis=0)

        # Lakukan prediksi
        score = model.predict(img_batch, verbose=0)[0][0]

        # Logika klasifikasi biner
        if score > 0.5:
            label = "Anorganik (Recyclable)"
            confidence = score * 100
            category = "R"
        else:
            label = "Organik (Organic)"
            confidence = (1 - score) * 100
            category = "O"

        return label, float(confidence), category
    except Exception as e:
        print(f"[DEBUG ERROR PREDICT] Error saat prediksi: {e}")
        return "Error Analisis", 0.0, "E"