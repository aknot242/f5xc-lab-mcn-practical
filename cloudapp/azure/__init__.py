import azure.functions as func # pylint: disable=all
from ..app import create_app

app = create_app()

def main(req: func.HttpRequest) -> func.HttpResponse:
    """azure handler"""
    return func.WsgiMiddleware(app.wsgi_app).handle(req)
