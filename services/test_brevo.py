import sys
import os

sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)
# tests/test_brevo.py

from services.brevo import (
    BrevoService
)

brevo = BrevoService()

result = brevo.send_email(
    recipient="your_actual_email@gmail.com",
    subject="Brevo API Test",
    body="Hello from Ocean + Prospeo automation."
)

print(result)