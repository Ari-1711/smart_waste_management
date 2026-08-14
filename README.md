<div align="center">

[🇬🇧 Read in English](README.md) | [🇮🇩 Baca dalam Bahasa Indonesia](README.id.md)

# ♻️ Smart Waste Management: AI-Powered Classification

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org)
[![TensorFlow](https://img.shields.io/badge/TensorFlow-2.x-FF6F00.svg?style=for-the-badge&logo=tensorflow&logoColor=white)](https://www.tensorflow.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B.svg?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io)
[![Keras](https://img.shields.io/badge/Keras-D00000.svg?style=for-the-badge&logo=keras&logoColor=white)](https://keras.io)
[![Kaggle Dataset](https://img.shields.io/badge/Kaggle-Dataset-20BEFF.svg?style=for-the-badge&logo=kaggle&logoColor=white)](https://www.kaggle.com/datasets/techsash/waste-classification-data)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)

**An Edge-Ready, Deep Learning Web Application for Automated Organic vs. Recyclable Waste Sorting.**

[**🚀 Launch Live Demo**](https://smartwastemanagement-bvasn5fbt3szlfmmnvvd6f.streamlit.app/)

</div>

---

> [!NOTE]  
> **Live Demo Notice (Streamlit Cloud)**  
> If you are accessing the live demo for the first time or after a period of inactivity, the application may take a moment to "wake up" from its cold-start sleep state. **You may need to refresh/reload the page once if it appears stuck or times out initially.** This is a standard container lifecycle behavior of the Streamlit Community Cloud free tier, not a runtime error or application bug. 

---

## 🚀 Executive Summary & Elevator Pitch

This project delivers an end-to-end Machine Learning pipeline utilizing Transfer Learning (MobileNetV2) to classify waste into **Organic** and **Recyclable** categories. Built with a focus on real-world applicability and deployment readiness, the model achieves near-production accuracy while maintaining a lightweight footprint suitable for future Edge AI integration. The solution is encapsulated in an interactive Streamlit web application, demonstrating seamless real-time inference and a robust user experience.

### 📊 Key Performance Metrics

| Metric | Value | Impact |
| :--- | :--- | :--- |
| **Validation Accuracy** | `93.88%` | High reliability for automated sorting systems. |
| **Validation Loss** | `0.1641` | Strong model generalization with minimal overfitting. |
| **Average F1-Score** | `94.00%` | Balanced precision and recall across both waste classes. |
| **Inference Confidence** | `91% - 99.69%` | Highly decisive predictions on real-world, unseen data. |
| **Data Volume** | `22,564 Images` | Trained on a robust, diverse Kaggle dataset. |

---

## 🗄️ Dataset Citation & Specifications

This project leverages the prominent **[Waste Classification Data](https://www.kaggle.com/datasets/techsash/waste-classification-data)** from Kaggle. 

- **Total Images:** 22,564 high-resolution images.
- **Classes:** Binary classification (Organic `O` vs. Recyclable `R`).
- **Data Split Strategy:** 
  - **Training Set (80%):** Utilized for model parameter optimization.
  - **Validation Set (20%):** Held out for unbiased evaluation and hyperparameter tuning during training.

---

## 🧠 Architecture & End-to-End Workflow

The pipeline employs a **MobileNetV2** backbone, pre-trained on ImageNet. The base layers are frozen to act as a powerful feature extractor, while a custom top block is appended and trained for this specific binary classification task.

![Architecture & Workflow Diagram](docs/assets/flow.png)

---

## 🔬 Experimental Benchmarks & Engineering Trade-Offs

To optimize training efficiency and prevent overfitting, we conducted a rigorous comparative analysis using the **Early Stopping** callback by monitoring `val_loss`. 

### Early Stopping Patience Analysis

| Patience | Epochs Stopped | Val Accuracy | Val Loss | Compute Efficiency | Verdict |
| :---: | :---: | :---: | :---: | :---: | :--- |
| `3` | ~8 | 91.50% | 0.2100 | Very High | Terminated prematurely; under-optimized. |
| `5` | ~12 | 92.75% | 0.1850 | High | Good baseline, but leaves accuracy on the table. |
| `7` | ~16 | 93.10% | 0.1780 | Moderate | Diminishing returns begin here. |
| **`10`** | **~22** | **93.88%** | **0.1641** | **Standard** | **Optimal balance achieved.** |

**Engineering First-Principles Analysis:**
In Edge AI scenarios, training compute is less of a bottleneck than inference latency. However, during the training phase, setting patience to 10 proved optimal. Patience values < 7 saved compute time but sacrificed over 2% in absolute accuracy (a significant margin in production sorting facilities). Patience 10 allowed the optimizer (Adam) to navigate local minima effectively, yielding a robust `0.1641` loss. The marginal cost of ~6 extra epochs was strongly justified by the resulting generalization capability (93.88% accuracy) on unseen data.

---

## 🎯 Model Evaluation

The model demonstrates exceptional balance, effectively mitigating the common pitfall of biasing towards the majority class.

### Classification Report (Validation Set)

| Class | Precision | Recall | F1-Score |
| :--- | :--- | :--- | :--- |
| **Organic (O)** | 0.95 | 0.94 | **0.94** |
| **Recyclable (R)** | 0.93 | 0.94 | **0.94** |
| *Macro Avg* | *0.94* | *0.94* | *0.94* |
| *Weighted Avg* | *0.94* | *0.94* | *0.94* |

---

## 💻 Web App Features & Local Quickstart

The Streamlit application is designed for intuitive interaction and robust error handling.
- **Features:** File Upload (JPG/PNG), Live Camera Input, Real-time Inference, Visual Confidence Gauge, Cached Model Loading (`@st.cache_resource`) for fast execution.

### Local Setup Instructions

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/Ari-1711/smart-waste-management.git
   cd smart-waste-management
   ```

2. **Create a Virtual Environment (Recommended):**
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Streamlit App:**
   ```bash
   streamlit run app.py
   ```

---

## 📂 Project Directory Tree

```text
smart_waste_management/
│
├── app.py                     # Main Streamlit application entry point
├── data/                      # Dataset and processed images folder
├── src/
│   └── predictor.py           # Inference logic and image preprocessing functions
├── models/
│   └── mobilenetv2_waste.keras # Pre-trained Keras model weights (frozen)
├── notebooks/
│   └── swm_model.ipynb        # Model architecture, training, and evaluation notebook
├── requirements.txt           # Project dependencies
└── README.md                  # Project documentation (You are here)
```

---

## 👥 Authors, Roles & Contribution Breakdown

This project originated as academic research at **Universitas Mercu Buana** and was subsequently scaled into a production-ready web application.

- **Ari Hermawan** — *Lead ML Engineer & Streamlit Developer*
  - Designed model architecture, preprocessing, and augmentation pipelines.
  - Engineered the Early Stopping experimentation framework and trained the model.
  - Developed, optimized, and deployed the interactive Streamlit web application.
- **Royhan Achmad** — *Academic Researcher*
  - Conducted extensive literature reviews and compiled theoretical foundations.
  - Managed reference formatting and structured the academic report documentation.
- **Adistya Firdaus** — *Academic Researcher*
  - Led dataset validation and integrity checks.
  - Executed comparative reporting and finalized technical documentation.
- **Essy Malay Sari Sakti, S.Kom., M.M.S.I.** — *Advisor / Dosen Pembimbing*
  - Provided strategic guidance, academic oversight, and project validation.

---

## 🛠️ Tech Stack & Future Roadmap

**Core Technologies:**
- **Languages:** Python 3.10+
- **Deep Learning:** TensorFlow 2.x, Keras, MobileNetV2
- **Data Processing:** NumPy, Pillow (PIL)
- **Frontend / Deployment:** Streamlit, Streamlit Community Cloud

**Future Roadmap:**
1. **Edge Deployment:** Optimize the model utilizing TensorFlow Lite for deployment on resource-constrained Edge IoT devices (e.g., NVIDIA Jetson Nano, Raspberry Pi) integrated with physical sorting bins.
2. **Multi-Class Expansion:** Expand the dataset and retrain the model to classify sub-categories (e.g., Glass, Plastic, Paper, Metal, E-Waste) to support more granular recycling processes.
3. **Continuous Learning:** Implement a feedback loop in the web app to collect misclassified images for future model retraining.
