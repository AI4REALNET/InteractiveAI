import json

class DeonticRecommender:

    def _parse_delay_hours(self, delay_str):
        """Convert '5 hour' or '1.5 hour' → float"""
        return float(delay_str.split()[0])

    def _process_single_pair(
        self,
        context_json,
        event_json,
        type,
        passengers_threshold,
        delay_threshold
    ):
        # Parse JSON
        context = json.loads(context_json) if isinstance(context_json, str) else context_json
        event = json.loads(event_json) if isinstance(event_json, str) else event_json

        context_data = context.get("data", {})
        event_data = event.get("data", {})

        train_id = event_data.get("id_train")
        event_type = event_data.get("event_type")

        passengers = int(
            context_data.get("trains", {}).get("nb_passengers_onboard", 0)
        )

        delay_hours = self._parse_delay_hours(
            event_data.get("delay", "0 hour")
        )

        passengers_threshold_val = int(passengers_threshold)
        delay_threshold_hours = self._parse_delay_hours(delay_threshold)

        exceeds_passengers = passengers > passengers_threshold_val
        exceeds_delay = delay_hours > delay_threshold_hours

        # --------------------------------------------------
        # Deontic rule selection
        # --------------------------------------------------
        if type == "passengers":
            rule_triggered = exceeds_passengers

        elif type == "delay":
            rule_triggered = exceeds_delay

        elif type == "both":
            rule_triggered = exceeds_passengers and exceeds_delay

        else:
            raise ValueError("type must be 'passengers', 'delay', or 'both'")

        severity_score = delay_hours * passengers

        recommendation = {
            "train_id": train_id,
            "event_type": event_type,
            "title": event.get("title"),
            "description": event.get("description"),
            "delay_hours": delay_hours,
            "passengers_onboard": passengers,
            "severity_score": severity_score,
            "rule_triggered": rule_triggered,
            "rule_type": type,
            "actions": self._actions_for_event(event_type)
        }

        return recommendation

    def _actions_for_event(self, event_type):
        if event_type == "PASSENGER":
            return [
                {"action": "provide_medical_assistance"},
                {"action": "inform_passengers"}
            ]
        elif event_type == "INFRASTRUCTURE":
            return [
                {"action": "reduce_speed"},
                {"action": "inspect_track"}
            ]
        elif event_type == "HARDWARE":
            return [
                {"action": "dispatch_maintenance"},
                {"action": "assist_passengers"}
            ]
        else:
            return [{"action": "monitor"}]

    # =====================================================
    # Main API
    # =====================================================
    def get_recommendations(
        self,
        pairs,
        type,
        passengers_threshold="0",
        delay_threshold="0 hour"
    ):
        """
        type: 'passengers' | 'delay' | 'both'
        passengers_threshold: string or int
        delay_threshold: string like '2 hour'
        """

        recommendations = []

        for context_json, event_json in pairs:
            rec = self._process_single_pair(
                context_json,
                event_json,
                type,
                passengers_threshold,
                delay_threshold
            )
            recommendations.append(rec)

        # --------------------------------------------------
        # Ordering:
        # 1. Rule-triggered events first
        # 2. Highest severity_score next
        # --------------------------------------------------
        recommendations.sort(
            key=lambda r: (r["rule_triggered"], r["severity_score"]),
            reverse=True
        )

        return recommendations
