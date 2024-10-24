# systemlogparser_cli_schedule
This script is designed to automate the process of running a system log parser tool (SLP), analyzing ArcGIS Server logs, and generating comprehensive reports. 

This script is in response to running https://github.com/Esri/SystemLogParser

You run the scripts in order of the numbering on the title. 

Here’s a description for the script that you can use on GitHub:

---

### **Script Name:** `system_log_parser.py`

### **Description:**

This script is designed to automate the process of running a system log parser tool (SLP), analyzing ArcGIS Server logs, and generating comprehensive reports. The script dynamically creates output directories based on the current date, runs the parser tool, logs the process, and sends an email notification upon successful completion with the log file as a reference.

### **Key Features**:
- **Password Encryption and Decryption**: The script securely handles sensitive information, such as user credentials, by utilizing the `cryptography` library to encrypt and decrypt the password used for the ArcGIS Server authentication.
- **Automated Folder Creation**: It automatically detects the current month and day to create organized folder structures for storing the reports.
- **Command Execution Logging**: Logs the full command used to execute the System Log Parser tool and captures any output or errors, making it easy to debug and review the process.
- **Email Notification**: Once the report is generated, an email is sent to predefined recipients, including the log file for reference.
- **Dynamic Report Naming**: The generated report and log files are timestamped to ensure uniqueness and easy tracking.

### **Usage**:
1. **Setup Encryption**: Ensure you have generated an encryption key using the `cryptography` library and encrypted the password to be used for accessing the ArcGIS Server.
2. **Configure Paths**: Update the script with the correct paths for the system log parser executable, the secret key file, the base report folder, and the ArcGIS Server URL.
3. **Run the Script**: The script will execute the SLP tool, generate a report, and move the report to the appropriate folder based on the current date.
4. **Receive Email Notifications**: After the report is generated, an email with the log file will be sent to the recipients defined in the script.

### **Prerequisites**:
- **Python 3.6+** installed.
- Required Python libraries, such as `cryptography`, installed using:
  ```bash
  pip install cryptography
  ```
- ArcGIS Server credentials encrypted with the `cryptography` library.
- Access to the System Log Parser tool (`slp.exe`), with the correct file paths provided.

### **Output Example**:
The script generates a structured folder for reports like:
```
/path/to/Enterprise Reports/Log Parser/2024/10. October/2024-10-24
```
Files generated:
- `System_Logs_Report_ArcGISServer--20241024T143000.xlsx`
- `System_Logs_Report_ArcGISServer--20241024T143000.txt` (log file)

---

### **Sample Email Notification**:
Subject: *GeoState System Log Parser Report*

Body:
```
The most recent reports generated by the GeoState System Log Parser Scripts are located in /path/to/output. 
Please review the report for the most up-to-date ArcGIS Server Report.

Log file for the operation: /path/to/log_file.txt
```

### **Customization**:
Users will need to update:
- File paths for the system log parser tool, output folder, and encryption key.
- Email addresses for the sender, recipients, and SMTP server information.
- Encrypted password, using the appropriate encryption method for their environment.

---

