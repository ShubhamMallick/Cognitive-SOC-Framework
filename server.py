"""
Flower Server for Federated Learning
Starts the server to aggregate model updates from clients.
"""

from flwr.server import start_server, ServerConfig

# Start the server
start_server(
    server_address="127.0.0.1:8080",
    config=ServerConfig(num_rounds=3)  # Number of FL rounds
)
