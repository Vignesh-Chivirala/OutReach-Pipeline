
import csv

from services.ocean import OceanService
from services.prospeo import ProspeoService
from services.brevo import BrevoService


TEST_MODE = True

TEST_EMAIL = "chvignesh2006@gmail.com"


def generate_email(contact):

    return f"""
Hi {contact['first_name']},

I came across {contact['company_name']} while researching companies in your industry.

I was impressed by your work and wanted to introduce myself.

I'm currently building automation solutions that help businesses streamline lead generation and outreach workflows.

Would you be open to a brief conversation?

Best regards,
Vignesh
"""


def main():

    seed_domain = input(
        "Enter company domain: "
    ).strip()

    ocean = OceanService()
    prospeo = ProspeoService()
    brevo = BrevoService()

    try:

        companies = ocean.get_company_domains(
            seed_domain,
            limit=5
        )

        if not companies:

            print(
                "No similar companies found."
            )
            return

        print(
            "\n=== Similar Companies ==="
        )

        for company in companies:

            print(
                f"- {company}"
            )

        confirm = input(
            "\nSend outreach emails? (y/n): "
        )

        if confirm.lower() != "y":

            print(
                "Cancelled."
            )
            return

        sent_count = 0

        sent_emails = set()

        with open(
            "leads.csv",
            "w",
            newline="",
            encoding="utf-8"
        ) as file:

            writer = csv.writer(
                file
            )

            writer.writerow([
                "Name",
                "Company",
                "Email",
                "LinkedIn"
            ])

        for company in companies:

            print(
                f"\nProcessing company: {company}"
            )

            try:

                contacts = (
                    prospeo.search_decision_makers(
                        company
                    )
                )

                if not contacts:

                    print(
                        "No contacts found."
                    )
                    continue

                for contact in contacts[:3]:

                    try:

                        print(
                            f"\nEnriching {contact['name']}..."
                        )

                        enriched = (
                            prospeo.enrich_person(
                                contact["first_name"],
                                contact["last_name"],
                                contact["company_name"],
                                contact["company"]
                            )
                        )

                        if not enriched.get(
                            "email_revealed"
                        ):

                            print(
                                "Email not revealed."
                            )
                            continue

                        email = enriched.get(
                            "email"
                        )

                        if not email:

                            print(
                                "No email found."
                            )
                            continue

                        if email in sent_emails:

                            print(
                                f"Duplicate email skipped: {email}"
                            )
                            continue

                        sent_emails.add(
                            email
                        )

                        print(
                            f"Found email: {email}"
                        )

                        with open(
                            "leads.csv",
                            "a",
                            newline="",
                            encoding="utf-8"
                        ) as file:

                            writer = csv.writer(
                                file
                            )

                            writer.writerow([
                                contact["name"],
                                contact["company_name"],
                                email,
                                enriched["linkedin"]
                            ])

                        subject = (
                            f"Automation idea for "
                            f"{contact['company_name']}"
                        )

                        body = generate_email(
                            contact
                        )

                        recipient = (
                            TEST_EMAIL
                            if TEST_MODE
                            else email
                        )

                        response = (
                            brevo.send_email(
                                recipient=recipient,
                                subject=subject,
                                body=body
                            )
                        )

                        print(
                            f"Email sent to: {recipient}"
                        )

                        print(
                            response
                        )

                        sent_count += 1

                    except Exception as e:

                        print(
                            f"Contact Error: {e}"
                        )

            except Exception as e:

                print(
                    f"Company Error: {e}"
                )

        print(
            "\n======================"
        )

        print(
            f"Total Emails Sent: {sent_count}"
        )

        print(
            "Leads saved to leads.csv"
        )

        print(
            "======================"
        )

    except Exception as e:

        print(
            f"Pipeline Error: {e}"
        )


if __name__ == "__main__":
    main()