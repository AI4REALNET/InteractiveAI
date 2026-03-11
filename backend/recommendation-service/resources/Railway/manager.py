# backend/recommendation-service/resources/Railway/manager.py
import json
from api.manager.base_manager import BaseRecommendationManager
from .mockRecommendations.mockRecommendations import RECOMMENDATION_CATALOG

import logging

logger = logging.getLogger(__name__)

class RailwayManager(BaseRecommendationManager):
    def __init__(self):
        super().__init__()

    def _transform_recommendation(self, reco_json):
        """Transform a recommendation from catalog to output format."""
        reco = json.loads(reco_json)
        return {
            "title": reco["data"]["title"],
            "description": reco["data"]["description"],
            "use_case": reco["data"]["use_case"],
            "agent_type": reco["data"]["agent_type"],
            "actions": [{}],
            "kpis": reco["data"]["kpis"],
        }

    def get_recommendation(self, request_data):
        """
        Override to provide recommendations specific to the Railway use case.
        
        This method generates and returns recommendations tailored for Railway events.
        """
        event_data = request_data.get("event", {})
        event_id = str(event_data.get("id_event", "1"))

        logger.info(f"Processing event_id: {event_id}")

        # Get recommendations from catalog 
        if event_id == "1":
            recommendations = RECOMMENDATION_CATALOG.get(event_id, RECOMMENDATION_CATALOG["1"])
        elif event_id == "2":
            recommendations = RECOMMENDATION_CATALOG.get(event_id, RECOMMENDATION_CATALOG["1"])
        elif event_id == "3":
            recommendations = RECOMMENDATION_CATALOG.get(event_id, RECOMMENDATION_CATALOG["1"])
        # Transform each recommendation to output format
        return [self._transform_recommendation(reco) for reco in recommendations]
    

