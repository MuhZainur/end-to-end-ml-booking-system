import mlflow
import mlflow.sklearn
import os
from dotenv import load_dotenv

load_dotenv()

class ModelLoader:
    def __init__(self):
        # Initial Setup (Will be overridden by load_model)
        self.tracking_uri = os.getenv("MLFLOW_TRACKING_URI")
        self.run_id = os.getenv("MLFLOW_RUN_ID")
        self.artifact_path = os.getenv("MODEL_ARTIFACT_PATH")
        self.model = None

    def _load_config(self):
        """Helper to load config from JSON or Env"""
        config = {
            "tracking_uri": os.getenv("MLFLOW_TRACKING_URI"),
            "active_run_id": os.getenv("MLFLOW_RUN_ID"),
            "artifact_path": os.getenv("MODEL_ARTIFACT_PATH")
        }
        
        # Priority 1: Check SAME directory (Docker Production)
        config_path_local = os.path.join(os.path.dirname(__file__), "model_version.json")
        # Priority 2: Check PARENT directory (Local Dev)
        config_path_dev = os.path.join(os.path.dirname(__file__), "..", "Config", "model_version.json")
        
        target_config_path = config_path_local if os.path.exists(config_path_local) else config_path_dev

        if os.path.exists(target_config_path):
            try:
                import json
                with open(target_config_path, 'r') as f:
                    json_config = json.load(f)
                    
                    # Merge JSON config (Priority)
                    if json_config.get("active_run_id"):
                        config["active_run_id"] = json_config["active_run_id"]
                    if json_config.get("tracking_uri") and not config["tracking_uri"]:
                        config["tracking_uri"] = json_config["tracking_uri"]
                    if json_config.get("artifact_path"):
                        config["artifact_path"] = json_config["artifact_path"]
                        
                print(f"📖 Loaded Configuration from {target_config_path}")
            except Exception as e:
                print(f"⚠️ Error reading model_version.json: {e}")
        return config

    def load_model(self):
        """
        Loads the model from MLflow.
        """
        try:
            # Debug Credentials
            gcs_creds = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
            print(f"🔑 GOOGLE_APPLICATION_CREDENTIALS Env: {gcs_creds}")
            
            # DEEP DEBUG: Check Directory Contents
            try:
                if gcs_creds:
                    secret_dir = os.path.dirname(gcs_creds)
                    print(f"📂 Checking directory: {secret_dir}")
                    if os.path.exists(secret_dir):
                        files = os.listdir(secret_dir)
                        print(f"📄 Files found in {secret_dir}: {files}")
                    else:
                        print(f"❌ Directory {secret_dir} does NOT exist! (Volume not mounted?)")
            except Exception as e:
                print(f"⚠️ Error listing secret dir: {e}")

            if gcs_creds and os.path.exists(gcs_creds):
                try:
                    with open(gcs_creds, 'r') as f:
                        content = f.read()
                        # Preview first 50 chars to avoid leaking full key but verify JSON
                        preview = content[:50] + "..." if len(content) > 50 else content
                        print(f"📄 Credential File Content Preview: {preview}")
                except Exception as read_err:
                    print(f"⚠️ Failed to read credential file: {read_err}")
            else:
                print("⚠️ Credential file does not exist or env var not set!")

            # Load configuration
            config = self._load_config()
            tracking_uri = config.get("tracking_uri")
            run_id = config.get("active_run_id")
            artifact_path = config.get("artifact_path")
            
            # Store for later use if needed
            self.tracking_uri = tracking_uri
            self.run_id = run_id
            self.artifact_path = artifact_path

            # Validate essential config
            if not tracking_uri:
                raise ValueError("Missing MLFLOW_TRACKING_URI in Env/Config")
            if not (run_id and artifact_path) and not (artifact_path and artifact_path.startswith("gs://")):
                raise ValueError("Missing MLFLOW_RUN_ID or MODEL_ARTIFACT_PATH in Env/Config, or a direct GCS path.")

            # Set tracking URI
            mlflow.set_tracking_uri(tracking_uri)
            print(f"📍 MLflow Tracking URI set to: {tracking_uri}")
            
            # Construct Model URI
            if artifact_path and artifact_path.startswith("gs://"):
                 # Direct GCS Path (Fix for 404 Registry Issue)
                model_uri = artifact_path
                print(f"🔗 Using Direct GCS Model URI: {model_uri}")
            elif run_id and artifact_path:
                # Standard MLflow Run Path
                model_uri = f"runs:/{run_id}/{artifact_path}"
                print(f"🔗 Using MLflow Run URI: {model_uri}")
            else:
                # This case should ideally be caught by the earlier validation
                raise ValueError("Could not construct model URI. Check run_id and artifact_path.")

            # Load the model
            print(f"⬇️ Attempting to download model from {model_uri}...")
            self.model = mlflow.sklearn.load_model(model_uri)
            print("✅ Model loaded successfully!")
            return self.model
            
        except Exception as e:
            print(f"❌ MLflow Load Failed: {e}")
            print("💡 Hint: If using Remote MLflow causing GCS Registry error, check your Google Cloud Credentials.")
            # Don't raise, allow app to start (fail-safe)
            self.model = None
            # Re-raise the exception to indicate failure to load model
            raise e

    def predict(self, input_df):
        if not self.model:
            raise Exception("Model not loaded. Call load_model() first.")
        
        prediction = self.model.predict(input_df)
        probability = self.model.predict_proba(input_df)
        return prediction[0], probability[0][1] # Return class and prob of class 1

# Global instance
model_loader = ModelLoader()
