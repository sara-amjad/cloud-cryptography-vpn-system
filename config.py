DATA_FILES = {
    "PMD": "data/PMD.csv",
    "PAD": "data/PAD.csv",
    "PFD": "data/PFD.csv"
}

PROTECTED_COLUMNS = {
    "PMD": [
        "disease_diagnosis",
        "heart_rate",
        "oxygen_level",
        "blood_pressure",
        "medication",
        "doctor_notes"
    ],
    "PAD": [
        "patient_name",
        "age",
        "ward_number",
        "registration_type",
        "discharge_status"
    ],
    "PFD": [
        "service_type",
        "total_bill",
        "payment_status",
        "insurance_provider",
        "claim_status",
        "transaction_id"
    ]
}

HASH_COLUMNS = {
    "PMD": ["patient_id"] + PROTECTED_COLUMNS["PMD"],
    "PAD": ["patient_id"] + PROTECTED_COLUMNS["PAD"],
    "PFD": ["patient_id"] + PROTECTED_COLUMNS["PFD"]
}

CERT_FILES = {
    "ca_cert": "certs/ca.crt",
    "client_cert": "certs/ashn_client.crt",
    "client_private_key": "certs/ashn_client.key"
}