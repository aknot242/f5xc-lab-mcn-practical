import azure.functions as func # pylint: disable=all
from app import app

def main(req: func.HttpRequest, context: func.Context) -> func.HttpResponse:
    """azure handler"""
    return func.WsgiMiddleware(app.wsgi_app).handle(req, context)
