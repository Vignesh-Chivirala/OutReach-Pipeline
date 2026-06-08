
from services.eazyreach import (
    EazyReachService
)

eazyreach = EazyReachService()

result = eazyreach.get_email(
    "https://www.linkedin.com/in/danielrmartinelli"
)

print(result)