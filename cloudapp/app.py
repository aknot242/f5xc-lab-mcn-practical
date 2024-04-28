"""
MCN Practical Universal Web App
"""
import os
import json
from dotenv import load_dotenv
from flask import Flask, jsonify, request, render_template

app = Flask(__name__)
load_dotenv()

@app.template_filter('to_pretty_json')
def to_pretty_json(value):
    return json.dumps(value, sort_keys=True, indent=4)

@app.route('/')
def index():
    """
    Index page
    """
    return jsonify(info='MCN Practical web app')

@app.route('/echo_raw', methods=['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
def echo():
    """
    Echo the request headers and data
    """
    env = os.getenv('SITE', 'unknown')
    headers = dict(request.headers)
    data = None
    if request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
        try:
            data = request.get_json() or request.form.to_dict()
        except Exception as e:
            print(e)
    response = {
        'request_headers': headers,
        'request_env': env
    }
    if data:
        response['request_data'] = data
    return jsonify(response)

@app.route('/echo', methods=['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
def echo_html():
    """ Same as /echo, just prettier"""
    env = os.getenv('SITE', 'local')
    headers = dict(request.headers)
    data = None
    if request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
        try:
            data = request.get_json()
        except Exception:
            pass
        try:
            data = request.form.to_dict()
        except Exception:
            pass
    return render_template('pretty_echo.html', request_env=env, request_headers=headers, request_data=data)

if __name__ == '__main__':
    app.run(debug=True)
