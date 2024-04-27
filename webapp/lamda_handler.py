from aws_lambda_wsgi import wsgi_handler
from app import app

def handler(event, context):
    """Lambda handler"""
    return wsgi_handler(event, context, app)
