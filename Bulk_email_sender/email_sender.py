# email_sender.py

import pandas as pd
from PyPDF2 import PdfFileReader
import re

def read_emails(file):
    file_extension = file.name.split('.')[-1]
    if file_extension == 'csv':
        df = pd.read_csv(file)
    elif file_extension == 'xlsx':
        df = pd.read_excel(file)
    elif file_extension == 'pdf':
        pdf = PdfFileReader(file)
        emails = []
        for page_num in range(pdf.getNumPages()):
            page = pdf.getPage(page_num)
            text = page.extract_text()
            emails.extend(re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text))
        df = pd.DataFrame(emails, columns=['Email'])
    else:
        raise ValueError("Unsupported file type")
    
    # Handle cases where the column might not be named 'Email'
    possible_email_columns = [col for col in df.columns if 'email' in col.lower()]
    if possible_email_columns:
        email_column = possible_email_columns[0]
    else:
        raise ValueError("No column named 'Email' found in the file")
    
    return df[email_column].tolist()

def send_email(user_email, user_password, recipient, subject, content, attachment=None):
    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    from email.mime.base import MIMEBase
    from email import encoders

    try:
        msg = MIMEMultipart()
        msg['From'] = user_email
        msg['To'] = recipient
        msg['Subject'] = subject
        msg.attach(MIMEText(content, 'plain'))

        if attachment:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f'attachment; filename={attachment.name}')
            msg.attach(part)

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(user_email, user_password)
        text = msg.as_string()
        server.sendmail(user_email, recipient, text)
        server.quit()
        return True
    except Exception as e:
        print(f"Failed to send email to {recipient}. Error: {e}")
        return False
