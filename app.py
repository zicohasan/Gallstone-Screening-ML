import streamlit as st
import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from imblearn.over_sampling import SMOTE

# Page configuration
st.set_page_config(
    page_title="Gallstone Risk Screening & Decision Support",
    page_icon="⚕️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom premium styling
st.markdown("""
    <style>
    .main {
        background-color: #f7f9fc;
        font-family: 'Inter', sans-serif;
    }
    h1 {
        color: #1e3d59;
        font-weight: 800;
        font-size: 2.2rem;
        margin-bottom: 0.2rem;
    }
    h2 {
        color: #17b978;
        font-weight: 700;
        font-size: 1.5rem;
    }
    .stButton>button {
        background-color: #1e3d59;
        color: white;
        border-radius: 8px;
        padding: 0.6rem 1.5rem;
        font-weight: 600;
        border: none;
    }
    .stButton>button:hover {
        background-color: #17b978;
        color: white;
    }
    .metric-card {
        background: white;
        padding: 1.2rem;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
        border: 1px solid #e1e8ed;
        margin-bottom: 1rem;
    }
    .metric-title {
        font-size: 0.85rem;
        color: #657786;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .metric-value {
        font-size: 1.4rem;
        font-weight: 700;
        color: #1e3d59;
    }
    </style>
""", unsafe_allow_html=True)

# ----------------- CACHED MODEL TRAINING -----------------
@st.cache_resource
def train_and_cache_models():
    # Load dataset
    data_path = 'Dataset/Data Gabungan/fix_data_gabungan_fe_tambahan_2.csv'
    if not os.path.exists(data_path):
        return None, None, None, None
        
    df = pd.read_csv(data_path)
    
    # Split into local and uci. We train on the UCI public dataset
    # (rows 294 onwards) since it contains both cases and controls (balanced).
    # This avoids the cohort confounding present in the merged dataset.
    df_uci = df.iloc[294:].copy()
    
    X = df_uci.drop(columns=['Gallstone Status'])
    y = df_uci['Gallstone Status']
    feature_names = X.columns.tolist()
    
    # Scale features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # SMOTE to ensure balance (though it is already ~50:50, 161:158)
    smote = SMOTE(random_state=42)
    X_res, y_res = smote.fit_resample(X_scaled, y)
    
    # Train Models
    rf = RandomForestClassifier(n_estimators=300, random_state=42)
    rf.fit(X_res, y_res)
    
    lr = LogisticRegression(max_iter=500, random_state=42)
    lr.fit(X_res, y_res)
    
    return rf, lr, scaler, feature_names

rf_model, lr_model, scaler, feature_names = train_and_cache_models()

# GFR CKD-EPI Helper
def calculate_gfr(scr, age, gender):
    # gender: 0 = Male, 1 = Female
    kappa = 0.7 if gender == 1 else 0.9
    alpha = -0.329 if gender == 1 else -0.411
    gender_factor = 1.018 if gender == 1 else 1.0
    
    min_ratio = min(scr / kappa, 1.0)
    max_ratio = max(scr / kappa, 1.0)
    
    gfr = 141 * (min_ratio ** alpha) * (max_ratio ** -1.209) * (0.993 ** age) * gender_factor
    return gfr

# Watson TBW Helper
def calculate_tbw(age, height, weight, gender):
    # gender: 0 = Male, 1 = Female
    if gender == 0:
        return 2.447 - (0.09156 * age) + (0.1074 * height) + (0.3362 * weight)
    else:
        return -2.097 + (0.1069 * height) + (0.2466 * weight)

# Boer Lean Mass Helper
def calculate_lm_pct(height, weight, gender):
    # gender: 0 = Male, 1 = Female
    if gender == 0:
        lm_kg = (0.407 * weight) + (0.267 * height) - 19.2
    else:
        lm_kg = (0.252 * weight) + (0.473 * height) - 48.3
    return (lm_kg / weight) * 100

# ----------------- SIDEBAR: INPUT PARAMETERS -----------------
st.sidebar.markdown("<h3 style='color: #1e3d59; font-weight:700;'>Patient Clinical Profile</h3>", unsafe_allow_html=True)

# Demographics
gender_str = st.sidebar.selectbox("Gender", ["Female", "Male"])
gender = 1 if gender_str == "Female" else 0

age = st.sidebar.slider("Age (Years)", 18, 100, 45)
height = st.sidebar.number_input("Height (cm)", 100.0, 220.0, 165.0, step=0.5)
weight = st.sidebar.number_input("Weight (kg)", 30.0, 200.0, 70.0, step=0.5)

# Comorbidities
st.sidebar.markdown("---")
st.sidebar.markdown("<h4 style='color: #1e3d59;'>Comorbidities / History</h4>", unsafe_allow_html=True)
cad = st.sidebar.checkbox("Coronary Artery Disease (CAD)", value=False)
dm = st.sidebar.checkbox("Diabetes Mellitus (DM)", value=False)
hyperlipidemia = st.sidebar.checkbox("Hyperlipidemia", value=False)
hypothyroidism = st.sidebar.checkbox("Hypothyroidism", value=False)
hypertension = st.sidebar.checkbox("Hypertension", value=False)
obesity_status = st.sidebar.checkbox("Obesity Status", value=False)
other_disease = st.sidebar.checkbox("Other Active Disease", value=False)

# Laboratory parameters
st.sidebar.markdown("---")
st.sidebar.markdown("<h4 style='color: #1e3d59;'>Blood Chemistry Labs</h4>", unsafe_allow_html=True)
creatinine = st.sidebar.number_input("Serum Creatinine (mg/dL)", 0.2, 10.0, 0.8, step=0.05)
alt = st.sidebar.number_input("Alanine Aminotransferase (ALT) (U/L)", 1.0, 500.0, 25.0, step=1.0)
ast = st.sidebar.number_input("Aspartate Aminotransferase (AST) (U/L)", 1.0, 500.0, 25.0, step=1.0)
glucose = st.sidebar.number_input("Random Glucose (mg/dL)", 40.0, 600.0, 95.0, step=5.0)
tc = st.sidebar.number_input("Total Cholesterol (TC) (mg/dL)", 50.0, 600.0, 190.0, step=5.0)
hdl = st.sidebar.number_input("HDL Cholesterol (mg/dL)", 10.0, 150.0, 50.0, step=2.0)
ldl = st.sidebar.number_input("LDL Cholesterol (mg/dL)", 10.0, 400.0, 110.0, step=5.0)
triglyceride = st.sidebar.number_input("Triglycerides (mg/dL)", 10.0, 1000.0, 130.0, step=5.0)
hgb = st.sidebar.number_input("Hemoglobin (HGB) (g/dL)", 5.0, 25.0, 13.5, step=0.1)


# ----------------- CALCULATE FEATURES -----------------
# 1. Comorbidity score
comorbidity = int(cad) + int(hypothyroidism) + int(dm) + int(hyperlipidemia) + int(obesity_status) + int(hypertension) + int(other_disease)

# 2. BMI
bmi = round(weight / ((height / 100) ** 2), 2)

# 3. Watson TBW
tbw = calculate_tbw(age, height, weight, gender)

# 4. Boer Lean Mass %
lm = calculate_lm_pct(height, weight, gender)

# 5. TBFR %
tbfr = 100 - lm

# 6. GFR via CKD-EPI
gfr = calculate_gfr(creatinine, age, gender)

# 7. Ratios
tc_hdl = tc / hdl
ldl_hdl = ldl / hdl
ai = (tc - hdl) / hdl
tg_hdl = triglyceride / hdl
nlm = weight - lm
body_fat_water = tbfr / tbw
de_ritis = ast / alt

# Construct feature dictionary in alphabetical matching order (same as the model expects)
feature_dict = {
    'Hypothyroidism': int(hypothyroidism),
    'Creatinine': creatinine,
    'Diabetes Mellitus (DM)': int(dm),
    'Alanin Aminotransferaz (ALT)': alt,
    'Low Density Lipoprotein (LDL)': ldl,
    'Hemoglobin (HGB)': hgb,
    'Coronary Artery Disease (CAD)': int(cad),
    'Total Body Fat Ratio (TBFR) (%)': tbfr,
    'Total Body Water (TBW)': tbw,
    'Height': height,
    'Weight': weight,
    'Body Mass Index (BMI)': bmi,
    'Gender': gender,
    'High Density Lipoprotein (HDL)': hdl,
    'Triglyceride': triglyceride,
    'Lean Mass (LM) (%)': lm,
    'Comorbidity': comorbidity,
    'Hyperlipidemia': int(hyperlipidemia),
    'Age': age,
    'Total Cholesterol (TC)': tc,
    'Aspartat Aminotransferaz (AST)': ast,
    'Glomerular Filtration Rate (GFR)': gfr,
    'Glucose': glucose,
    'TC/HDL Ratio': tc_hdl,
    'LDL/HDL Ratio': ldl_hdl,
    'Atherogenic Index': ai,
    'Triglyceride/HDL Ratio': tg_hdl,
    'Non-Lean Mass (NLM)': nlm,
    'Body Fat/Water Ratio': body_fat_water,
    'De Ritis Ratio': de_ritis
}

# Convert to dataframe in exact order
input_df = pd.DataFrame([feature_dict])[feature_names]


# ----------------- MAIN LAYOUT -----------------

st.markdown("<h1>⚕️ Gallstone Disease Risk Screening & Decision Support System</h1>", unsafe_allow_html=True)
st.markdown("<p style='color:#657786; font-size:1.1rem; margin-top:-0.5rem;'>Interactive Clinical Screening Interface powered by Machine Learning on Bioimpedance and Lab Data</p>", unsafe_allow_html=True)

# Tabs
tab1, tab2, tab3 = st.tabs(["📋 Patient Screening", "📊 Cohort Insights & Validation", "🔬 Local Interpretability"])

with tab1:
    col_l, col_r = st.columns([1, 1.2])
    
    with col_l:
        st.markdown("<h3 style='color:#1e3d59;'>Calculated Composites</h3>", unsafe_allow_html=True)
        
        # Display derived composites in grid
        c1, c2 = st.columns(2)
        with c1:
            st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-title">Body Mass Index (BMI)</div>
                    <div class="metric-value">{bmi:.1f} kg/m²</div>
                </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-title">Total Body Water (TBW)</div>
                    <div class="metric-value">{tbw:.1f} L</div>
                </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-title">eGFR (Renal Function)</div>
                    <div class="metric-value">{gfr:.1f} mL/min</div>
                </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-title">De Ritis Ratio (AST/ALT)</div>
                    <div class="metric-value">{de_ritis:.2f}</div>
                </div>
            """, unsafe_allow_html=True)

        with c2:
            st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-title">Lean Mass % (Boer)</div>
                    <div class="metric-value">{lm:.1f}%</div>
                </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-title">Body Fat % (TBFR)</div>
                    <div class="metric-value">{tbfr:.1f}%</div>
                </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-title">LDL/HDL Ratio</div>
                    <div class="metric-value">{ldl_hdl:.2f}</div>
                </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-title">Atherogenic Index</div>
                    <div class="metric-value">{ai:.2f}</div>
                </div>
            """, unsafe_allow_html=True)

    with col_r:
        st.markdown("<h3 style='color:#1e3d59;'>Screening Risk Assessment</h3>", unsafe_allow_html=True)
        
        if rf_model is None:
            st.error("Error: Could not load the combined dataset from 'Dataset/Data Gabungan/fix_data_gabungan_fe_tambahan_2.csv' to train the models.")
        else:
            # Scale patient data
            input_scaled = scaler.transform(input_df)
            
            # Predict
            prob_rf = rf_model.predict_proba(input_scaled)[0, 1]
            prob_lr = lr_model.predict_proba(input_scaled)[0, 1]
            
            # Actionable Risk Classification based on Decision Threshold
            # Let's use a threshold of 0.4 (optimizing recall/specificity balance for screening)
            screening_threshold = 0.4
            
            col_rf, col_lr = st.columns(2)
            with col_rf:
                st.markdown("### Random Forest Classifier")
                st.metric("Predicted Probability", f"{prob_rf * 100:.1f}%")
                if prob_rf >= screening_threshold:
                    st.error("⚠️ HIGH RISK (RF Recommendation: Refer for Ultrasonography)")
                else:
                    st.success("🟢 LOW RISK (RF Recommendation: Routine Follow-up)")
                    
            with col_lr:
                st.markdown("### Logistic Regression Classifier")
                st.metric("Predicted Probability", f"{prob_lr * 100:.1f}%")
                if prob_lr >= screening_threshold:
                    st.error("⚠️ HIGH RISK (LR Recommendation: Refer for Ultrasonography)")
                else:
                    st.success("🟢 LOW RISK (LR Recommendation: Routine Follow-up)")
            
            st.info(f"**Note**: Screening Decision Threshold is set to **{screening_threshold * 100:.0f}%** to maximize screening sensitivity (recall) and prevent false negatives (missed cases), in alignment with our Decision Curve Analysis.")

with tab2:
    st.markdown("<h3 style='color:#1e3d59;'>Cross-Cohort Generalizability & Validation</h3>", unsafe_allow_html=True)
    st.write(
        "A critical finding during manuscript revision was the existence of a severe cohort-specific distribution shift. "
        "The Indonesian cohort contains 294 healthy controls (0 cases), while the Turkish cohort contains 319 patients (161 cases, 158 controls). "
        "The model trained on the merged dataset suffered from **cohort confounding (batch effects)**, learning differences in age, BMI, and weight. "
        "Below are the clinical utility curves generated on the Turkish cohort (independent 10-fold CV) which represent realistic screening utility."
    )
    
    col_dca, col_cal = st.columns(2)
    with col_dca:
        st.markdown("### Decision Curve Analysis (DCA)")
        if os.path.exists("Paper/Figures/dca_plot.png"):
            st.image("Paper/Figures/dca_plot.png", use_container_width=True)
        else:
            st.info("DCA plot image not found in Paper/Figures/dca_plot.png")
            
    with col_cal:
        st.markdown("### Calibration Curve")
        if os.path.exists("Paper/Figures/calibration_plot.png"):
            st.image("Paper/Figures/calibration_plot.png", use_container_width=True)
        else:
            st.info("Calibration plot image not found in Paper/Figures/calibration_plot.png")

with tab3:
    st.markdown("<h3 style='color:#1e3d59;'>🔬 Explainable AI (Local Explanation)</h3>", unsafe_allow_html=True)
    st.write("Below is the local attribution of features contributing to the Logistic Regression model's prediction for this patient. Positive values push the risk score higher, while negative values reduce it.")
    
    if lr_model is not None and scaler is not None:
        # Calculate feature contributions for Logistic Regression
        # Contribution = scaled_feature * coefficient
        input_scaled = scaler.transform(input_df)[0]
        coefs = lr_model.coef_[0]
        contributions = input_scaled * coefs
        
        # Create a dataframe for plotting
        contrib_df = pd.DataFrame({
            'Feature': feature_names,
            'Attribution': contributions
        })
        
        # Sort by absolute attribution and take top 10
        contrib_df['Abs_Attribution'] = contrib_df['Attribution'].abs()
        top_contrib = contrib_df.sort_values(by='Abs_Attribution', ascending=False).head(12)
        
        # Plot
        fig, ax = plt.subplots(figsize=(10, 6))
        colors_att = ['#d62728' if x >= 0 else '#1f77b4' for x in top_contrib['Attribution']]
        sns.barplot(
            x='Attribution',
            y='Feature',
            data=top_contrib,
            palette=colors_att,
            ax=ax
        )
        ax.axvline(0, color='black', linewidth=1)
        ax.set_xlabel('Marginal Contribution to Logistic Regression log-odds', fontsize=11)
        ax.set_ylabel('Feature Name', fontsize=11)
        ax.grid(True, linestyle=':', alpha=0.5)
        st.pyplot(fig)
        
        st.caption("**Color Legend**: Red indicates the feature is elevating the patient's risk of gallstone disease, whereas Blue indicates the feature is protective / reducing the risk.")
