# Early Prediction of Gallstone Disease

This repository contains the dataset, model training notebooks, and an interactive clinical screening prototype for the paper:
**"Early Prediction of Gallstone Disease Using Validated Machine Learning Models on Bioimpedance and Laboratory Data"**
Submitted to *Clinica Chimica Acta* (Ref No: CCACTA-D-26-00706).

---

## 📁 Repository Structure

* `app.py` - Premium Streamlit web application for clinical screening, risk prediction, and local feature explanation.
* `Dataset/Data Gabungan/fix_data_gabungan_fe_tambahan_2.csv` - The processed combined dataset (Turkish UCI cohort and Indonesian local cohort).
* `Tesis Colab/` - Jupyter notebooks containing data preprocessing, feature engineering, cross-validation, and hyperparameter tuning for Logistic Regression, Random Forest, XGBoost, LightGBM, ANN, LSTM, and TabNet.
* `Paper/Figures/` - High-resolution figures generated for the revised manuscript, including ROC curves, confusion matrices, Calibration plot, and Decision Curve Analysis (DCA).
* `Paper/Response_to_Reviewers.md` - Detailed point-by-point response to the reviewers' comments.

---

## 🚀 Getting Started

### Prerequisites

Ensure you have Python 3.10+ installed. Install the required libraries using pip:

```bash
pip install streamlit pandas numpy scikit-learn xgboost lightgbm imbalanced-learn matplotlib seaborn
```

### Running the Screening Dashboard

To start the interactive Streamlit clinical decision support system, run:

```bash
streamlit run app.py
```

Open `http://localhost:8501` in your browser to interact with the application.

---

## 🔬 Model Validation & Replicability

* The core model training pipelines are located in the `Tesis Colab/` folder.
* **10-Fold Cross-Validation** and **External Cohort Validation** (Turkish cohort $\rightarrow$ Indonesian cohort) scripts are detailed in the notebooks and replication scripts.
* **Decision Curve Analysis (DCA)** and **Calibration curves** are integrated into both the manuscript and the web application.
