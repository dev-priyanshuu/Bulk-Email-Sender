# app.py

import streamlit as st
import os
from email_sender import read_emails, send_email
import time

# Load Google API key from environment variable
api_key = os.getenv("GOOGLE_API_KEY")

st.set_page_config(page_title="Email Sender")

st.header("Bulk Email Sender using LLM")

uploaded_file = st.file_uploader("Upload a file (PDF, Excel, CSV)", type=["pdf", "xlsx", "csv"])
attachment_file = st.file_uploader("Upload a file to attach (optional)", type=["pdf", "docx", "xlsx", "csv"])
subject = st.text_input("Email Subject")
content = st.text_area("Email Content")
user_email = st.text_input("Your Email")
user_password = st.text_input("Your Email Password", type="password")

submit = st.button("Send Emails")

if submit:
    if uploaded_file and subject and content and user_email and user_password:
        try:
            emails = read_emails(uploaded_file)
            st.write(f"Found {len(emails)} emails to send.")
            for email in emails:
                if send_email(user_email, user_password, email, subject, content, attachment_file):
                    st.write(f"Email sent to {email}")
                else:
                    st.write(f"Failed to send email to {email}")
                time.sleep(1)  # Adding delay to avoid being flagged as spam
        except Exception as e:
            st.error(f"Error: {e}")
    else:
        st.error("Please fill in all fields and upload a file.")
