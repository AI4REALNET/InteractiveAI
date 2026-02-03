
import json

def SNCF_RECO(pairs):
    all_results = []

    for context_json, event_json in pairs:
        context = json.loads(context_json)
        event = json.loads(event_json)

        event_type = event.get("data", {}).get("event_type")
        train_id = event.get("data", {}).get("id_train")

        # --------------------------------------------------
        # PASSENGER EVENT → Case 1
        # --------------------------------------------------
        if event_type == "PASSENGER":

            recos = [
                {"data": {
                    "reco_name": "Retenir en gare à St Pierre des Corps",
                    "description": "Retenir le train en gare à St Pierre des Corps jusqu' à la restitution des voies.",
                    "coût individuel": "78",
                    "nb passagers impactés": "468",
                    "coût total": "32838",
                    "retard": "1h30",
                    "Meilleure": "True"
                }},
                {"data": {
                    "reco_name": "Retarder",
                    "description": "Retenir le train en pleine voie jusqu'à la restitution des voies. Mise en place de moyens pour la prise en charge des clients",
                    "coût individuel": "87",
                    "nb passagers impactés": "398",
                    "coût total": "34626",
                    "retard": "1h30",
                    "Meilleure": "False"
                }},
                {"data": {
                    "reco_name": "Modifier parcours",
                    "description": "Détournement des trains. Les clients à destination et au départ de Poitiers sont pris en charge.",
                    "coût individuel": "102",
                    "nb passagers impactés": "350",
                    "coût total": "35700",
                    "retard": "1h40",
                    "Meilleure": "False"
                }},
                {"data": {
                    "reco_name": "Supprimer",
                    "description": "Suppression des trains. Les clients sont invités à reporter leur voyage.",
                    "coût individuel": "233",
                    "nb passagers impactés": "468",
                    "coût total": "109044",
                    "retard": "1h45",
                    "Meilleure": "False"
                }}
            ]

        # --------------------------------------------------
        # HARDWARE EVENT → Case 2
        # --------------------------------------------------
        elif event_type == "HARDWARE":

            recos = [
                {"data": {
                    "reco_name": "Retenir en gare",
                    "description": "Retenir le train en gare de Poitiers jusqu' à la restitution des voies.",
                    "coût individuel": "123",
                    "nb passagers impactés": "459",
                    "coût total": "56457",
                    "retard": "1h05",
                    "Meilleure": "False"
                }},
                {"data": {
                    "reco_name": "Retarder",
                    "description": "Retenir le train en pleine voie jusqu'à la restitution des voies. Mise en place de moyens pour la prise en charge des clients",
                    "coût individuel": "129",
                    "nb passagers impactés": "459",
                    "coût total": "59211",
                    "retard": "1h00",
                    "Meilleure": "False"
                }},
                {"data": {
                    "reco_name": "Modifier parcours",
                    "description": "Rebroussement et détournement des trains par la ligne classique entre Angoulême et Poitiers.",
                    "coût individuel": "73",
                    "nb passagers impactés": "459",
                    "coût total": "33507",
                    "retard": "1h00",
                    "Meilleure": "True"
                }},
                {"data": {
                    "reco_name": "Supprimer",
                    "description": "Suppression des trains. Les clients sont invités à reporter leur voyage.",
                    "coût individuel": "221",
                    "nb passagers impactés": "459",
                    "coût total": "101439",
                    "retard": "1h00",
                    "Meilleure": "False"
                }}
            ]

        # --------------------------------------------------
        # INFRASTRUCTURE EVENT → Case 3
        # --------------------------------------------------
        elif event_type == "INFRASTRUCTURE":

            recos = [
                {"data": {
                    "reco_name": "Attente en gare de Bordeaux",
                    "description": "Retenir le train en gare jusqu' à la restitution des voies.",
                    "coût individuel": "94",
                    "nb passagers impactés": "348",
                    "coût total": "32712",
                    "retard": "00h30",
                    "Meilleure": "True"
                }},
                {"data": {
                    "reco_name": "Retarder",
                    "description": "Retenir le train en pleine voie jusqu'à la restitution des voies. Mise en place de moyens pour la prise en charge des clients",
                    "coût individuel": "94",
                    "nb passagers impactés": "347",
                    "coût total": "32618",
                    "retard": "00h53",
                    "Meilleure": "False"
                }},
                {"data": {
                    "reco_name": "Détournement de Bordeaux à Angoulême",
                    "description": "Rebroussement et détournement des trains par la ligne classique entre Angoulême et Poitiers.",
                    "coût individuel": "95",
                    "nb passagers impactés": "348",
                    "coût total": "33060",
                    "retard": "1h24",
                    "Meilleure": "False"
                }},
                {"data": {
                    "reco_name": "Supprimer",
                    "description": "Suppression des trains. Les clients sont invités à reporter leur voyage.",
                    "coût individuel": "257",
                    "nb passagers impactés": "348",
                    "coût total": "89436",
                    "retard": "00h40",
                    "Meilleure": "False"
                }}
            ]

        else:
            recos = [{"data": {"reco_name": "Aucune recommandation disponible"}}]

        all_results.append({
            "train_id": train_id,
            "event_type": event_type,
            "event_title": event.get("title"),
            "recommendations": recos
        })

    return all_results


#test = 1




def SNCF_RECO1(pairs):
    """
    pairs: list of (context_json, event_json) tuples, in chronological order
    Returns: list of dictionaries with train_id, event_title, and ordered recommendations
    """
    
    # Predefined recommendations mapped to train_id + event_type
    predefined_recos = {
        ("AB001", "PASSENGER"): [Reco11, Reco12, Reco13, Reco14],
        ("AB001", "INFRASTRUCTURE"):  [Reco21, Reco22, Reco23, Reco24],
        ("EF004", "INFRASTRUCTURE"): [Reco31, Reco32, Reco33, Reco34],
    }
    
    all_results = []
    
    for context_json, event_json in pairs:
        context = json.loads(context_json)
        event = json.loads(event_json)
        
        train_id = event["data"]["id_train"]
        event_type = event["data"]["event_type"]
        
        key = (train_id, event_type)
        recos = predefined_recos.get(key, [{"data": {"title": "Aucune recommandation disponible"}}])
        
        # Sort so that the "best" recommendation appears first
        def best_first(reco_json):
            reco = json.loads(reco_json)
            return 0 if reco["data"]["kpis"].get("best") == "True" else 1
        
        ordered_recos = sorted(recos, key=best_first)
        
        all_results.append({
            "train_id": train_id,
            "event_title": event.get("title"),
            "event_start": event.get("start_date"),
            "recommendations": ordered_recos
        })
    
    # Optional: sort all_results chronologically by event_start
    all_results.sort(key=lambda x: datetime.fromisoformat(x["event_start"]) if x["event_start"] else datetime.min)
    
    return all_results





def SNCF_RECO2(event_payload, context_payload):
    """
    Takes event and context JSON strings, identifies the scenario, 
    and returns the associated recommendations sorted by 'best=True' first.
    """
    
    # 1. Parse the input payloads
    try:
        event = json.loads(event_payload)
        context = json.loads(context_payload)
    except json.JSONDecodeError as e:
        return f"Error decoding JSON: {e}"

    # 2.  hardcoded recommendations
    
    # Scenario 1 Recos
    recos_scenario_1 = [
        json.dumps({"data": {"title": "Retenir en gare à St Pierre des Corps", "description": "Retenir le train en gare à St Pierre des Corps jusqu' à la restitution des voies.", "use_case": "Railway", "agent_type": "AI", "kpis": {"cost": "78", "nb_impacted_passengers": "468", "total_cost": "32838", "delay": "1h30", "best": "True"}}}),
        json.dumps({"data": {"title": "Retarder", "description": "Retenir le train en pleine voie jusqu'à la restitution des voies. Mise en place de moyens pour la prise en charge des clients ", "use_case": "Railway", "agent_type": "AI", "kpis": {"cost": "87", "nb_impacted_passengers": "398", "total_cost": "34626", "delay": "1h30", "best": "False"}}}),
        json.dumps({"data": {"title": "Modifier parcours", "description": "Détournement des trains. Les clients à destination et au départ de Poitiers sont pris en charge.", "use_case": "Railway", "agent_type": "AI", "kpis": {"cost": "102", "nb_impacted_passengers": "350", "total_cost": "35700", "delay": "1h40", "best": "False"}}}),
        json.dumps({"data": {"title": "Supprimer", "description": "Suppression des trains. Les clients sont invités à reporter leur voyage.", "use_case": "Railway", "agent_type": "AI", "kpis": {"cost": "233", "nb_impacted_passengers": "468", "total_cost": "109044", "delay": "1h45", "best": "False"}}})
    ]

    # Scenario 2 Recos
    recos_scenario_2 = [
        json.dumps({"data": {"title": "Retenir en gare", "description": "Retenir le train en gare de Poitiers jusqu' à la restitution des voies.", "use_case": "Railway", "agent_type": "AI", "kpis": {"cost": "123", "nb_impacted_passengers": "459", "total_cost": "56457", "delay": "1h05", "best": "False"}}}),
        json.dumps({"data": {"title": "Retarder", "description": "Retenir le train en pleine voie jusqu'à la restitution des voies. Mise en place de moyens pour la prise en charge des clients ", "use_case": "Railway", "agent_type": "AI", "kpis": {"cost": "129", "nb_impacted_passengers": "459", "total_cost": "59211", "delay": "1h00", "best": "False"}}}),
        json.dumps({"data": {"title": "Modifier parcours", "description": "Rebroussement et détournement des trains par la ligne classique entre Angoulême et Poitiers . ", "use_case": "Railway", "agent_type": "AI", "kpis": {"cost": "73", "nb_impacted_passengers": "459", "total_cost": "33507", "delay": "1h00", "best": "True"}}}),
        json.dumps({"data": {"title": "Supprimer", "description": "Suppression des trains. Les clients sont invités à reporter leur voyage.", "use_case": "Railway", "agent_type": "AI", "kpis": {"cost": "221", "nb_impacted_passengers": "459", "total_cost": "101439", "delay": "1h00", "best": "False"}}})
    ]

    # Scenario 3 Recos
    recos_scenario_3 = [
        json.dumps({"data": {"title": "Attendre en gare de Bordeaux", "description": "Retenir le train en gare jusqu' à la restitution des voies.", "use_case": "Railway", "agent_type": "AI", "kpis": {"cost": "94", "nb_impacted_passengers": "348", "total_cost": "32712", "delay": "00h30", "best": "True"}}}),
        json.dumps({"data": {"title": "Retarder", "description": "Retenir le train en pleine voie jusqu'à la restitution des voies. Mise en place de moyens pour la prise en charge des clients ", "use_case": "Railway", "agent_type": "AI", "kpis": {"cost": "94", "nb_impacted_passengers": "347", "total_cost": "32618", "delay": "00h53", "best": "False"}}}),
        json.dumps({"data": {"title": "Détourner de Bordeaux à Angoulême ", "description": "Rebroussement et détournement des trains par la ligne classique entre Angoulême et Poitiers . ", "use_case": "Railway", "agent_type": "AI", "kpis": {"cost": "95", "nb_impacted_passengers": "348", "total_cost": "33060", "delay": "1h24", "best": "False"}}}),
        json.dumps({"data": {"title": "Supprimer", "description": "Suppression des trains. Les clients sont invités à reporter leur voyage.", "use_case": "Railway", "agent_type": "AI", "kpis": {"cost": "257", "nb_impacted_passengers": "348", "total_cost": "89436", "delay": "00h40", "best": "False"}}})
    ]

    # 3. Determine which Scenario matches the Event
    # We match based on the Event Title or specific characteristics
    event_title = event.get("title", "")
    target_recos_raw = []

    if "Malaise Voyageurs" in event_title:
        target_recos_raw = recos_scenario_1
    elif "Caténaire arrachée" in event_title:
        target_recos_raw = recos_scenario_2
    elif "Fuite de gaz" in event_title:
        target_recos_raw = recos_scenario_3
    else:
        return "Unknown Event: No recommendations found."

    # 4. Parse the raw recommendation strings into dictionaries
    parsed_recos = [json.loads(r) for r in target_recos_raw]

    # 5. Sort the recommendations
    # Logic: We want "best": "True" to be at the top (Index 0).
    # Since "True" > "False" in Python string comparison, we sort Descending (reverse=True).
    sorted_recos = sorted(
        parsed_recos, 
        key=lambda x: x['data']['kpis']['best'], 
        reverse=True
    )

    return sorted_recos




def SNCF_RECO3(event_json, context_json, recommendation_catalog):
    """
    Selects recommendations using IF–THEN rules based on event_id.
    
    Input:
        event_json (str)   : Event payload in JSON string format
        context_json (str) : Context payload (not used in rules but kept for extensibility)
    
    Output:
        List of 4 recommendation JSON strings ordered with best=True first
    """

    event = json.loads(event_json)
    context = json.loads(context_json)  # Currently unused but available if rules expand
    
    event_id = event["data"].get("event_id")

    if event_id not in recommendation_catalog:
            return [{"error": f"No recommendations defined for event_id {event_id}"}]

    recos = recommendation_catalog[event_id]

    # ------------- ORDER: BEST FIRST ----------------- #
    def best_first(reco_json):
        reco = json.loads(reco_json)
        return 0 if reco["data"]["kpis"].get("best") == "True" else 1

    ordered_recommendations = sorted(recos, key=best_first)

    return ordered_recommendations



