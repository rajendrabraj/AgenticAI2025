import pandas as pd
from datetime import datetime
import hashlib
import html

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging
import os





def send_email(body):   
    # Your Gmail credentials
    sender_email = "aiwthraj@gmail.com"
    app_password = "eamfbjsxhpfwxmds"

    # Receiver email
    receiver_email = "aiwthraj@gmail.com"

    from datetime import datetime; 
    today_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    subject = f"Daily AI News Update - {today_date}"
    

    # Create message
    message = MIMEMultipart()
    message["From"] = "aiwthraj@gmail.com"
    message["To"] = "rajendrabraj@gmail.com"
    message["cc"] = "aiwthraj@gmail.com"
    message["Subject"] = subject


    # Email body
    #body = "Daily AI News for Today."
    message_body=body
    message.attach(MIMEText(message_body, "plain"))
    
     


    server = None
    try:
        print("SMTP Server started successfully!")
        server = smtplib.SMTP("smtp.gmail.com", 587, timeout=100)
        server.starttls()  # Secure connection
        server.login(sender_email, app_password)
        server.send_message(message)    
        print("Email sent successfully!")
        logging.info(f"[NEWSFEEDER BOT : ] Email sent successfully!")

    except Exception as e:
        print("Error:", e)
        logging.info(f"[NEWSFEEDER BOT : ] Error occurred while sending email: {e}")

    finally:
        if server is not None:
            try:
                server.quit()
                print("SMTP Server QUIT successfully!")
            except Exception:
                try:
                    server.close()
                    print("SMTP Server Connection Closed successfully!")
                except Exception:
                    pass

# def main():
#     email_message_body = "Sample email body content for testing the send_email function."
#     send_email(email_message_body)
#     print("TESTING Email Function...")
    

# if __name__ == "__main__":
#     main()
    