# services/eazyreach.py

import os
import requests
from dotenv import load_dotenv

load_dotenv()


class EazyReachService:

    def __init__(self):

        self.api_key = os.getenv(
            "EAZYREACH_API_KEY"
        )

        if not self.api_key:
            raise Exception(
                "EAZYREACH_API_KEY not found in .env"
            )

        self.base_url = (
            "https://api.superflow.run"
        )

        self.headers = {
            "Authorization":
                f"Bearer {self.api_key}",
            "Content-Type":
                "application/json"
        }

    def get_email(
        self,
        linkedin_url
    ):

        url = (
            f"{self.base_url}/b2b/linkedin-emails"
        )

        payload = {
            "linkedinUrl":
                linkedin_url
        }

        response = requests.post(
            url,
            headers=self.headers,
            json=payload,
            timeout=60
        )

        print(
            f"\nEazyReach Status: "
            f"{response.status_code}"
        )

        print(response.text)

        response.raise_for_status()

        data = response.json()

        return {
            "email":
                data.get("email"),

            "work_email":
                data.get("workEmail"),

            "personal_email":
                data.get("personalEmail"),

            "raw":
                data
        }