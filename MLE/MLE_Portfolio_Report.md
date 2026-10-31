# British Airways ML Engineering: Portfolio Report

## 1. Executive Summary
**Project Name:** Enterprise-Grade Model Deployment System
**Role:** Machine Learning Engineer
**Goal:** Transition a static Data Science model into a scalable, high-availability web application with automated updates.
**Stack:** FastAPI, React (Vite), Docker, Render & Vercel, GitHub Actions.

---

## 2. System Architecture: "Beyond `model.predict()`"

A Data Science model is useless if it lives in a notebook. This project builds a Production Environment simulating a real-world enterprise setup.

### A. The Backend (Microservice)
*   **FastAPI Framework:** Chosen for its asynchronous capabilities (high concurrency) and automatic Swagger UI generation.
*   **Dynamic Model Loading:** Unlike traditional setups that "bake" the model into the Docker image, this service connects to a centralized **MLflow Model Registry**.
    *   *Benefit:* We can update the model version without rebuilding the Backend container.
*   **Pydantic Validation:** Strict type enforcement ensures that bad data (e.g., negative `flight_duration`) is rejected before reaching the model.

### B. The Frontend (Client)
*   **React + Vite:** A modern Single Page Application (SPA) offering a responsive user experience.
*   **British Airways Design System:** Implemented using **Tailwind CSS** to strictly adhere to corporate branding (Navy/Red/White), proving the ability to build user-centric internal tools.

---

## 3. DevOps & Containerization

To solve the "It works on my machine" problem, the entire stack is containerized.

*   **Docker Compose Orchestration:**
    *   **Service Isolation:** Frontend and Backend run in separate containers, communicating via an internal network.
    *   **Volume Mounting:** Securely injects Google Cloud Credentials (`gcs_key.json`) at runtime, ensuring no secrets are ever committed to the image.
*   **Optimization:**
    *   **Backend:** Uses `python:3.10-slim` for a minimal footprint.
    *   **Frontend:** Uses a **Multi-Stage Build** (Node Builder -> Lightweight Server) to keep the final image size under 50MB.

---

## 4. The "Holy Grail": Automated CI/CD & GitOps

This project implements a **Level 3 MLOps Pipeline**, automating the handover from Data Science to Engineering.

### The Problem
In many companies, Data Scientists email `.pkl` files to Engineers. This is slow, error-prone, and lacks version control.

### The Solution: Event-Driven GitOps
We built a pipeline `deploy_gcloud.yml` coupled with a Python controller `promote_model.py`:

1.  **Trigger:** A Data Scientist registers a new "Champion" model in MLflow.
2.  **Detection:** The `promote_model.py` script scans the registry for the best performing run.
3.  **GitOps Action:** The script **automatically commits** the new Run ID to the repository's `.env` config.
4.  **Deployment:** GitHub Actions detects the config change, rebuilds the Docker containers, and pushes the update to **Google Cloud Run**.

**Result:** Zero-touch deployment. The system heals and updates itself based on model performance data.

---

## 5. Security & Governance

*   **Secret Management:** No credentials exist in the code. All access keys are injected via environment variables or Docker volumes.
*   **Data Privacy:** `.gitignore` rules strictly prevent customer PII (datasets) from touching the version control system.

---
*Created by **[MuhZainur]** - Data Scientist & ML Engineer*
