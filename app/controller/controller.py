from flask_restx import Namespace

from ..routes.user_routes import user_routes
from ..routes.ai_routes import ai_routes
from ..routes.auth_routes import auth_routes

authorizations = {"Bearer": {"type": "apiKey", "in": "header", "name": "Authorization"}}

def register_namespaces(api):
    user_ns = Namespace("user")
    auth_ns = Namespace("auth", authorizations= authorizations)
    ai_ns = Namespace("ai")

    user_routes(user_ns)
    auth_routes(auth_ns)
    ai_routes(ai_ns)

    api.add_namespace(user_ns)
    api.add_namespace(auth_ns)
    api.add_namespace(ai_ns)