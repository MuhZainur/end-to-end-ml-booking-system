import mlflow
import os
from dotenv import load_dotenv, set_key

import json

# Load Environment (for credentials if needed)
load_dotenv('MLE/Backend/.env')

MLFLOW_TRACKING_URI = "http://35.192.146.116:5000"
EXPERIMENT_NAME = "BA_Booking_RF_Remote_Tracked"
CONFIG_FILE_PATH = "MLE/Config/model_version.json"

def promote_latest_model():
    print(f"🔌 Connecting to MLflow: {MLFLOW_TRACKING_URI}")
    mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
    
    # 1. Get Experiment ID
    experiment = mlflow.get_experiment_by_name(EXPERIMENT_NAME)
    if not experiment:
        print(f"❌ Experiment '{EXPERIMENT_NAME}' not found!")
        return
    
    print(f"✅ Found Experiment ID: {experiment.experiment_id}")
    
    # 2. Find Best Run
    print("🔍 Searching for best run...")
    df_runs = mlflow.search_runs(
        experiment_ids=[experiment.experiment_id],
        filter_string="metrics.accuracy > 0.7",
        order_by=["metrics.accuracy DESC"],
        max_results=1
    )
    
    if df_runs.empty:
        print("⚠️ No suitable runs found to promote.")
        return

    best_run_id = df_runs.iloc[0].run_id
    best_accuracy = df_runs.iloc[0]["metrics.accuracy"]
    print(f"🏆 Best Run Found: {best_run_id} (Accuracy: {best_accuracy:.4f})")
    
    # 3. Read Current Config
    current_config = {}
    if os.path.exists(CONFIG_FILE_PATH):
        with open(CONFIG_FILE_PATH, 'r') as f:
            current_config = json.load(f)
            
    current_run_id = current_config.get("active_run_id")

    if best_run_id == current_run_id:
        print("⚡ Environment is already up-to-date. No changes made.")
    else:
        print(f"🔄 Promoting Model: {current_run_id} -> {best_run_id}")
        
        # Update Config
        current_config["active_run_id"] = best_run_id
        current_config["tracking_uri"] = MLFLOW_TRACKING_URI
        
        with open(CONFIG_FILE_PATH, 'w') as f:
            json.dump(current_config, f, indent=4)
            
        print("✅ model_version.json updated successfully!")
        
        # 4. GitOps: Auto-Commit & Push (If in CI)
        if os.getenv("GITHUB_ACTIONS") == "true":
            print("🤖 Detected CI Environment. Initiating GitOps Auto-Commit...")
            os.system('git config --global user.name "Model Promoter Bot"')
            os.system('git config --global user.email "bot@mlops.com"')
            os.system(f'git add {CONFIG_FILE_PATH}')
            os.system(f'git commit -m "🚀 Model Promo: Updated to Run ID {best_run_id}"')
            os.system('git push')
            print("✅ Changes pushed to repository. This will trigger a new Deploy Workflow.")
        else:
            print("🚀 ACTION REQUIRED: Run 'docker-compose up --build' (or git commit & push) to deploy.")

if __name__ == "__main__":
    promote_latest_model()
