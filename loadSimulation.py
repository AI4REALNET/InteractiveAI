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
"criticality": "HIGH", #MEDIUM or LOW
                    "title": "fake_title",
                    "description": "fake_descp",
                    "data": {
                        #"simulation_name" : None,
                        "event_type": "PASSENGER", #INFRASTRUCTURE or IMPACT or HARDWARE
                        "id_train": "1234",
                        "agent_id": "1",
                        "delay": "1 hour"
                        #"num_rame": None,
                        #"tmp_rame": None,
                        #"agent_position": None,
                        #"malfunction_stop_position": None,
                        #"travel_plan": None,
                    },
                    #"start_date": iso_date,
                    #"end_date": iso_date,
                    "use_case": "Railway"
}
)


# event_data = {
#                     "criticality": "HIGH", #MEDIUM or LOW
#                     "title": "fake_itle"",
#                     "description": "fake_descp",
#                     "data": {
#                         #"simulation_name" : None,
#                         "event_type": "PASSENGER", #INFRASTRUCTURE or IMPACT or HARDWARE
#                         "id_train": "1234",
#                         #"agent_id": None,
#                         #"num_rame": None,
#                         #"tmp_rame": None,
#                         #"agent_position": None,
#                         #"malfunction_stop_position": None,
#                         #"travel_plan": None,
#                     },
#                     "start_date": iso_date,
#                     "end_date": iso_date,
#                     "use_case": "Railway"
#                 }




context_payload1 = json.dumps({
"data": {
                "trains": { # peut mettre plusieurs trains
                        "id_train": "1234",
                        #"nb_passengers_onboard": None,
                        #"nb_passengers_connection": None,
                        #"latitude": latitude,
                        #"longitude": longitude,
                        #"speed": None,
                        "failure": "FALSE"
                }
                #"list_of_target": None,
                #"direction_agents": None,
                #"position_agents": None,
            },
            #"date": iso_date,
            "use_case": "Railway",
}
)


# context_data = {
#             "data": {
#                 "trains": { # peut mettre plusieurs trains
#                         "id_train": "1234",
#                         #"nb_passengers_onboard": None,
#                         #"nb_passengers_connection": None,
#                         "latitude": latitude,
#                         "longitude": longitude,
#                         #"speed": None,
#                         "failure": FALSE
#                 }
#                 #"list_of_target": None,
#                 #"direction_agents": None,
#                 #"position_agents": None,
#             },
#             "date": iso_date,
#             "use_case": "Railway",
#         }








event_headers = {
            'Authorization': token,
            'Content-Type': 'application/json'
        }
# Les contexts

response1 = requests.request('POST', context_url, headers=event_headers, data=context_payload1)
response2 = requests.request('POST', events_url, headers=event_headers, data=event_payload1)

print("Context status:", response1.status_code, response1.text)
print("Event status:", response2.status_code, response2.text)


