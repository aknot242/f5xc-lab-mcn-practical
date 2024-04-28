import logging
import azure.functions as func
import sys
sys.path.append('..')
from app import create_app

flask = create_app()

app = func.WsgiFunctionApp(app=flask.wsgi_app, http_auth_level=func.AuthLevel.ANONYMOUS)


@app.route(route="cloudapp_dev", auth_level=func.AuthLevel.ANONYMOUS)
def cloudapp_dev(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    if name:
        return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully.")
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )