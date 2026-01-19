import json

class RecommenderSystem:
    def __init__(self):
        pass  # Here initialize models, heuristics, etc.

    # def get_recommended_transport_plan(self, context_data, event_data, target_ids):
    #     # Fake transport plan for demonstration
    #     return {
    #         "plan_type": "reroute",
    #         "targets": target_ids,
    #         "note": "This is a placeholder transport plan."
    #     }

    def run_idle(self, context_data, event_data):
        # Return fake idle targets
        return [0]  # Example placeholder

    def recommend(self, context_data, event_data, models=None):
        # Generate extra recommendations (fake)
        return [
            {
                "title": "Extra Recommendation",
                "description": "This is an AI/Heuristic generated recommendation.",
                "use_case": context_data.get("use_case", "Unknown"),
                "agent_type": "AI",
                "actions": [{"plan_type": "monitor", "targets": [1, 2]}],
            }
        ]

    def get_recommendation(self, context_json, event_json):
        # Parse JSON if input is string
        if isinstance(context_json, str):
            context_data = json.loads(context_json).get("data", {})
        else:
            context_data = context_json.get("data", {})

        if isinstance(event_json, str):
            event_data = json.loads(event_json).get("data", {})
        else:
            event_data = event_json.get("data", {})

        all_recommendations = []

        # Recommendations based on event_type
        if event_data.get("event_type") == "PASSENGER":
            fake_targets_ids_1 = [3, 36, 36]
            fake_transport_plan_1 = self.get_recommended_transport_plan(
                context_data, event_data, fake_targets_ids_1
            )
            all_recommendations.append({
                "title": "Adjust passenger stops",
                "description": "Consider adjusting stops for affected trains.",
                "use_case": context_json.get("use_case", "Railway"),
                "agent_type": "Fake",
                "actions": [fake_transport_plan_1],
            })

        elif event_data.get("event_type") == "INFRASTRUCTURE":
            fake_targets_ids_1 = [33, 33, 33, 30]
            fake_transport_plan_1 = self.get_recommended_transport_plan(
                context_data, event_data, fake_targets_ids_1
            )
            all_recommendations.append({
                "title": "Banalisation",
                "description": "Adjust train routes for infrastructure issues.",
                "use_case": context_json.get("use_case", "Railway"),
                "agent_type": "Fake",
                "actions": [fake_transport_plan_1],
            })

        # Always provide a generic suppression recommendation
        fake_targets_ids_2 = self.run_idle(context_data, event_data)
        fake_transport_plan_2 = self.get_recommended_transport_plan(
            context_data, event_data, fake_targets_ids_2
        )
        all_recommendations.append({
            "title": "Suppression",
            "description": "Suppress affected trains. Advise passengers to reschedule.",
            "use_case": context_json.get("use_case", "Railway"),
            "agent_type": "Fake",
            "actions": [fake_transport_plan_2],
        })

        # Add AI/Heuristic generated recommendations
        extra_recommendations = self.recommend(context_data, event_data, models=["AI", "Heuristic"])
        all_recommendations.extend(extra_recommendations)

        return all_recommendations


# Example usage
recommender = RecommenderSystem()
recommendations = recommender.get_recommendation(context_payload1, event_payload1)
print(json.dumps(recommendations, indent=2))
