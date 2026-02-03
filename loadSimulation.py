from pickle import FALSE
from time import sleep
import requests
import json
from datetime import datetime, timedelta


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


# event_payload1 = json.dumps({
# "criticality": "HIGH", #MEDIUM or LOW
#                     "title": "fake_title",
#                     "description": "fake_descp",
#                     "data": {
#                         #"simulation_name" : None,
#                         "event_type": "PASSENGER", #INFRASTRUCTURE or IMPACT or HARDWARE
#                         "id_train": "1234",
#                         "agent_id": "1",
#                         "delay": "1 hour"
#                         #"num_rame": None,
#                         #"tmp_rame": None,
#                         #"agent_position": None,
#                         #"malfunction_stop_position": None,
#                         #"travel_plan": None,
#                     },
#                     #"start_date": iso_date,
#                     #"end_date": iso_date,
#                     "use_case": "Railway"
# }
# )


# # event_data = {
# #                     "criticality": "HIGH", #MEDIUM or LOW
# #                     "title": "fake_itle"",
# #                     "description": "fake_descp",
# #                     "data": {
# #                         #"simulation_name" : None,
# #                         "event_type": "PASSENGER", #INFRASTRUCTURE or IMPACT or HARDWARE
# #                         "id_train": "1234",
# #                         #"agent_id": None,
# #                         #"num_rame": None,
# #                         #"tmp_rame": None,
# #                         #"agent_position": None,
# #                         #"malfunction_stop_position": None,
# #                         #"travel_plan": None,
# #                     },
# #                     "start_date": iso_date,
# #                     "end_date": iso_date,
# #                     "use_case": "Railway"
# #                 }




# context_payload1 = json.dumps({
# "data": {
#                 "trains": { # peut mettre plusieurs trains
#                         "id_train": "1234",
#                         #"nb_passengers_onboard": None,
#                         #"nb_passengers_connection": None,
#                         #"latitude": latitude,
#                         #"longitude": longitude,
#                         #"speed": None,
#                         "failure": "FALSE"
#                 }
#                 #"list_of_target": None,
#                 #"direction_agents": None,
#                 #"position_agents": None,
#             },
#             #"date": iso_date,
#             "use_case": "Railway",
# }
# )


# # context_data = {
# #             "data": {
# #                 "trains": { # peut mettre plusieurs trains
# #                         "id_train": "1234",
# #                         #"nb_passengers_onboard": None,
# #                         #"nb_passengers_connection": None,
# #                         "latitude": latitude,
# #                         "longitude": longitude,
# #                         #"speed": None,
# #                         "failure": FALSE
# #                 }
# #                 #"list_of_target": None,
# #                 #"direction_agents": None,
# #                 #"position_agents": None,
# #             },
# #             "date": iso_date,
# #             "use_case": "Railway",
# #         }

start_date = datetime.now() + timedelta(seconds=10)

event_payload1 = json.dumps({
"criticality": "HIGH", #MEDIUM or LOW
                    "title": "Malaise Voyageurs, Dérangement d'installation, Gare de Poitiers",
                    "description": "Malaise Voyageurs au TGV AB001. Intervention des pompiers en gare de Poitiers. Au même moment, dérangement d'installation à Poitiers accès impossible. Heure de restitution prévisible: 12h00." ,
                    "data": {
                        #"simulation_name" : None,
                        #"event_id":"1",
                        "event_type": "PASSENGER", #INFRASTRUCTURE or IMPACT or HARDWARE
                        "id_train": "AB001",
                        "agent_id": "1",
                        #"delay": "5 hour",
                        #"proba": "0.4"
                    },
                    "start_date": (start_date).isoformat(),
                    "end_date": (start_date + timedelta(hours=2)).isoformat(),
                    "use_case": "Railway"
}
)


context_payload1 = json.dumps({
"data": {
                "trains": { # peut mettre plusieurs trains
                        "id_train": "AB001",
                        "nb_passengers_onboard": "468",
                        "trajet" : "Paris/Bordeaux",
                        "arrets":"Poitiers/Bordeaux",
                        #"nb_passengers_connection": None,
                        "latitude": "46.583328",
                        "longitude": "0.33333",
                        #"speed": None,
                        "failure": "TRUE"
                }
        },  
"use_case": "Railway"     
}         
)



event_payload2 = json.dumps({
#"criticality": "HIGH", #MEDIUM or LOW
                    "title": "Caténaire arrachée ",
                    "description": "Le TGV CD001 a arraché la caténaire au niveau du poste 60 de Pliboux sur la LGV SEA. La voie est contigüe n'est pas accessible. Les trains sont détournés par la ligne classique entre Poitiers et  Angoulême. Heure de restitution prévisible d'une voie : 23h00.",
                    "data": {
                        #"simulation_name" : None,
                        #"event_id":"2",
                        "event_type": "INFRASTRUCTURE", #INFRASTRUCTURE or IMPACT or HARDWARE
                       "id_train": "AB001",
                        "latitude": "46.167",
                        "longitude": "0.127",
                        "agent_id": "1",
                        #"delay": "5 hour",
                        #"proba": "0.4"
                    },
                    "start_date": (start_date + timedelta(seconds=30)).isoformat(),
                    "end_date": (start_date + timedelta(hours=4)).isoformat(),
                    "use_case": "Railway"
}
)


context_payload2 = json.dumps({
"data": {
                "trains": { # peut mettre plusieurs trains
                        "id_train": "AB001",
                        "nb_passengers_onboard": "459",
                        "trajet" : "Paris/Bordeaux",
                        "arrets":"Angoulême/Bordeaux",
                        #"nb_passengers_connection": None,
                        #"latitude": latitude,
                        #"longitude": longitude,
                        #"speed": None,
                        "failure": "FALSE"
                }
        },  
"use_case": "Railway"     
}
)


event_payload3 = json.dumps({
"criticality": "HIGH", #MEDIUM or LOW
                    "title": "Fuite de gaz de ville",
                    "description": "Fuite de gaz au niveau de Bassens. La plateforme ferroviaire se retrouve dans le périmètre de sécurité. Les autorités décident d'interdir la circulation. Heure de restitution prévisible : 19h00.",
                    "data": {
                        #"simulation_name" : None,
                        "event_type": "INFRASTRUCTURE", #INFRASTRUCTURE or IMPACT or HARDWARE
                        #"event_id":"3",
                        "id_train": "EF004",
                        "latitude" : "44.900002",
                        "longitude" : "-0.51667 ",
                        "agent_id" : "1",
                        #"delay": "5 hour",
                        #"proba": "0.4"
                    },
                    "start_date": (start_date + timedelta(seconds=40)).isoformat(),
                    "end_date": (start_date + timedelta(hours=5)).isoformat(),
                    "use_case": "Railway"
}
)

context_payload3 = json.dumps({
"data": {
                "trains": { # peut mettre plusieurs trains
                        "id_train": "EF004",
                        "nb_passengers_onboard": "348",
                        "trajet" : "Bordeaux / Paris",
                        "arrets":"Bordeaux / Libourne/ Angoulême / Poitiers / Chatellerault",
                        #"nb_passengers_connection": None,
                        #"latitude": latitude,
                        #"longitude": longitude,
                        #"speed": None,
                        "failure": "FALSE"
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


