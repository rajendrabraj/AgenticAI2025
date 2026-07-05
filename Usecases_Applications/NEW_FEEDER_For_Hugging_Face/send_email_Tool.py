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




def send_email(body):
    """Send an email using Gmail SMTP.

    This function is safe to call from another program or a Gradio/Hugging Face app.
    It logs detailed information and returns a boolean status.
    """
    # sender_email = os.getenv("SMTP_SENDER_EMAIL", "aiwthraj@gmail.com")
    # app_password = os.getenv("SMTP_APP_PASSWORD")
    # receiver_email = os.getenv("SMTP_RECEIVER_EMAIL", "aiwthraj@gmail.com")
    
    sender_email = "aiwthraj@gmail.com"
    app_password = "eamfbjsxhpfwxmds"
    receiver_email = "aiwthraj@gmail.com"
    

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

    server = None
    try:
        logging.info("Connecting to Gmail SMTP server...")
        print("Connecting to Gmail SMTP server...")
        server = smtplib.SMTP("smtp.gmail.com", 587, timeout=60)
        server.ehlo()
        server.starttls()
        server.login(sender_email, app_password)
        server.send_message(message)
        logging.info("Email sent successfully!")
        print("Email sent successfully!")
        return True

    except Exception as exc:
        logging.exception("SMTP delivery failed: %s", exc)
        print(f"SMTP delivery failed: {exc}")
        return False

    finally:
        if server is not None:
            try:
                server.quit()
            except Exception:
                try:
                    server.close()
                except Exception:
                    pass

# def main():
#     email_message_body = "Sample email body content for testing the send_email function."
#     send_email(email_message_body)
#     print("TESTING Email Function...")
    

# if __name__ == "__main__":
#     main()