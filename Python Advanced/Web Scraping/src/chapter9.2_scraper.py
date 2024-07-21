import requests

# params = {"username": "Vinylon", "password": "password"}

# response = requests.post(
#     "https://pythonscraping.com/pages/cookies/welcome.php",
#     data=params,
# )
# print("Cookie is set to:")
# print(response.cookies.get_dict())
# print("Going to profile page...")
# response = requests.get(
#     "http://pythonscraping.com/pages/cookies/profile.php", cookies=response.cookies
# )
# print(response.text)

session = requests.Session()

params = {"username": "Vinylon", "password": "password"}

response = session.post(
    "https://pythonscraping.com/pages/cookies/welcome.php",
    data=params,
)
print("Cookie is set to:")
print(response.cookies.get_dict())
print("Going to profile page...")
response = session.get("http://pythonscraping.com/pages/cookies/profile.php")
print(response.text)
