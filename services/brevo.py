
import os
import requests
from dotenv import load_dotenv

load_dotenv()


class BrevoService:

    def __init__(self):

        self.api_key = os.getenv(
            "BREVO_API_KEY"
        )

        self.sender_email = os.getenv(
            "SENDER_EMAIL"
        )

        self.sender_name = os.getenv(
            "SENDER_NAME",
            "Vignesh"
        )

        self.url = (
            "https://api.brevo.com/v3/smtp/email"
        )

    def send_email(
        self,
        recipient,
        subject,
        body
    ):

        headers = {
            "accept":
                "application/json",

            "api-key":
                self.api_key,

            "content-type":
                "application/json"
        }

        payload = {
            "sender": {
                "name":
                    self.sender_name,

                "email":
                    self.sender_email
            },

            "to": [
                {
                    "email":
                        recipient
                }
            ],

            "subject":
                subject,

            "htmlContent":
                f"<p>{body}</p>"
        }

        response = requests.post(
            self.url,
            headers=headers,
            json=payload,
            timeout=30
        )

        print(
            "\nBrevo Status:",
            response.status_code
        )

        print(
            response.text
        )

        response.raise_for_status()

        return response.json()