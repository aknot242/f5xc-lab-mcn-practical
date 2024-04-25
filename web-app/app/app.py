"""
Flask app for lab/guide
"""
from flask import Flask, render_template, jsonify, request, redirect, make_response
import requests
import markdown
import re
import validators

app = Flask(__name__)

def is_valid_domain(domain):
    """Simple regex to validate a domain name."""
    pattern = r'^[a-zA-Z\d-]{,63}(\.[a-zA-Z\d-]{,63})*$'
    return re.match(pattern, domain) is not None

@app.route('/')
def index():
    with open("markdown/overview.md", "r") as file:
        content = file.read()
    html = markdown.markdown(content)
    return render_template('overview.html', content=html)

@app.route('/setup', methods=['GET', 'POST'])
def setup():
    if request.method == 'POST':
        action = request.form['action']
        if action == 'save':
            base_url = request.form['base_url'].strip()
            # Validate domain using the validators library
            if not validators.domain(base_url):
                # Handle invalid domain name
                return render_template('setup.html', error="Invalid domain format.")
            response = make_response(redirect('/setup'))
            response.set_cookie('base_url', base_url, max_age=60*60*24)
            return response
        elif action == 'clear':
            response = make_response(redirect('/setup'))
            response.set_cookie('base_url', '', expires=0)  # Clear the cookie
            return response
    return render_template('setup.html')

@app.route('/test')
def test():
    base_url = request.cookies.get('base_url')
    url = f"https://echo.{base_url}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return jsonify(status='success', data=response.json())
    except requests.RequestException as e:
        return jsonify(status='fail', error=str(e))

@app.route('/lb')
def lb():
    with open("markdown/lb.md", "r") as file:
        content = file.read()
    #html = markdown.markdown(content)
    html = markdown.markdown(
        content,
        extensions=['markdown.extensions.codehilite','markdown.extensions.fenced_code']
        )
    return render_template('lb.html', content=html)

@app.route('/page3')
def page3():
    return render_template('page3.html')

@app.route('/page4')
def page4():
    return render_template('page4.html')

@app.route('/appCon-aws')
def make_request_ac1_aws():
    try:
        response = requests.get('https://ifconfig.io/all.json')
        response.raise_for_status() 
        return jsonify(status='success', data=response.json())
    except requests.RequestException as e:
        return jsonify(status='fail', error=str(e))
    
@app.route('/appCon-azure')
def make_request_ac1_azure():
    try:
        response = requests.get('https://ifconfig1.io/all.json')
        response.raise_for_status() 
        return jsonify(status='success', data=response.json())
    except requests.RequestException as e:
        return jsonify(status='fail', error=str(e))

if __name__ == '__main__':
    app.run(debug=True)