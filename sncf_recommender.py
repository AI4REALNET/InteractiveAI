
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
