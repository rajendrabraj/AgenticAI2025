import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Your Gmail credentials
sender_email = "aiwthraj@gmail.com"
app_password = "eamfbjsxhpfwxmds"

# Receiver email
receiver_email = "aiwthraj@gmail.com"

# Create message
message = MIMEMultipart()
message["From"] = "aiwthraj@gmail.com"
message["To"] = "aiwthraj@gmail.com"
message["Subject"] = "Daily AI News Update"


# Email body
body = "Daily AI News for Today."
message.attach(MIMEText(body, "plain"))

try:
    # Connect to Gmail SMTP server
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()  # Secure connection
    server.login(sender_email, app_password)

    # Send email
    server.send_message(message)
    print("Email sent successfully!")

except Exception as e:
    print("Error:", e)

finally:
    server.quit()