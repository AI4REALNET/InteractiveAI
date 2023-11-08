from datetime import datetime

from apiflask import APIBlueprint
from apiflask.views import MethodView
from cab_common_auth.decorators import get_use_cases, protected
from flask import request
from settings import logger

from .schemas import ContextIn, ContextOut

api_bp = APIBlueprint("context-api", __name__, url_prefix="/api/v1")


class HealthCheck(MethodView):
    def get(self):
        return {"message": "Ok"}


class Context(MethodView):
    @api_bp.output(ContextOut)
    @protected
    def get(self, date):
        """Get a context"""
        from flask import current_app

        use_case_factory = current_app.use_case_factory
        use_cases = get_use_cases()
        context_list = []
        for use_case in use_cases:
            context_manager = use_case_factory.get_context_manager(use_case)
            context_list.append(context_manager.get_context_with_date(date))
        return context_list


class Contexts(MethodView):
    @api_bp.output(ContextOut(many=True))
    @protected
    def get(self):
        """Get all contexts"""

        def get_context_list(use_case_factory, date_query_param, use_cases):
            context_list = []

            for use_case in use_cases:
                context_manager = use_case_factory.get_context_manager(
                    use_case
                )
                if date_query_param:
                    context_r = context_manager.get_contexts_with_date(
                        date_query_param
                    )
                else:
                    context_r = [context_manager.get_context()]
                context_list = context_list + context_r
            return context_list

        from flask import current_app

        use_case_factory = current_app.use_case_factory
        date_query_param = request.args.get("date")
        use_case_query_param = request.args.get("use_case")
        use_cases = get_use_cases()
        logger.error(use_cases)
        logger.error(use_case_query_param)

        if use_case_query_param and (use_case_query_param in use_cases):
            use_cases = [use_case_query_param]

        context_list = get_context_list(
            use_case_factory, date_query_param, use_cases
        )

        return context_list

    @api_bp.input(ContextIn)
    @api_bp.output(ContextOut, status_code=201)
    @protected
    def post(self, data):
        """Add an context"""
        from flask import current_app

        use_case_factory = current_app.use_case_factory
        use_case = data.get("use_case")
        context_manager = use_case_factory.get_context_manager(use_case)
        return context_manager.set_context(data)


api_bp.add_url_rule("/health", view_func=HealthCheck.as_view("health"))
api_bp.add_url_rule(
    "/context/<string:date>", view_func=Context.as_view("context")
)
api_bp.add_url_rule("/contexts", view_func=Contexts.as_view("contexts"))
