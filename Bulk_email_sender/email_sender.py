import pandas as pd
from PyPDF2 import PdfFileReader
import re
from email.message import EmailMessage    
import smtplib, ssl

def read_emails(file):
    file_extension = file.name.split('.')[-1].lower()
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

def send_email(user_email, user_password, recipient, subject, body_message, attachments):
    try:
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as server:
            server.login(user_email, user_password)
            
            em = EmailMessage()
            em['From'] = user_email
            em['To'] = recipient
            em['Subject'] = subject
            em.set_content(body_message)
            
            for attachment in attachments:
                em.add_attachment(
                    attachment["content"],
                    maintype=attachment["maintype"],
                    subtype=attachment["subtype"],
                    filename=attachment["filename"]
                )
            
            server.send_message(em)
        
        return True
        
    except smtplib.SMTPAuthenticationError:
        print(f"Authentication failed. Check your email and password.")
    except smtplib.SMTPConnectError:
        print(f"Failed to connect to the SMTP server. Check your network settings.")
    except smtplib.SMTPException as e:
        print(f"SMTP error occurred: {e}")
    except Exception as e:
        print(f"Failed to send email to {recipient}. Error: {e}")
    
    return False

