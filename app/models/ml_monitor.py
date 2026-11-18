import os
import joblib
import time
from typing import Dict, Any, Tuple, Optional, List
import numpy as np
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
import sklearn
from app.config import settings

class ClassicalMLMonitor:
    def __init__(self, random_seed: int = 42):
        self.random_seed = random_seed
        self.model: Optional[RandomForestClassifier] = None
        self.feature_names: List[str] = []
        self.current_version: str = "v1.0.0"
        self.reference_data: Dict[str, np.ndarray] = {}

    def train_baseline(self, n_estimators: int = 50, max_depth: int = 5) -> Dict[str, Any]:
        """
        Train reproducible baseline model.
        Conforms to FR-05, NFR-04, TC-05, TC-16.
        """
        np.random.seed(self.random_seed)
        data = load_breast_cancer()
        # Use first 6 numerical features for crisp monitoring demonstration
        X = data.data[:, :6]
        y = data.target
        self.feature_names = [f"feat_{name.replace(' ', '_')}" for name in data.feature_names[:6]]

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.25, random_state=self.random_seed, stratify=y
        )

        clf = RandomForestClassifier(
            n_estimators=n_estimators,
            max_depth=max_depth,
            random_state=self.random_seed
        )
        clf.fit(X_train, y_train)
        self.model = clf

        preds = clf.predict(X_test)
        probs = clf.predict_proba(X_test)[:, 1]

        acc = float(accuracy_score(y_test, preds))
        prec = float(precision_score(y_test, preds))
        rec = float(recall_score(y_test, preds))
        f1 = float(f1_score(y_test, preds))
        auc = float(roc_auc_score(y_test, probs))

        # Store baseline reference data
        self.reference_data = {
            self.feature_names[i]: X_train[:, i] for i in range(len(self.feature_names))
        }

        # Save model artifact
        artifact_path = os.path.join(settings.MODEL_REGISTRY_DIR, f"baseline_rf_{self.current_version}.joblib")
        joblib.dump(clf, artifact_path)

        metadata = {
            "model_type": "Classical_RandomForest",
            "model_version": self.current_version,
            "random_seed": self.random_seed,
            "hyperparameters": {
                "n_estimators": n_estimators,
                "max_depth": max_depth
            },
            "metrics": {
                "accuracy": round(acc, 4),
                "precision": round(prec, 4),
                "recall": round(rec, 4),
                "f1_score": round(f1, 4),
                "roc_auc": round(auc, 4)
            },
            "environment": {
                "sklearn_version": sklearn.__version__,
                "numpy_version": np.__version__
            },
            "artifact_path": artifact_path,
            "timestamp": time.time()
        }
        return metadata

    def predict(self, features: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        if self.model is None:
            self.train_baseline()
        preds = self.model.predict(features)
        probs = self.model.predict_proba(features)
        return preds, probs

    def get_model_info(self) -> Dict[str, Any]:
        """Return rich metadata, actual feature importances, and dataset descriptions."""
        if self.model is None:
            self.train_baseline()
        importances = getattr(self.model, "feature_importances_", np.ones(len(self.feature_names)) / len(self.feature_names))
        total_imp = float(np.sum(importances)) if np.sum(importances) > 0 else 1.0
        
        feature_importance_list = []
        for i, name in enumerate(self.feature_names):
            imp_val = float(importances[i])
            pct_val = (imp_val / total_imp) * 100.0
            feature_importance_list.append({
                "feature": name,
                "importance": round(imp_val, 4),
                "percentage": round(pct_val, 2),
                "rank": 0 # to be sorted
            })
        feature_importance_list.sort(key=lambda x: x["importance"], reverse=True)
        for idx, item in enumerate(feature_importance_list):
            item["rank"] = idx + 1

        ref_stats = {}
        for name, arr in self.reference_data.items():
            ref_stats[name] = {
                "mean": round(float(np.mean(arr)), 4),
                "std": round(float(np.std(arr)), 4),
                "min": round(float(np.min(arr)), 4),
                "max": round(float(np.max(arr)), 4),
                "p25": round(float(np.percentile(arr, 25)), 4),
                "p50": round(float(np.percentile(arr, 50)), 4),
                "p75": round(float(np.percentile(arr, 75)), 4),
                "sample_count": len(arr)
            }

        return {
            "model_type": "Classical_RandomForest",
            "algorithm": "Scikit-Learn RandomForestClassifier",
            "model_version": self.current_version,
            "feature_names": self.feature_names,
            "feature_importances": feature_importance_list,
            "n_features": len(self.feature_names),
            "hyperparameters": {
                "n_estimators": getattr(self.model, "n_estimators", 50),
                "max_depth": getattr(self.model, "max_depth", 5),
                "random_state": self.random_seed
            },
            "dataset_info": {
                "name": "Breast Cancer Wisconsin Diagnostic Benchmark",
                "description": "Standard binary classification dataset tracking 6 core morphological cellular risk features.",
                "target_classes": {"0": "Malignant", "1": "Benign"},
                "num_reference_samples": len(next(iter(self.reference_data.values()))) if self.reference_data else 0
            },
            "reference_stats": ref_stats
        }

ml_monitor = ClassicalMLMonitor()

