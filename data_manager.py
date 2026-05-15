import pandas as pd
from config import DATA_FILES


def load_dataset(dataset_name):
    if dataset_name not in DATA_FILES:
        raise ValueError("Invalid dataset name.")
    return pd.read_csv(DATA_FILES[dataset_name], dtype=str)


def save_dataset(dataset_name, df):
    df.to_csv(DATA_FILES[dataset_name], index=False)


def find_by_patient_id(df, patient_id):
    return df[df["patient_id"].astype(str) == str(patient_id)]


def display_records(df, columns=None):
    if df.empty:
        print("No records found.")
        return

    if columns:
        print(df[columns].to_string(index=False))
    else:
        print(df.to_string(index=False))