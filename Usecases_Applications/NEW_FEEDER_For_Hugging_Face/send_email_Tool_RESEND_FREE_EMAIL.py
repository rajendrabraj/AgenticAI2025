import json
import logging
import os
import urllib.error
import urllib.request
from datetime import datetime

from dotenv import find_dotenv, load_dotenv


script_path = os.path.abspath(__file__)
script_dir = os.path.dirname(script_path)
parent_directory = os.path.abspath(os.path.join(script_dir, os.pardir))
log_file_path = os.path.join(parent_directory, "send_email_Tool_LOG.log")

logging.basicConfig(
    filename=log_file_path,
    filemode="a",
    format="%(asctime)s | %(levelname)s | %(message)s",
    level=logging.INFO,
    force=True,
)



# dotenv_path = find_dotenv()
# load_dotenv(dotenv_path)

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
print(f"Example variable RESEND_API_KEY : {os.getenv('RESEND_API_KEY')}") 
print(f"Example variable RESEND_FROM_EMAIL : {os.getenv('RESEND_FROM_EMAIL')}") 
print(f"Example variable RESEND_TO_EMAIL : {os.getenv('RESEND_TO_EMAIL')}") 
print(f"Example variable RESEND_CC_EMAIL : {os.getenv('RESEND_CC_EMAIL')}") 

print("=="*50 )
print("\n")


def _split_email_list(value):
    if not value:
        return []
    return [item.strip() for item in value.replace(";", ",").split(",") if item.strip()]


def _resolve_sender_email():
    configured_sender = os.getenv("RESEND_FROM_EMAIL", "").strip()
    if configured_sender:
        if configured_sender.lower().endswith("@resend.dev"):
            return configured_sender
        logging.warning(
            "RESEND_FROM_EMAIL is not a Resend verified sender (%s). Falling back to onboarding@resend.dev.",
            configured_sender,
        )
    return "onboarding@resend.dev"


def _resolve_api_key():
    for name in ("RESEND_API_KEY", "RESEND_API_TOKEN", "RESEND_TOKEN", "API_KEY"):
        value = os.getenv(name, "").strip()
        if value:
            return value
    return ""


def send_email(body):
    """Send an email through Resend using the same From/To/Cc/Subject values."""
    resend_api_key = _resolve_api_key()
    sender_email = _resolve_sender_email()
    receiver_email = os.getenv("RESEND_TO_EMAIL", "aiwthraj@gmail.com").strip()
    cc_email = os.getenv("RESEND_CC_EMAIL", "").strip()

    if not resend_api_key:
        logging.error("RESEND_API_KEY is not set. Email was not sent.")
        print("RESEND_API_KEY is not set. Email was not sent.")
        return False

    to_emails = _split_email_list(receiver_email)
    cc_emails = _split_email_list(cc_email)

    if not to_emails:
        logging.error("No recipient email was provided. Email was not sent.")
        print("No recipient email was provided. Email was not sent.")
        return False

    today_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    subject = f"Daily AI News Update - {today_date}"

    payload = {
        "from": sender_email,
        "to": to_emails,
        "subject": subject,
        "text": body if body is not None else "",
        "html": f"<p>{(body if body is not None else '')}</p>",
    }
    if cc_emails:
        payload["cc"] = cc_emails

    request = urllib.request.Request(
        "https://api.resend.com/emails",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {resend_api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            response_body = response.read().decode("utf-8")
            logging.info("Resend email sent successfully: %s", response_body)
            print("Email sent successfully via Resend!")
            return True

    except urllib.error.HTTPError as exc:
        error_body = exc.read().decode("utf-8", errors="ignore")
        logging.exception("Resend API request failed with HTTP %s: %s", exc.code, error_body)
        print(f"Resend request failed: {exc.code} {error_body}")
        if exc.code == 403:
            print("Access denied. Please check your RESEND_API_KEY and ensure it is valid.")
            print("Also verify that RESEND_FROM_EMAIL is a verified sender in Resend.")
        return False

    except Exception as exc:
        logging.exception("Resend delivery failed: %s", exc)
        print(f"Resend delivery failed: {exc}")
        return False


def main():
    email_message_body = "Sample email body content for testing the send_email function."
    send_email(email_message_body)
    print("TESTING Email Function...")


if __name__ == "__main__":
    main()