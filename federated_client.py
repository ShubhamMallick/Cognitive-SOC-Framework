"""
Federated Learning Client for Anomaly Detection
Uses Flower (flwr) to participate in federated updates for RF/IF models.
This is optional and does not disrupt core functionality.
"""

import flwr as fl
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier, IsolationForest
from sklearn.metrics import accuracy_score

# Simulated local data (in real setup, use organization's data)
def load_local_data():
    # Placeholder: Load local dataset
    # In production, load organization's logs
    X = np.random.rand(100, 23)  # 100 samples, 23 features
    y = np.random.randint(0, 2, 100)  # Binary labels
    return X, y

class AnomalyDetectionClient(fl.client.NumPyClient):
    def __init__(self):
        self.rf = RandomForestClassifier(n_estimators=100, random_state=42)
        self.iso = IsolationForest(random_state=42)
        X, y = load_local_data()
        self.X, self.y = X, y
        self.rf.fit(X, y)  # Initial local training
        self.iso.fit(X)

    def get_parameters(self, config):
        # Return numerical model parameters as ndarrays (avoid object types)
        rf_params = [self.rf.n_estimators, self.rf.random_state]
        iso_params = [self.iso.n_estimators, self.iso.random_state]
        return [np.array(rf_params), np.array(iso_params)]

    def set_parameters(self, parameters):
        # Update local models with aggregated parameters
        rf_params, iso_params = parameters
        # Simplified: Update random_state or key params
        self.rf.set_params(random_state=int(rf_params[0]))
        self.iso.set_params(random_state=int(iso_params[0]))

    def fit(self, parameters, config):
        self.set_parameters(parameters)
        # Local training on local data
        self.rf.fit(self.X, self.y)
        self.iso.fit(self.X)
        return self.get_parameters(config), len(self.X), {}

# Start FL client (run in background or separately)
if __name__ == "__main__":
    client = AnomalyDetectionClient()
    fl.client.start_client(server_address="127.0.0.1:8080", client=client.to_client())
