import requests
from requests.auth import HTTPBasicAuth

session = requests.Session()

auth = HTTPBasicAuth("Vinylon", "password")

response = session.post(
    "http://pythonscraping.com/pages/auth/login.php",
    auth=auth,
)

print(response.text)
