from apiflask import APIBlueprint
from cab_common_auth.decorators import get_use_cases, protected
from flask import request
from flask.views import MethodView

from .context_manager.da_context_manager import DAContextManager
from .context_manager.orange_context_manager import OrangeContextManager
from .context_manager.rte_context_manager import RTEContextManager
from .context_manager.sncf_context_manager import SNCFContextManager
from .schemas import ContextIn, ContextOut
from .utils import UseCaseFactory

api_bp = APIBlueprint("context-api", __name__, url_prefix="/api/v1")

use_case_factory = UseCaseFactory()
use_case_factory.register_use_case('DA', DAContextManager())
use_case_factory.register_use_case('RTE', RTEContextManager())
use_case_factory.register_use_case('ORANGE', OrangeContextManager())
use_case_factory.register_use_case('SNCF', SNCFContextManager())


class HealthCheck(MethodView):

    def get(self):
        return {'message': 'Ok'}


class Context(MethodView):

    @api_bp.output(ContextOut)
    @protected
    def get(self, date):
        """Get a context"""
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
        date_query_param = request.args.get('date')
        use_cases = get_use_cases()
        context_list = []

        for use_case in use_cases:
            context_manager = use_case_factory.get_context_manager(use_case)
            if date_query_param:
                context = context_manager.get_contexts_with_date(
                    date_query_param)
            else:
                context = context_manager.get_context()
            context_list.append(context)

        return context_list

    @api_bp.input(ContextIn)
    @api_bp.output(ContextOut, status_code=201)
    @protected
    def post(self, data):
        """Add an context"""
        use_case = data.get("use_case")
        context_manager = use_case_factory.get_context_manager(use_case)
        return context_manager.set_context(data)


api_bp.add_url_rule("/health", view_func=HealthCheck.as_view("health"))
api_bp.add_url_rule('/context/<string:date>',
                    view_func=Context.as_view('context'))
api_bp.add_url_rule("/contexts", view_func=Contexts.as_view("contexts"))
