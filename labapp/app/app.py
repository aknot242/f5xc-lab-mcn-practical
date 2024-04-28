"""
Flask app for lab/guide
"""
from flask import Flask, render_template, jsonify, request, redirect, make_response, flash, url_for
from flask_caching import Cache
import requests
import markdown
import validators
import os
from dotenv import load_dotenv
from ce import get_ce_info, get_ce_state

app = Flask(__name__)
app.config['site'] =  os.getenv('SITE', None)
info = None
if app.config['site']:
    info = get_ce_info()
app.config['ce_info'] = info
app.config['ce_info'] = None
app.config['base_url'] = "lab-mcn.f5demos.com"
app.config['CACHE_TYPE'] = 'SimpleCache'
cache = Cache(app)
app.secret_key = "blahblahblah"

@app.errorhandler(404)
@app.errorhandler(500)
def return_err(err):
    """common error handler"""
    img = {
        404: "/static/404.png",
        500: "/static/500.png"
    }
    return render_template("error.html", err_img=img[err.code])

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
            if not validators.domain(base_url):
                flash("Invalid domain format.", "info")
                return redirect(url_for('setup'))
            if not base_url.endswith(app.config['base_url']):
                flash(f"Domain must end with {app.config['base_url']}.", "info")
                return redirect(url_for('setup'))
            response = make_response(redirect('/setup'))
            response.set_cookie('base_url', base_url, max_age=60*60*24)
            flash("Domain successfully set.", "success")
            return response
        elif action == 'clear':
            response = make_response(redirect('/setup'))
            response.set_cookie('base_url', '', expires=0)
            flash("Domain setting cleared.", "info")
            return response
    return render_template('setup.html', base_url=app.config['base_url'])

@app.route('/ce_state')
@cache.cached(timeout=30)
def ce_state():
    data = get_ce_state(app.config['ce_info'])
    return data

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
    html = markdown.markdown(
        content,
        extensions=['markdown.extensions.codehilite','markdown.extensions.fenced_code']
        )
    return render_template('lb.html', content=html)

@app.route('/path')
def path():
    with open("markdown/path.md", "r") as file:
        content = file.read()
    html = markdown.markdown(
        content,
        extensions=['markdown.extensions.codehilite','markdown.extensions.fenced_code']
        )
    return render_template('path.html', content=html)

@app.route('/header')
def header():
    with open("markdown/header.md", "r") as file:
        content = file.read()
    html = markdown.markdown(
        content,
        extensions=['markdown.extensions.codehilite','markdown.extensions.fenced_code']
        )
    return render_template('header.html', context=html)

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
    app.run(debug=False)