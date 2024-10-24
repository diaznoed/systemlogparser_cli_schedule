import os
import subprocess
import datetime
import time
import smtplib
from email.message import EmailMessage
from cryptography.fernet import Fernet

# Function to load the encryption key from a specified path
def load_key():
    # Update the key path with your actual key file location
    return open(r"/path/to/secret.key", "rb").read()  # <--- Update this path

# Function to encrypt the password
def encrypt_password(password):
    key = load_key()
    fernet = Fernet(key)
    encrypted_password = fernet.encrypt(password.encode())
    return encrypted_password

# Function to decrypt the password
def decrypt_password(encrypted_password):
    key = load_key()
    fernet = Fernet(key)
    decrypted_password = fernet.decrypt(encrypted_password).decode()
    return decrypted_password

# Function to send an email with log file information
def send_email(log_file_path):
    # Email body and subject
    bodyLine1 = (
        "The most recent reports generated by the GeoState System Log Parser Scripts are located in /path/to/output. "  # <--- Update this path
        "Please review the report for the most up-to-date ArcGIS Server Report.\n\n"
        f"Log file for the operation: {log_file_path}\n"
    )
    subjString = "GeoState System Log Parser Report"
    
    # Update the sender and recipient email addresses
    smmFrom = "your-email@example.com"  # <--- Update this email
    SMTPMailRecpts = [
        "recipient1@example.com",  # <--- Add email recipients
        "recipient2@example.com",
    ]
    smmSvr = "your-smtp-server.com"  # <--- Update your SMTP server

    msg = EmailMessage()
    msg['From'] = smmFrom
    msg['To'] = ', '.join(SMTPMailRecpts)
    msg['Subject'] = subjString
    msg.set_content(bodyLine1)

    # Send the email
    with smtplib.SMTP(smmSvr) as server:
        server.send_message(msg)
    print("Email sent successfully.")

# Define variables (Users need to update these paths and server information)
SLP_PATH = r"/path/to/SystemLogParser/"  # <--- Update this path
SERVER_URL = "https://your-server-url.com/arcgis/"  # <--- Update with your server URL
USER_NAME = "YourUsername"  # <--- Update with your username

# Replace this with your actual encrypted password after running the above encryption function
encrypted_password = b'your-encrypted-password'  # <--- Replace with encrypted password

# Decrypt the password for use
PASSWORD = decrypt_password(encrypted_password)

START_TIME = "1day"
END_TIME = "now"
ANALYSIS_TYPE = "complete"
BASE_REPORT_FOLDER = r"/path/to/output"  # <--- Update this path

# Get current date and time in the format YYYYMMDDTHHMMSS
now = datetime.datetime.now()
TIMESTAMP = now.strftime("%Y%m%dT%H%M%S")

# Get the current month and day to dynamically create the folder structure
current_month = now.strftime("%B")  # Example: 'October'
DATE_FOLDER = now.strftime("%Y-%m-%d")
MONTH_FOLDER = f"{now.month}. {current_month}"  # Example: '10. October'

# Build the full report folder path for the current month and day
REPORT_FOLDER = os.path.join(BASE_REPORT_FOLDER, MONTH_FOLDER, DATE_FOLDER)
LOG_FILE = os.path.join(SLP_PATH, f"System_Logs_Report_ArcGISServer--{TIMESTAMP}.txt")
REPORT_NAME = f"System_Logs_Report_ArcGISServer--{TIMESTAMP}.xlsx"

# Create the output directory if it does not exist
if not os.path.exists(REPORT_FOLDER):
    os.makedirs(REPORT_FOLDER)

# Log the starting message
with open(LOG_FILE, 'w') as log:
    log.write(f"[{TIMESTAMP}] Starting System Log Parser...\n")
    log.write(f"[{TIMESTAMP}] Executing command: \"{SLP_PATH}slp.exe\" -f AGS -s {SERVER_URL} -u {USER_NAME} -p {PASSWORD} -sh {START_TIME} -eh {END_TIME} -a {ANALYSIS_TYPE} -validate true -d {REPORT_FOLDER} -n {REPORT_NAME}\n")

# Execute the System Log Parser command and log output
command = [
    os.path.join(SLP_PATH, "slp.exe"),
    "-f", "AGS",
    "-s", SERVER_URL,
    "-u", USER_NAME,
    "-p", PASSWORD,
    "-sh", START_TIME,
    "-eh", END_TIME,
    "-a", ANALYSIS_TYPE,
    "-validate", "true",
    "-d", REPORT_FOLDER,
    "-n", REPORT_NAME
]

with open(LOG_FILE, 'a') as log:
    process = subprocess.Popen(command, stdout=log, stderr=subprocess.STDOUT)
    process.wait()

# Log completion message
with open(LOG_FILE, 'a') as log:
    if process.returncode == 0:
        log.write(f"[{TIMESTAMP}] System Log Parser completed successfully.\n")
    else:
        log.write(f"[{TIMESTAMP}] System Log Parser encountered errors. Return code: {process.returncode}\n")
    log.write(f"[{TIMESTAMP}] Log file created at: {os.path.join(REPORT_FOLDER, REPORT_NAME)}\n")

# Wait for the .xlsx file to appear
while not os.path.exists(os.path.join(REPORT_FOLDER, REPORT_NAME)):
    time.sleep(10)

# Send the email after the report is generated
send_email(LOG_FILE)