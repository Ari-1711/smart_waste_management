<div align="center">

[🇮🇩 Baca dalam Bahasa Indonesia](README.md) | [🇬🇧 Read in English](README.en.md)

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

## 📑 Table of Contents
- [🚀 Executive Summary & Elevator Pitch](#-executive-summary--elevator-pitch)
- [🗄️ Dataset Citation & Specifications](#️-dataset-citation--specifications)
- [🧠 Architecture & End-to-End Workflow](#-architecture--end-to-end-workflow)
- [🔬 Experimental Benchmarks & Engineering Trade-Offs](#-experimental-benchmarks--engineering-trade-offs)
- [🎯 Model Evaluation](#-model-evaluation)
- [🔍 Engineering Reflections & Technical Evaluation](#-engineering-reflections--technical-evaluation)
- [💻 Web App Features & Local Quickstart](#-web-app-features--local-quickstart)
- [📂 Project Directory Tree](#-project-directory-tree)
- [👥 Authors, Roles & Contribution Breakdown](#-authors-roles--contribution-breakdown)
- [🛠️ Tech Stack & Future Roadmap](#️-tech-stack--future-roadmap)

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

The project's architectural workflow is designed with the following systematic stages:
**Image Preprocessing** ➔ **Transfer Learning MobileNetV2** (Base layers frozen + Custom Top: GAP2D & Sigmoid) ➔ **Experimental Training Max 25 Epochs** (Comparison of Patience 3, 5, 7, 10) ➔ **Best Model Selection** (Patience 10) ➔ **New Image Inference** ➔ **Streamlit Deployment Integration**.

![Architecture & Workflow Diagram](docs/assets/flow.png)

---

## 🔬 Experimental Benchmarks & Engineering Trade-Offs

All training scenarios were executed with a baseline hyperparameter configuration: a **maximum limit of 25 epochs**, the **Adam** optimizer, and the **Binary Crossentropy** objective function. To optimize training efficiency and prevent overfitting, we conducted a rigorous comparative analysis using the **Early Stopping** callback by monitoring `val_accuracy` and enabling the `restore_best_weights=True` parameter.

### Early Stopping Patience Analysis

| Patience | Epochs Stopped | Best Epoch | Train Acc | Val Accuracy | Train Loss | Val Loss | Verdict |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| `3` | 18 | 15 | 93.36% | 93.84% | 0.1776 | 0.1652 | Computationally efficient (locks best weights at epoch 15). |
| `5` | 16 | 11 | 93.36% | 93.66% | 0.1773 | 0.1716 | Terminated prematurely at a local optimum. |
| `7` | 22 | 15 | 93.36% | 93.84% | 0.1776 | 0.1652 | Stable, restores identical weights as Patience 3. |
| **`10`** | **25** | **25** | **93.73%** | **93.88%** | **0.1677** | **0.1641** | **Absolute best performance (lowest validation loss).** |

**Engineering First-Principles Analysis:**
In Edge AI scenarios, training compute is less of a bottleneck than inference latency. However, during the training phase, setting patience to 10 proved to yield the most optimal performance (lowest loss). There is a clear computational trade-off: the accuracy improvement margin from Patience 7 (93.84% at epoch 22 with best epoch 15) to Patience 10 (93.88% at epoch 25) is only 0.04%. This slight accuracy improvement requires full execution up to the 25-epoch limit to minimize the validation loss to 0.1641, whereas configurations with tighter tolerances (such as Patience 3 and 7) successfully locked in the 93.84% accuracy earlier. Ultimately, Patience 10 allows the optimizer (Adam) to navigate local minima more effectively, resulting in the absolute best model performance.

---

## 🎯 Model Evaluation

The model demonstrates exceptional balance, effectively mitigating the common pitfall of biasing towards the majority class.

### Classification Report (Validation Set)

| Class | Precision | Recall | F1-Score |
| :--- | :---: | :---: | :---: |
| **Organic (O)** | 0.96 | 0.93 | **0.94** |
| **Recyclable (R)** | 0.92 | 0.95 | **0.93** |
| *Macro Avg / Overall* | *0.94* | *0.94* | **0.94** |

---

## 🔍 Engineering Reflections & Technical Evaluation

Summary of technical challenges, applied mitigations, and future system development directions:

### 1. Cold-Start Lifecycle (Streamlit Cloud)

* **Challenge:** Initial access requires a one-time reload because the free-tier container goes into hibernation (sleep) when idle.
* **Mitigation & Solution:** We have currently implemented model caching using `@st.cache_resource` as an initial mitigation. For a permanent solution moving forward, a migration to a containerized architecture (Docker/Cloud Run) is planned to completely eliminate wake-up latency.

### 2. Iteration Efficiency & Model Convergence

* **Context:** Training was capped at 25 epochs as a controlled iteration limit using a T4 GPU on Google Colab.
* **Findings:** The model enters a stable convergence phase at epochs 15–25. The *Patience 10* configuration locks in optimal performance (Val Loss 0.1641) with a marginal accuracy increase of only 0.04% compared to Patience 3/7, proving that adding further epochs is no longer computationally efficient.

### 3. Class Granularity & Data Scalability

* **Challenge:** Classification is still binary (Organic vs Recyclable) with a dataset variation (22,564 images) that is still limited to cover the diversity of real-world waste.
* **Future Development:**
  * Expansion to specific multi-classes (Plastic, Paper, Glass, Metal, E-Waste) to support integration with industrial recycling systems.
  * Exploration of targeted fine-tuning on the top layers of MobileNetV2 to improve accuracy on complex object variations.

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
├── data/                      # Dataset and processed images folder
├── docs/                      
│   └── assets/                # Documentation assets (e.g., flow diagrams)
├── models/
│   └── mobilenetv2_waste.keras # Pre-trained Keras model weights (frozen)
├── notebooks/
│   └── swm_model.ipynb        # Model architecture, training, and evaluation notebook
├── src/
│   └── predictor.py           # Inference logic and image preprocessing functions
├── app.py                     # Main Streamlit application entry point
├── requirements.txt           # Project dependencies
├── .gitignore                 # Git ignore rules
├── Project_Summary.md         # Project summary & updates (for Obsidian vault)
├── README.en.md               # Project documentation (English version - You are here)
└── README.md                  # Project documentation (Indonesian version)
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
