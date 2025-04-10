import pandas as pd
from fpdf import FPDF
import os
from datetime import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from email.mime.text import MIMEText
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Constants for email configuration
SMTP_SERVER = os.getenv('SMTP_SERVER')
SMTP_PORT = os.getenv('SMTP_PORT')
EMAIL_USER = os.getenv('EMAIL_USER')
EMAIL_PASS = os.getenv('EMAIL_PASS')

def validate_data(df):
    """Check if the data has all required columns and no missing values."""
    required_columns = ['Employee ID', 'Name', 'Email', 'Basic Salary', 'Allowances', 'Deductions']
    missing_columns = [col for col in required_columns if col not in df.columns]
    
    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")
    
    if df.isnull().values.any():
        raise ValueError("Excel file contains missing values in some cells")
    
    print("✓ Data validation passed - all required columns present with no missing values")

def calculate_net_salary(df):
    """Calculate net salary for each employee."""
    df['Net Salary'] = df['Basic Salary'] + df['Allowances'] - df['Deductions']
    return df

def generate_payslip(employee):
    """Generate a PDF payslip for one employee."""
    pdf = FPDF()
    pdf.add_page()
    
    # Title
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(0, 10, 'MONTHLY PAYSLIP', 0, 1, 'C')
    pdf.ln(10)  # Add space
    
    # Company info
    pdf.set_font('Arial', '', 12)
    pdf.cell(0, 10, 'Uncommon.org', 0, 1, 'C')
    pdf.cell(0, 10, f'Date: {datetime.now().strftime("%d/%m/%Y")}', 0, 1, 'C')
    pdf.ln(10)
    
    # Employee info
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(40, 10, 'Employee ID:', 0, 0)
    pdf.set_font('Arial', '', 12)
    pdf.cell(0, 10, str(employee['Employee ID']), 0, 1)
    
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(40, 10, 'Name:', 0, 0)
    pdf.set_font('Arial', '', 12)
    pdf.cell(0, 10, employee['Name'], 0, 1)
    pdf.ln(10)
    
    # Salary details
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, 'Salary Details', 0, 1)
    pdf.set_font('Arial', '', 12)
    
    pdf.cell(60, 10, 'Basic Salary:', 0, 0)
    pdf.cell(0, 10, f"${employee['Basic Salary']:,.2f}", 0, 1)
    
    pdf.cell(60, 10, 'Allowances:', 0, 0)
    pdf.cell(0, 10, f"${employee['Allowances']:,.2f}", 0, 1)
    
    pdf.cell(60, 10, 'Deductions:', 0, 0)
    pdf.cell(0, 10, f"${employee['Deductions']:,.2f}", 0, 1)
    
    # Net salary
    net_salary = employee['Net Salary']
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(60, 10, 'Net Salary:', 0, 0)
    pdf.cell(0, 10, f"${net_salary:,.2f}", 0, 1)
    
    # Footer
    pdf.ln(20)
    pdf.set_font('Arial', 'I', 10)
    pdf.cell(0, 10, 'This is a computer generated payslip. No signature required.', 0, 1, 'C')
    
    # Save the PDF
    filename = f"payslips/{employee['Employee ID']}.pdf"
    pdf.output(filename)
    print(f"Generated payslip: {filename}")

def send_email(employee):
    """Send the payslip to the employee via email."""
    msg = MIMEMultipart()
    msg['From'] = EMAIL_USER
    msg['To'] = employee['Email']
    msg['Subject'] = "Your Payslip for This Month"

    body = f"Dear {employee['Name']},\n\nPlease find attached your payslip for this month.\n\nBest regards,\nUncommon.org"
    msg.attach(MIMEText(body, 'plain'))

    # Attach the payslip
    filename = f"payslips/{employee['Employee ID']}.pdf"
    attachment = open(filename, "rb")
    part = MIMEBase('application', 'octet-stream')
    part.set_payload(attachment.read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', f'attachment; filename={filename}')
    msg.attach(part)

    # Send the email
    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()  # Secure the connection
        server.login(EMAIL_USER, EMAIL_PASS)
        server.send_message(msg)
        server.quit()
        print(f"Email sent to {employee['Email']}")
    except Exception as e:
        print(f"Failed to send email to {employee['Email']}: {str(e)}")

# Main program
def main():
    # Create payslips directory if it doesn't exist
    if not os.path.exists('payslips'):
        os.makedirs('payslips')

    try:
        # Read the Excel file
        employee_data = pd.read_excel('employees.xlsx')
        
        # Validate the data
        validate_data(employee_data)
        
        # Calculate net salaries
        employee_data = calculate_net_salary(employee_data)
        
        # Generate payslips and send emails
        print("Generating payslips and sending emails...")
        for index, employee in employee_data.iterrows():
            generate_payslip(employee)
            send_email(employee)
        
        print("\nAll payslips generated and emails sent successfully!")
        
    except Exception as e:
        print(f"\nError: {str(e)}")

if __name__ == "__main__":
    main()