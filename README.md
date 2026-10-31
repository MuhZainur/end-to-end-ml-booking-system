# British Airways (BA) - Customer Booking Intelligence ✈️

[![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white)]()
[![React](https://img.shields.io/badge/Frontend-React-61DAFB?style=flat-square&logo=react&logoColor=black)]()
[![Docker](https://img.shields.io/badge/Deployment-Docker%20%2B%20GCP-4285F4?style=flat-square&logo=google-cloud&logoColor=white)]()

**🔴 LIVE DEMO:**
*   **Frontend Dashboard:** [Click to Open App 🚀](https://ba-booking-predictor.vercel.app/)
*   **Backend API (Swagger):** [Swagger UI 📄](https://end-to-end-ml-booking-system.onrender.com/docs)

An End-to-End Machine Learning Solution to predict customer booking intent and optimize revenue strategies. Built for the modern enterprise stack, transforming raw flight data into a deployed, scalable predictive AI.

---

## 🏗️ Architecture Overview

This project simulates a real-world Machine Learning Engineering workflow, executed in three professional phases:

### Phase 1: Data Analytics (DA) 📊
*   **Goal:** Uncover behavioral patterns and strategic insights from raw booking data.
*   **Analysis:** Statistical testing (Chi-Square), Conversion Funnel Analysis, and Customer Segmentation.
*   **Deliverable:** `DA/DA_Portfolio_Report.md`.

### Phase 2: Data Science (DS) 🧠
*   **Goal:** Engineer a robust predictive model for booking completion.
*   **Model:** **Random Forest Classifier** (Optimized for Imbalanced Data).
*   **Techniques:** SMOTE (Synthetic Minority Over-sampling), Pipeline Architecture, and Feature Engineering.
*   **Deliverable:** `DS/Data_Science_BA_Classification.ipynb`.

### Phase 3: ML Engineering (MLE) ⚙️
*   **Goal:** Deploy the model into a production-grade application.
*   **Backend:** **FastAPI** service that dynamically fetches the latest model from a remote MLflow Tracking Server.
*   **Frontend:** **React** (Vite + Tailwind) dashboard for business users to simulate customer scenarios.
*   **Authentication:** Secure Google Cloud Storage (GCS) integration for artifact retrieval.

### Phase 4: DevOps & Deployment 🐳
*   **Containerization:** Full Docker support for both services.
*   **Orchestration:** `docker-compose` for one-click local deployment.
*   **CI/CD Logic:** Pull-based Model Deployment (Backend automatically loads strictly versioned models).

---

## 💻 Tech Stack

| Component | Technologies |
| :--- | :--- |
| **Data Science** | Python 3.10, Scikit-Learn, Imbalanced-Learn, Pandas, MLflow |
| **Backend API** | FastAPI, Uvicorn, Pydantic, GCS Auth |
| **Frontend UI** | React.js, Vite, Tailwind CSS, Axios |
| **Infrastructure** | Docker, Docker Compose, Google Cloud Storage |

---

## 🚀 How to Run (Docker)

The entire application can be launched with a single command using Docker Compose.

### Prerequisites
*   Docker & Docker Compose installed.
*   **Service Account Key**: Place your `gcs_key.json` in `MLE/Backend/` (Required for GCS Model Access).

### Steps
1.  **Clone the Repository**
    ```bash
    git clone https://github.com/YourUsername/BA_Booking_Prediction.git
    cd BA_Booking_Prediction
    ```

2.  **Launch Application**
    ```bash
    cd MLE
    docker-compose up --build
    ```

3.  **Access Services**
    *   **Web Dashboard:** [http://localhost:3000](http://localhost:3000)
    *   **API Docs (Swagger):** [http://localhost:8000/docs](http://localhost:8000/docs)


---

## 🚀 Live Deployment (Google Cloud Run)

This project is deployed manually to Google Cloud Platform using Docker containers and Cloud Run.

**Deployment Method:** Manual Docker Push (CI/CD under IAM security review)

### Prerequisites for Cloud Deployment
*   Google Cloud Project with enabled APIs: Cloud Run, Artifact Registry, Secret Manager
*   Service Account with IAM roles: Storage Admin, Artifact Registry Writer, Cloud Run Admin
*   Remote MLflow Tracking Server
*   Google Cloud Storage bucket for model artifacts

> **Note:** The `.github/workflows/deploy_gcloud.yml.disabled` file contains the full CI/CD configuration for reference. Additional IAM permissions are required for automated deployment.

---

## 📂 Project Structure

```
├── DS/                   # Phase 1: Data Science
│   └── Data_Science_BA_Classification.ipynb
├── MLE/                  # Phase 2 & 3: Deployment
│   ├── Backend/          # FastAPI App
│   │   ├── Dockerfile
│   │   ├── main.py
│   │   ├── model_loader.py
│   │   └── requirements.txt
│   ├── Frontend/         # React App
│   │   ├── Dockerfile
│   │   └── src/
│   ├── docker-compose.yml
│   └── MLE_Portfolio_Report.md
└── README.md             # Project Documentation
```

---

*Created by **[MuhZainur]** - Data Scientist & ML Engineer*
