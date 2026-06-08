import sys
import os

sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)


from services.prospeo import ProspeoService

prospeo = ProspeoService()

result = prospeo.enrich_person(
    first_name="Corina",
    last_name="Mack",
    company_name="Patrice and Associates Franchising",
    company_domain="patriceandassociates.com"
)

print(result)