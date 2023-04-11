import requests

BASE_URL = "https://zenodo.org"

params = {
    'q': '3051910',
    'sort': 'mostrecent',
    'all_versions': 'true'
}

r = requests.get(BASE_URL + "/api/records/", params=params)

print(r.text)