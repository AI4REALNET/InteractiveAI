import json

class RiskRecommender:

    def _parse_delay_hours(self, delay_str):
        """Extract numeric hours from delay string like '5 hour' or '1.5 hour'"""
        return float(delay_str.split()[0])

    def _process_single_pair(self, context_json, event_json):
        # Parse JSON inputs
        context = json.loads(context_json) if isinstance(context_json, str) else context_json
        event = json.loads(event_json) if isinstance(event_json, str) else event_json

        context_data = context.get("data", {})
        event_data = event.get("data", {})
        use_case = context.get("use_case", "Railway")

        # Extract values
        train_id = event_data.get("id_train")
        event_type = event_data.get("event_type")

        delay_hours = self._parse_delay_hours(event_data.get("delay", "0 hour"))
        proba = float(event_data.get("proba", 0))

        passengers = int(
            context_data.get("trains", {}).get("nb_passengers_onboard", 0)
        )

        # Risk computation
        total_risk = delay_hours * passengers * proba

        # Print required message
        print(f"total risk estimated = {total_risk}")

        # Build recommendation
        recommendation = {
            "train_id": train_id,
            "event_type": event_type,
            "title": event.get("title"),
            "description": event.get("description"),
            "use_case": use_case,
            "total_risk": total_risk,
            "actions": self._actions_for_event(event_type)
        }

        return recommendation

    def _actions_for_event(self, event_type):
        """Simple action templates per event type"""
        if event_type == "PASSENGER":
            return [
                {"action": "provide_medical_assistance"},
                {"action": "inform_passengers"},
                {"action": "adjust_schedule"}
            ]
        elif event_type == "INFRASTRUCTURE":
            return [
                {"action": "reduce_speed"},
                {"action": "inspect_track"},
                {"action": "reroute_if_needed"}
            ]
        elif event_type == "HARDWARE":
            return [
                {"action": "dispatch_maintenance"},
                {"action": "assist_passengers"},
                {"action": "prepare_train_swap"}
            ]
        else:
            return [{"action": "monitor"}]

    # ==========================================================
    # Main entry point
    # ==========================================================
    def get_recommendations(self, pairs):
        """
        pairs = [(context1, event1), (context2, event2), ...]
        """

        recommendations = []

        for context_json, event_json in pairs:
            rec = self._process_single_pair(context_json, event_json)
            recommendations.append(rec)

        # Sort by total_risk (highest first)
        recommendations.sort(
            key=lambda r: r["total_risk"],
            reverse=True
        )

        return recommendations
