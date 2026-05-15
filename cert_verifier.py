import subprocess
from config import CERT_FILES
from logger import log_event


def verify_certificate(show_output=True):
    try:
        result = subprocess.run(
            [
                "openssl",
                "verify",
                "-CAfile",
                CERT_FILES["ca_cert"],
                CERT_FILES["client_cert"]
            ],
            capture_output=True,
            text=True,
            check=False
        )

        is_valid = result.returncode == 0

        if is_valid:
            log_event("SUCCESS", "Certificate verified successfully")
        else:
            log_event("SECURITY", "Certificate verification failed")

        if show_output:
            print("\n[PKI CERTIFICATE VERIFICATION]")
            print("--------------------------------")
            print("Command: openssl verify -CAfile ... client_cert")
            print("\nStdout:")
            print(result.stdout.strip() if result.stdout.strip() else "No stdout output")
            print("\nStderr:")
            print(result.stderr.strip() if result.stderr.strip() else "No stderr output")
            print(f"\nReturn code: {result.returncode}")
            print(f"Verification result: {'VALID' if is_valid else 'INVALID'}")

        return is_valid

    except Exception as e:
        log_event("ERROR", f"Certificate "
                           f"verification error: {e}")
        if show_output:
            print("\n[PKI CERTIFICATE VERIFICATION]")
            print("--------------------------------")
            print(f"Certificate verification failed "
                  f"with exception: {e}")
        return False

    