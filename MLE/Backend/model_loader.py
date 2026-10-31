import os
import joblib
from dotenv import load_dotenv

load_dotenv()

class ModelLoader:
    def __init__(self):
        self.model = None
        self.model_source = None

    def _find_local_model(self):
        """Search for local serialized model file"""
        candidates = [
            os.path.join(os.path.dirname(__file__), "ba_booking_prediction_model.pkl"),
            os.path.join(os.getcwd(), "ba_booking_prediction_model.pkl"),
            os.path.join(os.getcwd(), "MLE", "Backend", "ba_booking_prediction_model.pkl"),
            os.path.join(os.path.dirname(__file__), "..", "..", "MLE", "Backend", "ba_booking_prediction_model.pkl"),
        ]
        for path in candidates:
            if os.path.exists(path):
                return os.path.abspath(path)
        return None

    def _load_config(self):
        """Helper to load config from JSON or Env (Legacy MLflow fallback)"""
        config = {
            "tracking_uri": os.getenv("MLFLOW_TRACKING_URI"),
            "active_run_id": os.getenv("MLFLOW_RUN_ID"),
            "artifact_path": os.getenv("MODEL_ARTIFACT_PATH")
        }
        
        config_path_local = os.path.join(os.path.dirname(__file__), "model_version.json")
        config_path_dev = os.path.join(os.path.dirname(__file__), "..", "Config", "model_version.json")
        target_config_path = config_path_local if os.path.exists(config_path_local) else config_path_dev

        if os.path.exists(target_config_path):
            try:
                import json
                with open(target_config_path, 'r') as f:
                    json_config = json.load(f)
                    if json_config.get("active_run_id"):
                        config["active_run_id"] = json_config["active_run_id"]
                    if json_config.get("tracking_uri") and not config["tracking_uri"]:
                        config["tracking_uri"] = json_config["tracking_uri"]
                    if json_config.get("artifact_path"):
                        config["artifact_path"] = json_config["artifact_path"]
            except Exception as e:
                print(f"⚠️ Error reading model_version.json: {e}")
        return config

    def load_model(self):
        """
        Loads the model: Priority 1 is local .pkl; Priority 2 is MLflow remote.
        """
        # 1. Try Local Model first
        local_model_path = self._find_local_model()
        if local_model_path:
            try:
                print(f"📦 Loading local production pipeline from: {local_model_path}")
                self.model = joblib.load(local_model_path)
                self.model_source = f"local:{local_model_path}"
                print("✅ Production Pipeline loaded successfully!")
                return self.model
            except Exception as e:
                print(f"⚠️ Failed to load local model: {e}")

        # 2. Legacy MLflow Fallback (if remote tracking server is available)
        try:
            import mlflow
            import mlflow.sklearn
            
            config = self._load_config()
            tracking_uri = config.get("tracking_uri")
            run_id = config.get("active_run_id")
            artifact_path = config.get("artifact_path")
            
            if tracking_uri and (run_id or (artifact_path and artifact_path.startswith("gs://"))):
                mlflow.set_tracking_uri(tracking_uri)
                if artifact_path and artifact_path.startswith("gs://"):
                    model_uri = artifact_path
                else:
                    model_uri = f"runs:/{run_id}/{artifact_path}"
                print(f"⬇️ Attempting to load model from MLflow: {model_uri}...")
                self.model = mlflow.sklearn.load_model(model_uri)
                self.model_source = f"mlflow:{model_uri}"
                print("✅ Model loaded successfully from MLflow!")
                return self.model
        except Exception as e:
            print(f"⚠️ MLflow Load skipped or unavailable: {e}")

        return self.model

    def predict(self, input_df):
        if not self.model:
            self.load_model()
            
        if self.model:
            try:
                prediction = self.model.predict(input_df)
                probability = self.model.predict_proba(input_df)
                return int(prediction[0]), float(probability[0][1])
            except Exception as e:
                print(f"⚠️ Model prediction encountered error, using heuristic fallback: {e}")

        # Fallback heuristic calculation if model not available
        score = 0.30
        try:
            if 'wants_extra_baggage' in input_df.columns and input_df['wants_extra_baggage'].iloc[0] == 1:
                score += 0.18
            if 'wants_in_flight_meals' in input_df.columns and input_df['wants_in_flight_meals'].iloc[0] == 1:
                score += 0.12
            if 'wants_preferred_seat' in input_df.columns and input_df['wants_preferred_seat'].iloc[0] == 1:
                score += 0.10
            if 'trip_type' in input_df.columns and input_df['trip_type'].iloc[0] == 'RoundTrip':
                score += 0.08
            if 'sales_channel' in input_df.columns and input_df['sales_channel'].iloc[0] == 'Internet':
                score += 0.05
        except Exception:
            pass

        score = min(max(score, 0.05), 0.95)
        pred = 1 if score >= 0.5 else 0
        return pred, float(round(score, 4))

# Global instance
model_loader = ModelLoader()
