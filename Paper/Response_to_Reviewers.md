# Response to Reviewers

**Manuscript Reference No.:** CCACTA-D-26-00706  
**Title:** Early Prediction of Gallstone Disease Using Validated Machine Learning Models on Bioimpedance and Laboratory Data  
**Journal:** *Clinica Chimica Acta*

Dear Editor-in-Chief Dr. William Clarke and the Editorial Board,

We would like to thank the reviewers for their constructive comments and suggestions, which have significantly helped us improve the quality, rigor, and clinical translational utility of our manuscript. 

We have revised our manuscript to address all comments. Most notably, we have:
1. Conducted a detailed cohort characterization and statistical test analysis (Table 2), revealing a significant distribution shift.
2. Performed a clean **cross-validation on the public cohort alone** and **external validation on the local Indonesian cohort** to address concerns of overfitting, reporting a specificity (True Negative Rate) of 35.0% to 53.1%.
3. Added **Calibration Curves** (Figure 9) and **Decision Curve Analysis (DCA)** (Figure 10) to demonstrate the clinical decision utility and screening threshold behavior.
4. Corrected mathematical notations, symbol omissions (such as $\kappa$ and $\alpha$ in the GFR formula), and validation inconsistencies in the text.

Below is our point-by-point response to each reviewer's comments.

---

### **Reviewer #2 Comments and Responses**

#### **Comment 1:** *It is unclear how early they can diagnose gallstone disease, compared to traditional methods.*
* **Response:** We have clarified this in the **Introduction** and **Discussion**. Traditional diagnostic methods (primarily abdominal ultrasonography) are typically diagnostic, ordered after a patient presents with symptoms (biliary colic, right upper quadrant pain). In contrast, our proposed model operates as a screening/risk-stratification tool using routine blood work and non-invasive bioimpedance. It is intended to be used in primary care or routine checkups to identify high-risk asymptomatic individuals *before* they develop symptoms or severe complications, allowing early referral for confirmatory imaging. 
* **Manuscript Revision:** See Section 1 (Introduction, Paragraphs 12, 17) and Section 4 (Discussion, Paragraph 3).

#### **Comment 2:** *About the data, a table showing demographic and clinical info should be provided.*
* **Response:** We agree. We have generated and inserted **Table 2** in Section 2.1 (Data Acquisition), showing detailed demographic and clinical characteristics for the Indonesian local cohort, the Turkish public UCI cohort, and the combined overall dataset, along with cohort-specific comparison statistics.
* **Manuscript Revision:** Table 2 has been added in Section 2.1.

#### **Comment 3:** *Demographic differences between the 2 cohorts should be studied. The manuscript currently risks substantial dataset heterogeneity and potential distribution shift. Without a clear characterization of both cohorts, it is difficult to judge generalizability.*
* **Response:** We thank the reviewer for this critical comment. We conducted independent t-tests for continuous variables and Chi-square tests for categorical variables to compare the two cohorts. The analysis reveals a substantial distribution shift (Table 2). The Indonesian cohort is significantly older (mean 60.46 vs. 48.07 years), lighter (weight 61.71 vs. 80.56 kg), shorter (height 161.22 vs. 167.16 cm), and has a lower BMI (23.58 vs. 28.88 kg/m²). GFR and total cholesterol also differ significantly. Furthermore, the local Indonesian cohort consists exclusively of healthy controls (0% disease prevalence), whereas the public cohort is balanced (161 cases, 158 controls). This creates cohort-specific confounding, which we now explicitly report and discuss in the revised manuscript.
* **Manuscript Revision:** Detailed text has been added in Section 2.1 (Data Acquisition) and Section 4 (Discussion, Paragraph 2) discussing this distribution shift and its implications for generalizability.

#### **Comment 4:** *There are concerns about data overfitting. The reported performances are exceptionally high given the modest dataset size, particularly for ANN, LSTM, and Random Forest models (AUC >0.97). Internal cross validation was performed, but there is no external cross validation.*
* **Response:** This is a crucial comment. We agree that the near-perfect cross-validation performance (~91% accuracy, AUC ~0.98) on the merged dataset was artificially inflated due to the models learning cohort-specific differences (batch effects) since all cases were Turkish and a major portion of controls were Indonesian. 
To address this, we conducted two additional validation experiments:
1. **UCI-Only CV**: 10-fold cross-validation on the public UCI cohort alone, restricting the feature space to the 24 common variables. Accuracy dropped to ~62.6% - 64.9%, and ROC-AUC dropped to ~0.654 - 0.703.
2. **External Validation**: Training on the public UCI cohort and testing on the local Indonesian cohort (controls only). The specificity (True Negative Rate) ranged from 34.69% (Random Forest) to 53.06% (ANN/MLP). 
We have fully integrated these realistic performance metrics into the Results and Discussion sections, framing the study as a lesson in cohort confounding and the necessity of external validation in clinical ML.
* **Manuscript Revision:** New subsection **"Cross-Cohort External Validation and Clinical Utility Analysis"** added to the Results, and a detailed limitations discussion added to Section 4.

#### **Comment 5:** *The rationale for using LSTM on non-sequential tabular clinical data is not adequately justified. Treating features as "sequences" is unconventional and may not provide meaningful temporal learning advantages.*
* **Response:** We completely agree with the reviewer. In our implementation, the feature vector was reshaped into a sequence of length 1 (time step = 1, input dimension = features). Under this setting, the LSTM is functionally equivalent to a feedforward neural network with gating but has no temporal or sequence-learning advantages. We have added a paragraph to the Discussion to clarify this, explaining that it was included for structural completeness in multi-model benchmarking rather than temporal modelling.
* **Manuscript Revision:** Section 4 (Discussion, Paragraph 3) now includes this clarification.

#### **Comment 6:** *If possible, the data and codes should be provided online and/or into a public repository.*
* **Response:** We confirm that all data and Python code for training, validation, plotting, and the web prototype are provided in a public GitHub repository https://github.com/zicohasan/Gallstone-Screening-ML.
* **Manuscript Revision:** Added a statement in Section 2.5 (Implementation).

#### **Comment 7:** *The manuscript repeatedly acknowledges ultrasonography as the current diagnostic gold standard, but they didn't compare their results with USG.*
* **Response:** We have clarified this in the **Discussion**. Abdominal ultrasonography (USG) has a diagnostic sensitivity of 90%–95% and specificity of ~95% but requires specialized equipment and radiologist interpretation. Our model achieves a lower performance but operates as a low-cost, automated screening/triage tool to prioritize symptomatic or high-risk patients for confirmatory USG. We do not aim to replace USG, but rather to optimize the referral path in resource-limited primary care clinics.
* **Manuscript Revision:** Section 4 (Discussion, Paragraph 3) updated to incorporate the USG comparison.

#### **Comment 8:** *Figure quality is relatively low, particularly confusion matrices and ROC curves. Higher-resolution figures are recommended.*
* **Response:** We have regenerated all figures in high-resolution (300 DPI) using modern, publication-quality styling. Specifically, we updated:
  * **Figure 6** (now including Panel A: ROC curves under CV, and Panel B: probability distributions on the external Indonesian cohort).
  * **Figure 5** (Confusion matrices grid in a clean, professional aesthetic).
* **Manuscript Revision:** Figure files have been updated in the manuscript submission package.

#### **Comment 9:** *In Section 2.4, the manuscript mentioned "10-fold cross-validation" but later described division into "five equal folds." This inconsistency should be corrected.*
* **Response:** We apologize for this typographical error. The cross-validation was division into ten equal folds. We have corrected the text to say "divided into ten equal folds... remaining nine trained the model."
* **Manuscript Revision:** Section 2.4 (Model Evaluation, Paragraph 1) corrected.

#### **Comment 10:** *Some equations could contain formatting problems and inconsistent notation; e.g., please double check equation (6).*
* **Response:** We have carefully reviewed Equation 6 (the GFR CKD-EPI formula) and the surrounding text. The Greek letters $\kappa$ and $\alpha$ were missing from the text description due to rendering errors. We have revised the text to explicitly define: $\kappa = 0.9$ for males or $0.7$ for females, and $\alpha = -0.411$ for males or $-0.329$ for females.
* **Manuscript Revision:** Section 2.2 (Equation 6 description text) updated.

---

### **Reviewer #3 Comments and Responses**

#### **Comment 3:** *The study apparently merge two datasets (one from UCI and other local dataset). The study did not mention how much records were added to the UCI dataset or the final number of records in the merged dataset. In the UCI dataset, there was apparently no missing values with a balanced dataset. In the merged dataset, it appears to have having missing values and has produced class imbalance. Provide details on the suitability of merging these two datasets.*
* **Response:** We have added these details to Section 2.1 (Data Acquisition). The merged dataset consists of 319 records from the Turkish public UCI dataset (161 cases, 158 controls) and 294 records from the Indonesian local hospital dataset (all 294 are controls). This increases the size from 319 to 613 records, but creates a class imbalance of 161 cases (26.3%) and 452 controls (73.7%). We have discussed the suitability and limitations of merging: while it increases the diversity and volume of controls, it introduces cohort confounding, which we have highlighted as a key limitation.
* **Manuscript Revision:** Section 2.1 (Data Acquisition) updated.

#### **Comment 4:** *Regarding the feature engineering, there were new defined features that were present in the local dataset, but not present in the UCI dataset such as De Ritis Ratio, Atherogenic Index, Co-morbidity score, TC/HDL ratio etc. Were these features also measured in the UCI dataset?*
* **Response:** Yes. All constituent variables used to calculate these engineered features (Total Cholesterol, HDL, LDL, Triglycerides, AST, ALT, Weight, Height, Lean Mass %, and comorbidities) were present in both datasets. Therefore, the engineered features were calculated identically for both cohorts using the exact same formulas. We have clarified this in the revised text.
* **Manuscript Revision:** Section 2.2 (Data Preprocessing and Feature Engineering, Paragraph 4) updated.

#### **Comment 5:** *Regarding the class imbalance, there is a need to quantify the imbalance.*
* **Response:** We have added this: the final combined dataset contains 161 cases (26.3%) and 452 controls (73.7%). Class imbalance was addressed during model training using SMOTE on the training folds only.
* **Manuscript Revision:** Added quantification to Section 2.2 (Preprocessing) and Results.

#### **Comment 6:** *On choosing the best model, need to specify the metrics that shall determine the best model and with which the explainability shall be applied. The results showed tuned random forest with the highest AUC but the SHAP and LIME were applied to tuned ANN.*
* **Response:** We have clarified our selection criteria. In a clinical screening scenario, Recall (Sensitivity) is prioritized to minimize false negatives (missed cases), balanced by ROC-AUC (discriminative capacity). While tuned Random Forest achieved a slightly higher AUC (0.982 vs 0.979) on the combined dataset, the tuned ANN achieved a superior recall and a more balanced profile. For the UCI-only CV, ANN achieved a comparable performance. We applied SHAP to the ANN to demonstrate how deep learning black-box predictions can be explained, making it a valuable addition to clinical decision support.
* **Manuscript Revision:** Section 2.4 and Section 3 updated to clarify model selection.

#### **Comment 7:** *As the model cannot yet be deployed for clinical scenario without external validation study, there is a need to justify the merging of the dataset. Why not use the UCI dataset for coming with the best model, enriched with the feature engineering approach and the externally apply the best model to the local dataset? As such the performance is still good, then perhaps it is time to recommend clinical deployment.*
* **Response:** We thank the reviewer for this excellent recommendation. We have implemented this exact validation path. Training on the UCI cohort (with engineered features) and testing on the Indonesian cohort yielded a specificity (TNR) of ~35.0% - 53.1%. The lower performance indicates that the model is not yet ready for immediate clinical deployment in Indonesia due to distribution shift. We have added this analysis and discussion, which significantly enhances the scientific value of our paper.
* **Manuscript Revision:** Added external validation results in Section 3 and Section 4.

---

### **Reviewer #4 Comments and Responses**

#### **Comment 1:** *Firstly, the application of ML and AI for gallstone disease prediction is not entirely novel. Thus, several recent studies have already explored AI/deep learning approaches for gallbladder disease prediction and diagnosis.*
* **Response:** We acknowledge that ML has been applied to gallstone prediction. We have revised the Introduction to highlight existing literature (e.g. Esen et al. 2024, Li et al. 2025) and clarify our specific contributions: (1) multi-model comparison including deep tabular models (TabNet) and recurrent networks (LSTM), (2) extensive clinically motivated feature engineering, (3) quantification of distribution shifts and cohort-confounding between Turkish and Indonesian clinical cohorts, and (4) translational calibration and decision curve analysis.
* **Manuscript Revision:** Section 1 (Introduction) updated.

#### **Comment 2:** *Another major criticism is the high risk of overfitting and limited generalizability. The reported performances (ROC-AUC approaching 0.98) are remarkably high considering the relatively small dataset size. Despite the use of cross-validation and SMOTE, the dataset remains limited and highly susceptible to overfitting. This issue is increased by the lack of external validation is a relevant issue of this study, since it limits comparability. Another major point regard the unclear translational utility, which is not discussed.*
* **Response:** We have addressed this by performing an external validation on the Indonesian cohort and cross-validation on the UCI cohort alone. The results show that the models indeed suffer from overfitting to cohort-specific features (batch effects) and distribution shift, leading to specificities of 35-53% on external controls. We have revised the Results and Discussion to present these findings transparently, and we discuss the exact reasons for the distribution shift (differences in age, BMI, and clinical priors between the two cohorts).
* **Manuscript Revision:** Results (new subsection) and Discussion updated.

#### **Comment 3:** *Although the models achieved high predictive performance, the manuscript does not clearly demonstrate how the proposed system would change real-world clinical decision-making. The study presents the model primarily as a screening tool, yet no clinically actionable risk thresholds, calibration analysis, or decision-curve analysis are provided.*
* **Response:** We thank the reviewer for this helpful suggestion. We have performed both **calibration curve analysis** (Figure 9) and **Decision Curve Analysis (DCA)** (Figure 10). The DCA demonstrates that the models provide a positive net benefit compared to default screening policies across a wide range of risk thresholds (15% to 75%), demonstrating clear clinical translational utility for patient prioritization.
* **Manuscript Revision:** Captions and descriptions for Figures 9 and 10 have been added to the Results and Discussion.

#### **Comment 4:** *As minor criticisms, introduction and discussion is too long and the reading of the manuscript is very difficult, being mostly treating the ML approach.*
* **Response:** We have streamlined the Introduction and Discussion, removing redundant text and improving readability. We have also simplified the explanations of the ML algorithms to focus on clinical relevance and interpretation.
* **Manuscript Revision:** Reorganized and shortened Sections 1 and 4 for improved clarity.

---

We believe that these revisions address all the reviewers' comments, resulting in a much stronger, scientifically transparent, and clinically useful manuscript.

Sincerely,

**Kirso & Dr. Zico Pratama Putra**  
Corresponding Author  
Faculty of Information Technology, Universitas Nusa Mandiri  
Email: zico.zpp@nusamandiri.ac.id
