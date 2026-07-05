import os
import logging
import smtplib
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText



## Start Logging Information to log    
script_path = os.path.abspath(__file__)
# Get the directory name from the script path
script_dir = os.path.dirname(script_path)
# Get the parent directory using os.pardir ('..')
parent_directory = os.path.abspath(os.path.join(script_dir, os.pardir))
print(f"Parent directory path: {parent_directory}")


log_file_path = os.path.join(parent_directory, "send_email_Tool_LOG.log") 

#logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")


logging.basicConfig(
    filename= log_file_path,
    filemode='a',
    format="%(asctime)s | %(levelname)s | %(message)s",
    level=logging.INFO,
    force=True
)


from dotenv import load_dotenv, find_dotenv
import os

# Find the .env file, searching upwards in the directory tree
dotenv_path = find_dotenv()

# Load the .env file
load_dotenv(dotenv_path)
# Now you can access environment variables
print("=="*50 )
print("\n")
print(f"Path to .env file: {dotenv_path}")
print(f"Example variable SMTP_ENABLED : {os.getenv('SMTP_ENABLED')}") 
print(f"Example variable SMTP_APP_PASSWORD : {os.getenv('SMTP_APP_PASSWORD')}") 
print("=="*50 )
print("\n")

def send_email(body):
    """Send an email using Gmail SMTP.

    This function is safe to call from another program or a Gradio/Hugging Face app.
    It logs detailed information and returns a boolean status.
    """
    sender_email = os.getenv("SMTP_SENDER_EMAIL", "aiwthraj@gmail.com")
    app_password = os.getenv("SMTP_APP_PASSWORD", "eamfbjsxhpfwxmds")
    receiver_email = os.getenv("SMTP_RECEIVER_EMAIL", "aiwthraj@gmail.com")

    smtp_enabled = os.getenv("SMTP_ENABLED", "false").strip().lower()
    if smtp_enabled not in {"1", "true", "yes", "on"}:
        logging.info("SMTP sending skipped because SMTP_ENABLED is not enabled.")
        print("SMTP sending skipped because SMTP_ENABLED is not enabled.")
        return False

    if not app_password:
        logging.error("SMTP_APP_PASSWORD is not set. Email was not sent.")
        print("SMTP_APP_PASSWORD is not set. Email was not sent.")
        return False

    today_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    subject = f"Daily AI News Update - {today_date}"

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = "rajendrabraj@gmail.com"
    message["Cc"] = sender_email
    message["Subject"] = subject

    message_body = body if body is not None else ""
    message.attach(MIMEText(message_body, "plain", "utf-8"))

    try:
        logging.info("Connecting to Gmail SMTP server using SSL on port 465...")
        print("Connecting to Gmail SMTP server using SSL on port 465...")
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, timeout=60) as server:
            server.login(sender_email, app_password)
            server.send_message(message)
        logging.info("Email sent successfully!")
        print("Email sent successfully!")
        return True

    except OSError as exc:
        logging.warning("SMTP network is unavailable in this environment: %s", exc)
        print("SMTP network is unavailable in this environment; email skipped.")
        return False

    except Exception as exc:
        logging.exception("SMTP delivery failed: %s", exc)
        print("SMTP delivery failed; email skipped.")
        return False

def main():
    email_message_body = "Sample email body content for testing the send_email function."
    send_email(email_message_body)
    print("TESTING Email Function...")
    

if __name__ == "__main__":
    main()