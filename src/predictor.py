import numpy as np
import tensorflow as tf
from PIL import Image


def load_model_waste(model_path="models/mobilenetv2_waste.keras"):
    """Memuat model TensorFlow yang sudah dilatih."""
    try:
        model = tf.keras.models.load_model(model_path)
        return model
    except Exception as e:
        print(f"Error memuat model: {e}")
        return None


def predict_image(model, image):
    """Menerima input gambar dari PIL, mengubah ukuran ke 224x224,

    dan mengembalikan label prediksi serta persentase keyakinan.
    """
    # Resize gambar sesuai input MobileNetV2
    img = image.resize((224, 224))

    # Konversi gambar ke array numpy
    img_array = tf.keras.utils.img_to_array(img)

    # Tambahkan dimensi batch menjadi (1, 224, 224, 3)
    img_batch = np.expand_dims(img_array, axis=0)

    # Lakukan prediksi
    score = model.predict(img_batch, verbose=0)[0][0]

    # Logika klasifikasi biner sesuai notebook (Organik vs Anorganik)
    if score > 0.5:
        label = "Anorganik (Recyclable)"
        confidence = score * 100
        category = "R"
    else:
        label = "Organik (Organic)"
        confidence = (1 - score) * 100
        category = "O"

    return label, confidence, category