import time
import pandas as pd

from config import DATA_FILES
from data_manager import load_dataset, save_dataset, find_by_patient_id, display_records
from crypto_manager import encrypt_row, decrypt_row, preview_decrypt_row
from cert_verifier import verify_certificate
from logger import log_event


def slow_print(message, delay=0.6):
    print(message)
    time.sleep(delay)


def dataset_choice_menu():
    print("\nSelect Dataset")
    print("1. PMD")
    print("2. PAD")
    print("3. PFD")
    print("4. ALL")

    choice = input("Enter choice: ").strip()

    mapping = {
        "1": "PMD",
        "2": "PAD",
        "3": "PFD",
        "4": "ALL"
    }
    return mapping.get(choice)


def single_or_all_dataset_choice_menu():
    print("\nSelect Dataset")
    print("1. PMD")
    print("2. PAD")
    print("3. PFD")
    print("4. ALL")
    print("5. Back")

    choice = input("Enter choice: ").strip()

    mapping = {
        "1": "PMD",
        "2": "PAD",
        "3": "PFD",
        "4": "ALL",
        "5": "BACK"
    }
    return mapping.get(choice)


def show_sample_change(before_row, after_row, dataset_name):
    print("\nSample Record View")
    print("------------------")

    preview_cols = [col for col in before_row.index[:6]]

    before_df = pd.DataFrame([before_row[preview_cols]])
    after_df = pd.DataFrame([after_row[preview_cols]])

    print("\nBefore")
    print(before_df.to_string(index=False))

    print("\nAfter")
    print(after_df.to_string(index=False))

    print(f"\nDataset: {dataset_name}")
    print(f"Current status: {after_row.get('enc_status', 'unknown')}")
    print(f"Algorithm: {after_row.get('enc_algorithm', 'unknown')}")


def encrypt_flow():
    dataset_choice = dataset_choice_menu()
    if not dataset_choice:
        print("Invalid choice. Enter numbers only from the menu.")
        return

    log_event("INFO", f"Encryption process started for dataset selection: {dataset_choice}")
    targets = list(DATA_FILES.keys()) if dataset_choice == "ALL" else [dataset_choice]

    slow_print("\nInitializing encryption process...", 0.8)

    if not verify_certificate(show_output=True):
        print("Operation stopped due to invalid certificate.")
        log_event("SECURITY", "Encryption blocked due to invalid certificate")
        return

    for dataset_name in targets:
        slow_print(f"\nProcessing {dataset_name} dataset...", 0.8)
        df = load_dataset(dataset_name)

        if df.empty:
            print(f"{dataset_name} is empty.")
            log_event("INFO", f"{dataset_name} dataset was empty during encryption")
            continue

        sample_before = df.loc[df.index[0]].copy()

        processed_count = 0
        for idx in df.index:
            row = df.loc[idx].copy()
            updated_row = encrypt_row(row, dataset_name)
            df.loc[idx] = updated_row
            processed_count += 1

        save_dataset(dataset_name, df)

        sample_after = df.loc[df.index[0]].copy()
        show_sample_change(sample_before, sample_after, dataset_name)

        print("\nIntegrity Status")
        print("----------------")
        print(f"Hash generated for encrypted rows in {dataset_name}.")
        print(f"Rows processed: {processed_count}")
        print(f"{dataset_name} encryption completed successfully.")

        log_event("SUCCESS", f"{dataset_name} encrypted successfully. Rows processed: {processed_count}")
        time.sleep(1)


def decrypt_flow():
    dataset_choice = dataset_choice_menu()
    if not dataset_choice:
        print("Invalid choice. Enter numbers only from the menu.")
        return

    log_event("INFO", f"Decryption process started for dataset selection: {dataset_choice}")
    targets = list(DATA_FILES.keys()) if dataset_choice == "ALL" else [dataset_choice]

    slow_print("\nInitializing decryption process...", 0.8)

    if not verify_certificate(show_output=True):
        print("Operation stopped due to invalid certificate.")
        log_event("SECURITY", "Decryption blocked due to invalid certificate")
        return

    for dataset_name in targets:
        slow_print(f"\nProcessing {dataset_name} dataset...", 0.8)
        df = load_dataset(dataset_name)

        if df.empty:
            print(f"{dataset_name} is empty.")
            log_event("INFO", f"{dataset_name} dataset was empty during decryption")
            continue

        sample_before = df.loc[df.index[0]].copy()

        processed_count = 0
        try:
            for idx in df.index:
                row = df.loc[idx].copy()
                updated_row = decrypt_row(row, dataset_name)
                df.loc[idx] = updated_row
                processed_count += 1
        except Exception as e:
            log_event("SECURITY", f"Integrity or decryption failure in {dataset_name}: {e}")
            raise

        save_dataset(dataset_name, df)

        sample_after = df.loc[df.index[0]].copy()
        show_sample_change(sample_before, sample_after, dataset_name)

        print("\nIntegrity Status")
        print("----------------")
        print("Hash verification completed before decryption.")
        print(f"Rows processed: {processed_count}")
        print(f"{dataset_name} decryption completed successfully.")

        log_event("SUCCESS", f"{dataset_name} decrypted successfully. Rows processed: {processed_count}")
        time.sleep(1)


def search_flow():
    print("\nSearch Menu")
    print("1. Search by patient_id")
    print("2. Back")

    choice = input("Enter choice: ").strip()

    if choice == "2":
        return

    if choice != "1":
        print("Invalid choice. Enter numbers only from the menu.")
        return

    dataset_choice = single_or_all_dataset_choice_menu()
    if not dataset_choice or dataset_choice == "BACK":
        return

    patient_id = input("Enter patient_id: ").strip()

    if not patient_id.isdigit():
        print("patient_id must be numeric.")
        return

    log_event("INFO", f"Search initiated for patient_id: {patient_id} in dataset selection: {dataset_choice}")
    slow_print("\nSearching record...", 0.7)

    targets = list(DATA_FILES.keys()) if dataset_choice == "ALL" else [dataset_choice]
    found_any = False

    print("\nDisplay Options")
    print("1. Show all fields")
    print("2. Show key fields only")
    print("3. Back")

    display_choice = input("Enter choice: ").strip()

    if display_choice == "3":
        return

    if display_choice not in ["1", "2"]:
        print("Invalid choice.")
        return

    for dataset_name in targets:
        df = load_dataset(dataset_name)
        results = find_by_patient_id(df, patient_id)

        if results.empty:
            continue

        found_any = True
        log_event("SUCCESS", f"Record found in {dataset_name} for patient_id: {patient_id}")

        row = results.iloc[0].copy()
        encrypted_state = str(row.get("enc_status", "plaintext")).lower()

        print(f"\n{'=' * 20} {dataset_name} RECORD {'=' * 20}")

        if encrypted_state == "encrypted":
            slow_print("Encrypted record found. Validating certificate and integrity for secure preview...", 1)

            if not verify_certificate(show_output=True):
                print("Cannot preview encrypted record because certificate validation failed.")
                log_event("SECURITY", f"Encrypted preview blocked by certificate failure for patient_id: {patient_id} in {dataset_name}")
                continue

            try:
                row, status = preview_decrypt_row(row, dataset_name)

                print("\nIntegrity Status")
                print("----------------")
                print("Hash verification successful.")
                print("Encrypted record temporarily decrypted for display.")
                log_event("SECURITY", f"Encrypted record previewed for patient_id: {patient_id} in {dataset_name}")
            except Exception as e:
                print(f"Preview failed: {e}")
                log_event("SECURITY", f"Encrypted preview failed for patient_id: {patient_id} in {dataset_name}. Reason: {e}")
                continue
        else:
            print("\nRecord is already in plaintext.")
            status = "plaintext"

        row_df = pd.DataFrame([row])

        if display_choice == "1":
            print("\nPatient Record")
            print("--------------")
            display_records(row_df)
        else:
            key_fields = [
                col for col in row_df.columns
                if col in [
                    "patient_id",
                    "hospital_branch",
                    "record_date",
                    "billing_date",
                    "patient_name",
                    "service_type",
                    "total_bill",
                    "disease_diagnosis",
                    "payment_status",
                    "discharge_status",
                    "enc_status"
                ]
            ]
            print("\nPatient Record")
            print("--------------")
            display_records(row_df, key_fields)

        print(f"\nDisplay mode: {status}")

    if not found_any:
        print("No matching patient record found in the selected dataset(s).")
        log_event("INFO", f"No record found for patient_id: {patient_id} in dataset selection: {dataset_choice}")


def main():
    while True:
        print("\n" + "=" * 38)
        print("      ASHN VPN SECURITY SYSTEM")
        print("=" * 38)
        print("1. Encrypt data")
        print("2. Decrypt data")
        print("3. Search records")
        print("4. Exit")

        choice = input("Enter choice: ").strip()

        if not choice.isdigit():
            print("Please enter numbers only.")
            continue

        try:
            if choice == "1":
                encrypt_flow()
            elif choice == "2":
                decrypt_flow()
            elif choice == "3":
                search_flow()
            elif choice == "4":
                log_event("INFO", "System exited by user")
                print("Exiting system.")
                break
            else:
                print("Invalid menu choice.")
        except Exception as e:
            log_event("ERROR", f"System error occurred: {e}")
            print(f"Error: {e}")


if __name__ == "__main__":
    main()