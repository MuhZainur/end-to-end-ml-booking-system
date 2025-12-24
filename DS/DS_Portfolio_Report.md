# British Airways Data Science: Portfolio Report

## 1. Executive Summary
**Project Name:** Predictive Modeling for Flight Booking Completion
**Role:** Data Scientist
**Goal:** Build a robust, production-ready Machine Learning model to predict customer booking intent, overcoming significant class imbalance (15% conversion).
**Stack:** Python, Scikit-Learn, Imbalanced-Learn (SMOTE), MLflow, Random Forest.

---

## 2. The Challenge: "Finding the Needle in the Haystack"

The core challenge of this dataset was **Class Imbalance**. The majority of users (85%) browse without booking. A standard model trained on this data would simply predict "No Booking" every time and achieve 85% accuracy—which is **useless** for the business.

**Objective:**
We needed a model that prioritizes **Recall** (finding the actual bookers) while maintaining reasonable Precision, rather than optimizing for vanity metrics like raw accuracy.

---

## 3. Technical Approach & Pipeline Architecture

We engineered a sophisticated **Imbalanced-Learn Pipeline** to handle preprocessing and modeling in a single, deployable unit.

### A. Feature Engineering
*   **Categorical Encoding:** Leveraged `OrdinalEncoder` within a `ColumnTransformer` to handle high-cardinality features like `route` and `booking_origin`.
*   **Temporal Features:** Decomposed dates into `flight_day` and `flight_hour` to capture behavioral patterns.

### B. Handling Imbalance: SMOTE
*   **Synthetic Minority Over-sampling Technique (SMOTE):** Instead of simple duplication, we used SMOTE to generate synthetic examples of "Bookers" in the feature space.
*   **Integration:** Crucially, SMOTE was placed **inside the Cross-Validation pipeline**. This ensures synthetic data is *only* created from the Training fold, completely preventing **Data Leakage** into the Validation fold.

### C. Model Selection
*   **Algorithm:** **Random Forest Classifier**.
*   **Why?** Chosen for its resilience to noise, ability to handle non-linear relationships, and interpretability (Feature Importance).
*   **Hyperparameter Tuning:** Conducted `RandomizedSearchCV` to optimize `n_estimators`, `max_depth`, and `min_samples_split`.

---

## 4. Experiment Tracking with MLflow

To ensure reproducibility and professional standards, we integrated **MLflow** for experiment tracking.

*   **Remote Tracking:** All experiments were logged to a remote MLflow Tracking Server (GCP).
*   **Logged Metrics:** Precision, Recall, F1-Score, and AUC-ROC.
*   **Artifact Management:** The final pipeline was saved as a localized artifact, allowing the Backend engineering team to "pull" the model dynamically without manual file transfers.

---

## 5. Model Performance

| Metric | Score | Interpretation |
| :--- | :--- | :--- |
| **Accuracy** | 86% | The model remains robust overall. |
| **Precision (Class 1)** | ~0.53 | When it predicts "Book", it is correct about half the time. |
| **Recall (Class 1)** | ~0.76 | **Critical Success:** The model successfully captures 76% of all actual bookings. |
| **AUC-ROC** | 0.82 | Strong separability between classes. |

*Note: In a marketing context, High Recall is preferred. We'd rather send a discount to someone who might not book (False Positive) than miss someone who would (False Negative).*

---

## 6. Business Impact
This model acts as the "Engine" for a targeted intervention system:
1.  **Revenue Protection:** By identifying high-intent users who haven't paid yet, BA can send real-time reminders or incentives.
2.  **Cost Efficiency:** Marketing spend is redirected away from low-probability users (the "Browser" segment).

---
*Created by **[MuhZainur]** - Data Scientist & ML Engineer*
