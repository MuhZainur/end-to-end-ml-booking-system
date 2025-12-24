import mlflow
import mlflow.sklearn
import os
import sys
from dotenv import load_dotenv

# Force load .env from the current directory
load_dotenv()

tracking_uri = os.getenv("MLFLOW_TRACKING_URI")
run_id = os.getenv("MLFLOW_RUN_ID")
artifact_path = os.getenv("MODEL_ARTIFACT_PATH")

print(f"🔍 Debugging MLflow Connection...")
print(f"   URI: {tracking_uri}")
print(f"   Run ID: {run_id}")
print(f"   Artifact Path: {artifact_path}")

try:
    print("\n   [1] Setting Tracking URI...")
    mlflow.set_tracking_uri(tracking_uri)
    
    model_uri = f"runs:/{run_id}/{artifact_path}"
    print(f"   [2] Attempting to load model from: {model_uri}")
    
    model = mlflow.sklearn.load_model(model_uri)
    print("\n✅ Model loaded SUCCESSFULLY!")
    print(f"   Type: {type(model)}")
    
except Exception as e:
    print("\n❌ FAILED to load model.")
    print("   Error Details:")
    print(e)
    import traceback
    traceback.print_exc()
