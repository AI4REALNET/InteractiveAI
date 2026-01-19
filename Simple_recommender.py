import json

class SimpleRecommender:

    def _process_single_pair(self, context_json, event_json):
        """Handles a single (context, event) pair."""
        
        # Parse JSON inputs
        if isinstance(context_json, str):
            context = json.loads(context_json)
        else:
            context = context_json

        if isinstance(event_json, str):
            event = json.loads(event_json)
        else:
            event = event_json

        context_data = context.get("data", {})
        event_data = event.get("data", {})
        use_case = context.get("use_case", "Railway")

        recommendations = []

        event_type = event_data.get("event_type")
        train_id = event_data.get("id_train")
        delay = event_data.get("delay")

        # -------------------------------
        # PASSENGER EVENT
        # -------------------------------
        if event_type == "PASSENGER":
            recommendations.append({
                "title": "Passenger Malaise",
                "description": (
                    f"Train {train_id} is delayed ({delay}). "
                    "Recommend informing passengers, adjusting its schedule, "
                    "and preparing platform change if required."
                ),
                "use_case": use_case,
                "actions": [
                    {"action": "notify_passengers"},
                    {"action": "reschedule_train", "train_id": train_id},
                    {"action": "prioritize_track_allocation", "train_id": train_id}
                ]
            })

        # -------------------------------
        # INFRASTRUCTURE EVENT
        # -------------------------------
        elif event_type == "INFRASTRUCTURE":
            recommendations.append({
                "title": "Infrastructure Issue",
                "description": (
                    f"Infrastructure problem affecting train {train_id}. "
                    "Recommend rerouting and adjusting traffic flow."
                ),
                "use_case": use_case,
                "actions": [
                    {"action": "reroute_train", "train_id": train_id},
                    {"action": "inspect_track_section"},
                    {"action": "reduce_speed_zone"}
                ]
            })

        # -------------------------------
        # HARDWARE EVENT
        # -------------------------------
        elif event_type == "HARDWARE":
            recommendations.append({
                "title": "Hardware Failure Response",
                "description": (
                    f"Hardware issue on train {train_id}. "
                    "Recommend stopping the train and sending maintenance."
                ),
                "use_case": use_case,
                "actions": [
                    {"action": "stop_train", "train_id": train_id},
                    {"action": "dispatch_maintenance_team"},
                    {"action": "assist_passengers"}
                ]
            })

        # # Fallback monitoring recommendation
        # recommendations.append({
        #     "title": "System Monitoring",
        #     "description": "Continue monitoring this train and system stability.",
        #     "use_case": use_case,
        #     "actions": [
        #         {"action": "monitor_system"}
        #     ]
        # })

        return recommendations

    # ========================================================================
    # NEW: accepts several (context, event) pairs
    # ========================================================================
    def get_recommendations(self, pairs):
        """
        pairs = [
          (context_json1, event_json1),
          (context_json2, event_json2),
          ...
        ]
        """

        all_results = []

        for context_json, event_json in pairs:
            result = self._process_single_pair(context_json, event_json)
            all_results.append(result)

        return all_results