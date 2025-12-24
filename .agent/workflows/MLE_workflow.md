---
description: Machine Learning Engineering / Deployment Workflow
---

1.  **Containerize**:
    Update `MLE/Dockerfile` if needed.
    Build Docker image:
    ```powershell
    docker build -t ba-model:latest -f MLE/Dockerfile .
    ```
2.  **Test API**:
    Run the application (`MLE/main.py`):
    ```powershell
    python MLE/main.py
    ```
    Test endpoints using curl or Postman.
3.  **Deploy**:
    Push to registry or deploy to target environment.
