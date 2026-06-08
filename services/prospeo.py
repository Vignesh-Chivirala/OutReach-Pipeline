
import os
import requests
from dotenv import load_dotenv

load_dotenv()


class ProspeoService:

    def __init__(self):

        self.api_key = os.getenv(
            "PROSPEO_API_KEY"
        )

        if not self.api_key:
            raise Exception(
                "PROSPEO_API_KEY not found in .env"
            )

        self.base_url = (
            "https://api.prospeo.io"
        )

        self.headers = {
            "X-KEY": self.api_key,
            "Content-Type": "application/json"
        }

    def search_decision_makers(
        self,
        domain
    ):

        url = (
            f"{self.base_url}/search-person"
        )

        payload = {
            "page": 1,
            "filters": {
                "person_search": {
                    "company_domain": domain
                },
                "person_seniority": {
                    "include": [
                        "Founder/Owner"
                    ]
                }
            }
        }

        response = requests.post(
            url,
            headers=self.headers,
            json=payload,
            timeout=60
        )

        response.raise_for_status()

        data = response.json()

        results = data.get(
            "results",
            []
        )

        contacts = []

        for record in results:

            person = record.get(
                "person",
                {}
            )

            company = record.get(
                "company",
                {}
            )

            email_info = person.get(
                "email",
                {}
            )

            mobile_info = person.get(
                "mobile",
                {}
            )

            contacts.append({

                "person_id":
                    person.get(
                        "person_id"
                    ),

                "name":
                    person.get(
                        "full_name"
                    ),

                "first_name":
                    person.get(
                        "first_name"
                    ),

                "last_name":
                    person.get(
                        "last_name"
                    ),

                "title":
                    person.get(
                        "current_job_title"
                    ),

                "headline":
                    person.get(
                        "headline"
                    ),

                "linkedin":
                    person.get(
                        "linkedin_url"
                    ),

                "email":
                    email_info.get(
                        "email"
                    ),

                "email_status":
                    email_info.get(
                        "status"
                    ),

                "email_revealed":
                    email_info.get(
                        "revealed"
                    ),

                "verification_method":
                    email_info.get(
                        "verification_method"
                    ),

                "mobile":
                    mobile_info.get(
                        "mobile"
                    ),

                "mobile_status":
                    mobile_info.get(
                        "status"
                    ),

                "mobile_revealed":
                    mobile_info.get(
                        "revealed"
                    ),

                "company":
                    company.get(
                        "domain"
                    ),

                "company_name":
                    company.get(
                        "name"
                    )
            })

        return contacts

    def enrich_person(
        self,
        first_name,
        last_name,
        company_name,
        company_domain
    ):

        url = (
            f"{self.base_url}/enrich-person"
        )

        payload = {
            "data": {
                "first_name":
                    first_name,

                "last_name":
                    last_name,

                "company_name":
                    company_name,

                "company_website":
                    company_domain
            }
        }

        response = requests.post(
            url,
            headers=self.headers,
            json=payload,
            timeout=60
        )

        response.raise_for_status()

        data = response.json()

        person = data.get(
            "person",
            {}
        )

        email_info = person.get(
            "email",
            {}
        )

        mobile_info = person.get(
            "mobile",
            {}
        )

        return {

            "email":
                email_info.get(
                    "email"
                ),

            "email_revealed":
                email_info.get(
                    "revealed"
                ),

            "email_status":
                email_info.get(
                    "status"
                ),

            "verification_method":
                email_info.get(
                    "verification_method"
                ),

            "mobile":
                mobile_info.get(
                    "mobile"
                ),

            "mobile_revealed":
                mobile_info.get(
                    "revealed"
                ),

            "mobile_status":
                mobile_info.get(
                    "status"
                ),

            "linkedin":
                person.get(
                    "linkedin_url"
                ),

            "job_title":
                person.get(
                    "current_job_title"
                )
        }