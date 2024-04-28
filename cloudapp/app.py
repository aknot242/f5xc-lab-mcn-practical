"""
MCN Practical Universal Web App
"""
import os
import json
from flask import Flask, jsonify, request, render_template

def create_app():
    app = Flask(__name__)
    app.config['site'] =  os.getenv('SITE', "local")

    @app.template_filter('to_pretty_json')
    def to_pretty_json(value):
        return json.dumps(value, sort_keys=True, indent=4)

    @app.route('/raw', methods=['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
    def echo():
        """
        Echo the request headers and data
        """
        headers = dict(request.headers)
        data = None
        if request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            try:
                data = request.get_json() or request.form.to_dict()
            except Exception as e:
                print(e)
        response = {
            'request_headers': headers,
            'request_env': app.config['site']
        }
        if data:
            response['request_data'] = data
        return jsonify(response)

    @app.route('/', methods=['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
    @app.route('/echo', methods=['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
    def echo_html():
        """ Same as /raw, just prettier"""
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
        return render_template('pretty_echo.html', request_env=app.config['site'], request_headers=headers, request_data=data)
    
    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=False)
