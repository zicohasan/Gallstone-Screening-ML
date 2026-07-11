# Response to Reviewers - Round 2 Revisions

**Manuscript Reference No.:** CCACTA-D-26-00706  
**Title:** Early Prediction of Gallstone Disease Using Validated Machine Learning Models on Bioimpedance and Laboratory Data  
**Journal:** *Clinica Chimica Acta*

Dear Editor-in-Chief Dr. William Clarke and the Editorial Board,

We thank the Editor and the Reviewers for their valuable comments and suggestions in this second round of review. We have revised our manuscript to address all comments. 

In this revision, we have:
1. Conducted a **collinearity diagnostic (VIF)** (Table 3) and added a discussion on how collinearity is managed.
2. Conducted a formal **Feature Ablation Study** (Table 4) to isolate the contribution of our feature engineering.
3. Quantified the **missingness** and **SMOTE class distributions** explicitly.
4. Formulated the contributions as bullet points and corrected the caption typo in Figure 1.
5. Provided detailed clinical and mathematical justifications for our choice of SMOTE, Random Search, and SHAP over alternatives.

Below is our point-by-point response to each reviewer's comments.

---

### **Reviewer #5 Comments and Responses**

#### **Comment 1:** *The claim of "validated" models is overstated. Validation on a single, modestly sized, merged dataset does not constitute robust validation.*
* **Response:** We agree with the reviewer that "validation" on a single cohort is a limitation. We have revised the manuscript to tone down this claim, explicitly framing our work as a feasibility and exploratory study. We discuss that while we perform cross-cohort validation, true clinical validation requires prospective multi-center studies.
* **Manuscript Revision:** Section 1 (Introduction, last paragraph) and Section 4 (Discussion, Limitations) have been updated to reflect this change in terminology.

#### **Comment 2:** *The novelty is incremental: prior work on the same UCI dataset (Esen et al., 2024; Li et al., 2025) already reported AUCs >0.90. The authors improve upon this via tuning, but the core dataset remains largely the same.*
* **Response:** We acknowledge that previous studies used the Esen et al. dataset. However, our study provides distinct novelties: (1) we study the impact of cross-cohort dataset integration (Turkish public dataset + Indonesian local dataset), revealing significant distribution shifts (Table 2); (2) we perform a clean external validation on Indonesian controls showing the generalizability limits under distribution shifts (TNR of 35-53%); and (3) we introduce Decision Curve Analysis (DCA) and calibration checks to evaluate the model's translational screening utility.
* **Manuscript Revision:** Re-emphasized these points in Section 1 (Introduction) and Section 4 (Discussion).

#### **Comment 3:** *The local dataset is poorly described; its size, missingness, and contribution to model improvement are not quantified separately.*
* **Response:** We have added a detailed description of the local Indonesian cohort in Section 2.1. The local cohort consists of 294 records (all healthy controls, $y=0$). The missingness in the raw local dataset before imputation has been quantified: Uric Acid (17.0%), Anti-HIV (16.3%), Anti-HCV (3.7%), NLR (2.0%), and WBC (2.0%); other parameters had less than 1% missingness.
* **Manuscript Revision:** Section 2.1 (Data Acquisition) updated.

#### **Comment 4:** *Sample size: The final merged dataset size is not clearly stated. The UCI component has 319 records; the local contribution is undisclosed. This is a major omission, as model complexity (especially LSTM and TabNet) far exceeds the effective sample size, raising serious overfitting concerns.*
* **Response:** We apologize for this omission. The final merged dataset consists of 613 records: 319 records from the public UCI cohort (161 cases, 158 controls) and 294 records from the Indonesian local cohort (all controls). This results in 161 cases (26.26%) and 452 controls (73.74%). We have made this explicit in the text and discussed how the small sample size relative to model complexity (specifically for LSTM and TabNet) represents an overfitting risk, which is why we regularized these models using dropout and early stopping.
* **Manuscript Revision:** Section 2.1 (Data Acquisition) and Section 4 (Discussion, Limitations).

#### **Comment 5:** *SMOTE application is applied only to training folds, which is correct, but the authors do not report the degree of imbalance before SMOTE, nor the number of synthetic samples generated. This is essential for reproducibility and for interpreting recall improvements.*
* **Response:** We have added these details. In the cross-validation on the public UCI dataset, the original distribution before SMOTE is 158 controls (49.5%) vs. 161 cases (50.5%), requiring negligible oversampling. In the combined dataset cross-validation, the training set has an average imbalance of ~407 controls vs. ~145 cases per fold; SMOTE generates approximately 262 synthetic cases per fold to achieve a balanced 50:50 ratio (~407 controls vs. ~407 cases) for model training, without modifying the test folds.
* **Manuscript Revision:** Section 2.2 (Data Preprocessing, Paragraph 3) and Results.

#### **Comment 6:** *Feature overlap and multicollinearity: Many engineered features are mathematically derived from raw variables (e.g., BMI, TBW, LM%, TBFR%, body fat/water ratio). This introduces high multicollinearity, which can inflate variance in linear models and obscure SHAP attributions. No collinearity diagnostics (e.g., VIF) are reported.*
* **Response:** We thank the reviewer for this excellent methodological point. We computed the Variance Inflation Factor (VIF) for all features after standardization (Table 3). As expected, deterministic features (such as weight, lean mass %, TC/HDL ratio, and Atherogenic Index) exhibit infinite (inf) or very high VIFs. We have added a new subsection detailing these VIF diagnostics and discussed how this multicollinearity is handled: (1) using L2 regularization (Ridge) in Logistic Regression to stabilize coefficients, (2) using tree-based ensembles which are immune to multicollinearity for prediction, and (3) acknowledging that it makes individual SHAP attributions more sensitive to local correlations.
* **Manuscript Revision:** Section 2.2 (new subsection: **"Collinearity Diagnostics and Multicollinearity Mitigation"**) and **Table 3** have been added.

#### **Comment 7:** *LSTM for tabular data: Treating tabular features as a sequence lacks biological or clinical justification. This is a methodological gimmick rather than a principled choice, and the authors do not justify why an LSTM would be appropriate for non-sequential data.*
* **Response:** We agree with the reviewer. Reshaping static patient features into a sequence of length 1 is unconventional and acts purely as a feedforward layer with gate controls without modeling actual temporal patterns. We have revised the Discussion to clarify this, framing the LSTM primarily as a baseline comparison for recurrent neural networks on tabular representations rather than a clinically justified temporal model.
* **Manuscript Revision:** Section 4 (Discussion, Paragraph 3).

#### **Comment 8:** *Inconsistent numbers: In the abstract, ANN achieves 91.19% accuracy and 95.65% recall; in the results, LSTM is said to have 91.52% accuracy. Which model is recommended? The authors favor ANN, but the rationale is unclear.*
* **Response:** We have clarified our recommendation and unified the numbers to prevent confusion. Although the tuned LSTM achieved a slightly higher nominal accuracy (91.52% vs. 91.19% for ANN) under combined CV, we recommend the **tuned ANN** because: (1) it achieves the highest recall (95.65%), which is critical in clinical screening to minimize false negatives (missed diagnoses); and (2) the LSTM uses an unconventional sequence length of 1 on static data, whereas the ANN is a standard, principled feedforward model.
* **Manuscript Revision:** Section 3 (Results) and Section 4 (Discussion).

#### **Comment 9:** *No comparison with prior models on the same test set. The authors claim improvement over ~85% benchmarks, but they do not re-run Esen et al.'s model on their merged dataset to provide a fair comparison.*
* **Response:** We have clarified this. Esen et al.'s original accuracy (~85.4%) was achieved using Gradient Boosting on a larger set of 39 features (including CRP and Vitamin D, which were unavailable in our local cohort and thus excluded). When we re-run Gradient Boosting (XGBoost/LightGBM) on the public dataset with the restricted 24 common features, the accuracy drops to ~62.6% - 63.3%. This shows that the performance drop is due to feature restriction rather than model degradation, and highlights that our engineered features help recover this loss.
* **Manuscript Revision:** Section 3 (Results) and Section 4 (Discussion).

#### **Comment 10:** *Local dataset performance is not isolated. We have no idea whether the performance gains come from the local data, the engineering, or the tuning.*
* **Response:** We have conducted a formal **Feature Ablation Study** on the public cohort (Table 4) to isolate these effects. For Logistic Regression, the baseline (17 raw features) has a mean ROC-AUC of 0.661. Adding Stage 1 features (TBW, GFR, BMI) improves the AUC to 0.700 (+3.9%), and adding Stage 2 features (lipid ratios) further improves it to 0.703 (+4.2%). For Random Forest, adding Stage 1 & 2 features improves the AUC from 0.673 to 0.678. This demonstrates that our clinical feature engineering isolates clear performance improvements.
* **Manuscript Revision:** Section 3 (new subsection: **"Feature Ablation Study"**) and **Table 4** have been added.

#### **Comment 11:** *SHAP for ANN: The authors use SHAP for ANN, but DeepSHAP or KernelSHAP approximations are not validated for stability. SHAP values for neural networks can be unstable; no sensitivity analysis is provided.*
* **Response:** We acknowledge this risk. To ensure the stability of SHAP values for our recommended MLP/ANN model, we utilized KernelSHAP with a high background sample count ($N_{samples} = 500$) and verified the consistency of the feature rankings across different validation folds, showing that the top five features (Gender, TBW, Hemoglobin, BMI, lipid ratios) remained stable. We have documented this sensitivity check.
* **Manuscript Revision:** Section 2.4 (Interpretability Analysis, Paragraph 2).

#### **Comment 12:** *The authors repeatedly use language implying causality ("risk drivers," "dominant contributors"), but this is a cross-sectional prediction study. SHAP identifies associations, not causal effects.*
* **Response:** We apologize for this oversight. We have carefully revised the manuscript to remove causal language, replacing terms like "risk drivers" or "causes" with associative terms such as "predictive factors," "associated risk markers," or "model feature attributions."
* **Manuscript Revision:** Revised throughout the manuscript.

#### **Comment 13:** *The claim that the tool can "reduce diagnostic delays and complications" is speculative and unsupported by any prospective or implementation data.*
* **Response:** We agree. We have toned down this claim, stating that the model has *potential* to assist in screening but that prospective clinical implementation studies are required to verify any reduction in diagnostic delays or complications.
* **Manuscript Revision:** Abstract, Introduction, and Future Works have been revised.

#### **Comment 14:** *The comparison with imaging-based DL models (90-99% accuracy) is misleading; those models are diagnostic, not screening, and operate on different gold standards.*
* **Response:** We have revised the discussion. We now explicitly state that imaging-based DL models are diagnostic tools designed for confirmation, whereas our model is designed strictly as a low-cost, automated precursor screening tool.
* **Manuscript Revision:** Section 4 (Discussion, Paragraph 3).

---

### **Reviewer #6 Comments and Responses**

#### **Comment 1:** *Figure 1 contains a typographical error. "Hapley Additive exPlanations (SHAP)" should be corrected to "Shapley Additive exPlanations (SHAP)."*
* **Response:** We have corrected this typographical error in the Figure 1 caption and text.
* **Manuscript Revision:** Figure 1 caption corrected.

#### **Comment 2:** *The main contributions of the manuscript should be presented as bullet points for better clarity.*
* **Response:** We agree. The main contributions of this work have been reformatted as a clear bulleted list in the Introduction.
* **Manuscript Revision:** Section 1 (Introduction, last paragraph).

#### **Comment 3:** *How clinically realistic are the synthetic samples generated using SMOTE for gallstone disease prediction? The authors should provide justification that the interpolated feature space preserves medical plausibility and does not introduce biologically inconsistent patient profiles.*
* **Response:** We have added a justification in Section 2.2. SMOTE performs local linear interpolation between a patient and their nearest neighbors in a standardized continuous physiological feature space. Because metabolic variables (lipids, BMI, body water) naturally exhibit high correlation, local interpolation ensures that synthetic samples fall within a continuous risk region, preserving clinical associations (such as high BMI correlating with elevated body fat ratio) and avoiding medically inconsistent profiles (such as extremely high weight coupled with extremely low BMI).
* **Manuscript Revision:** Section 2.2 (Preprocessing, Paragraph 3) updated.

#### **Comment 4:** *The authors should clarify how the final feature set was determined after dataset integration and whether the exclusion of any features may have affected the model's predictive performance.*
* **Response:** We have clarified this in Section 2.1. The final feature set was restricted to the 24 common variables present in both cohorts. Features unique to the public dataset (like CRP and Vitamin D) were excluded to allow cohort integration. We explicitly report that this exclusion caused a drop in nominal model performance (from ~85% to ~63% accuracy on the public cohort), which represents a trade-off: a lower accuracy in exchange for a model that can be deployed using only basic, low-cost screening parameters.
* **Manuscript Revision:** Section 2.1 (Data Acquisition) updated.

#### **Comment 5:** *The authors should justify the choice of Random Search over other hyperparameter optimization methods, such as Bayesian optimization, Grid Search, or Optuna.*
* **Response:** We have added a justification. Random Search is computationally efficient, avoids the grid-alignment bias of Grid Search, and is highly robust in non-convex loss landscapes (avoiding premature convergence in local minima compared to Bayesian optimization during early exploration), making it a standard and reproducible baseline for benchmarking.
* **Manuscript Revision:** Section 2.3 (Model Development) updated.

#### **Comment 6:** *Authors should justify the choice of SHAP over other explainability methods such as LIME.*
* **Response:** We have added this justification. Unlike LIME, which fits a local surrogate model on perturbed samples (leading to high instability and sensitivity to perturbation scale), SHAP is uniquely grounded in cooperative game theory, ensuring that the attributions satisfy mathematical properties of local accuracy, consistency, and missingness, which are critical for clinical safety and trust.
* **Manuscript Revision:** Section 2.4 (Interpretability Analysis) updated.

#### **Comment 7:** *The comparative analysis is limited. Authors should include a more comprehensive comparison with relevant previous studies and present the results in a comparison table for better clarity and readability.*
* **Response:** We agree. We have generated and added **Table 5** in the Results section, comparing our study with other publications on the Esen et al. dataset (Esen et al. 2024, Li et al. 2025, Chakraborty & Mukherjee 2025) in terms of features, validation, tuning, and results.
* **Manuscript Revision:** **Table 5** and accompanying text have been added to the Results.

---

We believe that these additions and revisions fully address the reviewers' comments, resulting in a much stronger, scientifically transparent, and clinically useful manuscript.

Sincerely,

**Kirso & Dr. Zico Pratama Putra**  
Corresponding Author  
Faculty of Information Technology, Universitas Nusa Mandiri  
Email: zico.zpp@nusamandiri.ac.id
