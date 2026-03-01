import requests

# Sample data for testing the /analyze endpoint
data = {
    "device_id": "D493",
    "device_type": "mri",
    "department": "ICU",
    "criticality_level": 3,
    "firmware_version": "v2.0",
    "cpu_usage_percent": 41.121555940988,
    "memory_usage_percent": 38.017316798916255,
    "disk_write_mb_per_min": 103.47476800765736,
    "disk_read_mb_per_min": 113.31302952096242,
    "process_spawn_count": 14,
    "file_rename_count": 39,
    "new_file_creation_count": 23,
    "file_entropy_avg": 5.791509269680069,
    "encrypted_extension_ratio": 0.3759678090647714,
    "outbound_traffic_mb": 106.94927049845988,
    "inbound_traffic_mb": 34.99751845103267,
    "unique_external_ips": 0,
    "dns_request_count": 63,
    "unusual_port_flag": 0,
    "privilege_escalation_flag": 0,
    "configuration_change_flag": 0,
    "antivirus_alert_flag": 0,
    "failed_auth_attempts": 7
}

# Send POST request
response = requests.post("http://127.0.0.1:8000/analyze", json=data)

# Print the response
print(response.json())
