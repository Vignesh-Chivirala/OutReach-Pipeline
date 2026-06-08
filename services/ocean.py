import os
import requests
from dotenv import load_dotenv

load_dotenv()


class OceanService:

    def __init__(self):

        self.api_key = os.getenv("OCEAN_API_KEY")

        if not self.api_key:
            raise Exception(
                "OCEAN_API_KEY not found in .env"
            )

        self.base_url = "https://api.ocean.io"

        self.headers = {
            "x-api-token": self.api_key,
            "Content-Type": "application/json"
        }

    def get_raw_response(
        self,
        domain,
        limit=10
    ):

        endpoint = (
            f"{self.base_url}/v3/search/companies"
        )

        payload = {
            "size": limit,
            "companiesFilters": {
                "lookalikeDomains": [
                    domain
                ]
            }
        }

        response = requests.post(
            endpoint,
            headers=self.headers,
            json=payload,
            timeout=60
        )

        print("\n===================")
        print("Status:", response.status_code)
        print("===================")
        print(response.text)
        print("===================\n")

        response.raise_for_status()

        return response.json()

    def get_company_domains(
        self,
        domain,
        limit=10
    ):

        data = self.get_raw_response(
            domain,
            limit
        )

        domains = []

        # recursively search for domains
        def extract(obj):

            if isinstance(obj, dict):

                for key, value in obj.items():

                    if (
                        key.lower() == "domain"
                        and isinstance(value, str)
                    ):
                        domains.append(value)

                    extract(value)

            elif isinstance(obj, list):

                for item in obj:
                    extract(item)

        extract(data)

        return list(set(domains))