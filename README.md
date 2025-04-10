# 🧾 Payslip Generator

This is a Python script that automates the process of generating and emailing monthly payslips to employees. It reads data from an Excel file, calculates net salaries, generates PDF payslips, and sends them via email.

---

## 📌 Features

- Reads employee data from an Excel file using `pandas`
- Calculates net salary:

Net Salary = Basic Salary + Allowances - Deductions
- Generates a professional PDF payslip using `fpdf`
- Emails the payslip to each employee using `smtplib`
- Uses `.env` for secure email credentials

---

## 🛠️ Requirements

- Python 3.x
- Required libraries:
- pandas
- fpdf
- openpyxl
- python-dotenv

Install them using:

pip install pandas fpdf openpyxl python-dotenv
📁 Files and Folders
.
├── payslip_generator.py      # Main script
├── employees.xlsx            # Input Excel file with employee details
├── payslips/                 # Folder where PDF payslips will be saved
├── .env                      # Hidden file for email credentials
└── README.md                 # This file

🔐 Environment Variables

Create a .env file in the root directory with the following content:

SMTP_SERVER=smtp.yourmail.com
SMTP_PORT=587
EMAIL_USER=your_email@example.com
EMAIL_PASS=your_email_password_or_app_password
⚠️ Never share your .env file or commit it to Git.

🧑‍💼 Excel File Format

The employees.xlsx file should include the following columns:

Employee ID	Name	Email	Basic Salary	Allowances	Deductions
001	Jane Doe	jane@example.com	1000	200     	100
002	John Smith	john@example.com	1200	300	        150

▶️ How to Run the Script
Make sure your .env and employees.xlsx are ready.

Open your terminal in the project folder.

Run the script:


python payslip_generator.py
📧 Email Details
Subject: Your Payslip for This Month

Body:

Dear [Employee Name],

Please find attached your payslip for this month.

Best regards,  
Uncommon.org
Attachment: The employee’s PDF payslip

✅ Output

Payslips will be saved in the payslips/ folder.

Each file is named by Employee ID (e.g., 001.pdf).

The PDF includes employee info, salary breakdown, and a professional layout.

🧑‍💻 Author

Created by Kudzaishe Chikowore
For the Python Programming Assignment: Payslip Generator