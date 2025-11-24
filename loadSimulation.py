from pickle import FALSE
from time import sleep
import requests
import json

print("test")

username = "railway_user"
password = "test"

# server_url = "192.168.210.29"
server_url = "192.168.209.192"

client_id = "opfab-client"
token_url = f"http://{server_url}:3200/auth/token"
events_url = f"http://{server_url}:3200/cab_event/api/v1/events"
context_url = f"http://{server_url}:3200/cabcontext/api/v1/contexts"

token_payload = f"username={username}&password={password}&grant_type=password&clientId={client_id}"
token_headers = {
    'Content-Type': 'application/x-www-form-urlencoded'
}
req_token = requests.post(token_url, headers=token_headers, data=token_payload)

# Check if request was successful
if req_token.status_code > 500:
    raise ValueError(f"Token request failed with status code {req_token.status_code}")

# Extract and return access token
access_token = json.loads(req_token.text)['access_token']
token_type = json.loads(req_token.text)['token_type']
token =  token_type + ' ' + access_token


event_payload1 = json.dumps({
  "criticality": "HIGH",
  "title": "06 78 83 09 89",
  "description": "Feu",
  "data": {
    "call_id": "1",
    "urgence": "LOW",
    "numero_number": "06 78 83 09 89",
  },
  "use_case": "Railway",
  "is_active": False,
}
)



context_payload1 = json.dumps({
    "data" : {
        "FillForm": {
        "FirstName":"Chloé",
        "LastName": "DESCHAMPS",
        "PhoneNumber": "06 78 89 90 91",
        "Address": "Rue Saint-Exupéry, 18520 Avord ",
        "AccessMean": "Rocade sortie 34" ,
        "CallNature": "ACCIDENT DE LA ROUTE",
        "AdviceCallNature2": "ACCIDENT DE LA ROUTE",
        "AdviceCallNature3": "BLESSURE GRAVE",
        "AggravationRisk": "  Explosion avec l'essence",
        "Observations": "Deux véhicules impliqués, choc frontal",
        "SMURQuantity": 2,
        "FirefighterQuantity":1,
        "AdviceSMUR2":1,
        "AdviceFirefighter2":2,
        "AdviceSMUR3":3,
        "AdviceFirefighter3":0
        }
    },
    "use_case": "Railway"
}
)

event_headers = {
            'Authorization': token,
            'Content-Type': 'application/json'
        }
# Les contexts

response1 = requests.request('POST', context_url, headers=event_headers, data=context_payload1)
response2 = requests.request('POST', events_url, headers=event_headers, data=event_payload1)

print("Context status:", response1.status_code, response1.text)
print("Event status:", response2.status_code, response2.text)


