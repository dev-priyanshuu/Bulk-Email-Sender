import streamlit as st
import os
from email_sender import read_emails, send_email
import time

# Load Google API key from environment variable
api_key = os.getenv("GOOGLE_API_KEY")

st.set_page_config(page_title="Email Sender")

st.header("Bulk Email Sender")

uploaded_file = st.file_uploader("Upload a file (PDF, Excel, CSV)", type=["pdf", "xlsx", "csv"])
attachments = st.file_uploader("Upload a file to attach (optional)", type=None, accept_multiple_files=True)
subject = st.text_input("Email Subject")
body_message = st.text_area("Email Content")
user_email = st.text_input("Sender Email")
user_password = st.text_input("Your App Password", type="password")
st.markdown("[How to create an app password?](https://support.google.com/accounts/answer/185833?hl=en)")

submit = st.button("Send Emails")

if submit:
    if uploaded_file and subject and body_message and user_email and user_password:
        try:
            emails = read_emails(uploaded_file)
            st.write(f"Found {len(emails)} emails to send.")
            
            attachment_data = []
            for attachment in attachments:
                content = attachment.read()
                maintype, subtype = attachment.type.split('/', 1)
                attachment_data.append({
                    "filename": attachment.name,
                    "content": content,
                    "maintype": maintype,
                    "subtype": subtype
                })

            for email in emails:
                if send_email(user_email, user_password, email, subject, body_message, attachment_data):
                    st.write(f"Email sent to {email}")
                else:
                    st.write(f"Failed to send email to {email}")
                time.sleep(1)  # Adding delay to avoid being flagged as spam
        except Exception as e:
            st.error(f"Error: {e}")
    else:
        st.error("Please fill in all fields and upload a file.")
