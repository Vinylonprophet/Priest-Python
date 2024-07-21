import requests

params = {"firstname": "Wu", "lastname": "Vinylon"}

response = requests.post(
    "https://pythonscraping.com/pages/files/processing.php",
    data=params,
)
print(response.text)
