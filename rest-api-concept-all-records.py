import requests
import pandas

BASE_URL = "https://zenodo.org"

params = {
    'q': 'conceptrecid:1213050',
    
    'sort': 'bestmatch',
    'all_versions': 'true',
    'exact': 'true'
}

r = requests.get(BASE_URL + "/api/records/", params=params)

df = r.json()

concept_records = pandas.json_normalize(r.json()['hits']['hits'])

print(concept_records)