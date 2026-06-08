from services.ocean import OceanService

ocean = OceanService()

try:

    domains = ocean.get_company_domains(
        "openai.com"
    )

    print(
        "\n=== Similar Company Domains ===\n"
    )

    for d in domains:
        print(d)

except Exception as e:

    print(
        "\nError:"
    )

    print(e)