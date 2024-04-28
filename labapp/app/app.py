"""
Flask app for lab/guide
"""
from flask import Flask, render_template, jsonify, request, redirect, make_response, flash, url_for
from flask_caching import Cache
import requests
import markdown
import validators
from ce import get_ce_info, get_ce_state

app = Flask(__name__)
app.config['ce_info'] = get_ce_info()
app.config['CACHE_TYPE'] = 'SimpleCache'
cache = Cache(app)
#app.secret_key = 'super_secret'

@app.errorhandler(400)
def return_400():
    return render_template("error.html"), 400

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
                flash("Invalid domain format.", "error")
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
    return render_template('setup.html')

@app.route('/ce_state')
@cache.cached(timeout=30)
def get_ce_state():
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