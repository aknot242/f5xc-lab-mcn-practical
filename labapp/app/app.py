"""
Flask app for lab/guide
"""
import os
import re
from flask import Flask, render_template, jsonify, request, redirect, make_response, flash, url_for
from flask_caching import Cache
import requests
import markdown
from ce import get_ce_info, get_ce_state

app = Flask(__name__)
app.config['udf'] =  os.getenv('UDF', False)
info = None
if app.config['udf']:
    info = get_ce_info()
app.config['ce_info'] = info
app.config['base_url'] = "mcn-lab.f5demos.com"
app.config['CACHE_TYPE'] = 'SimpleCache'
cache = Cache(app)
app.secret_key = "blahblahblah"

def render_md(file: str) -> str:
    """render markdown w/ common extentions"""
    with open(file, "r") as file:
        content = file.read()
    html = markdown.markdown(
        content,
        extensions=['markdown.extensions.attr_list','markdown.extensions.codehilite','markdown.extensions.fenced_code']
        )
    return html

def validate_eph_ns(input_name):
    """validate ephemeral namespace name"""
    pattern = r'^[a-zA-Z]+-[a-zA-Z]+$'
    return bool(re.match(pattern, input_name))

def eph_ns() -> str:
    """check if ephemeral namespace is set"""
    eph_ns = request.cookies.get('eph_ns', None)
    return eph_ns

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
    """index page"""
    html = render_md("markdown/overview.md")
    return render_template('overview.html', content=html)

@app.route('/setup', methods=['GET', 'POST'])
def setup():
    """setup page"""
    if request.method == 'POST':
        action = request.form['action']
        if action == 'save':
            eph_ns = request.form['eph_ns'].strip()
            print(eph_ns)
            if not validate_eph_ns(eph_ns):
                flash("Invalid ephemeral NS.", "danger")
                return redirect(url_for('setup'))
            response = make_response(redirect('/setup'))
            response.set_cookie('eph_ns', eph_ns, max_age=60*60*24)
            flash("Ephemeral NS successfully set.", "success")
            return response
        elif action == 'clear':
            response = make_response(redirect('/setup'))
            response.set_cookie('eph_ns', '', expires=0)
            flash("Ephemeral NS cleared.", "info")
            return response
    html = render_md("markdown/setup.md")
    return render_template('setup.html', content=html)

@app.route('/arch')
def arch():
    """arch page"""
    html = render_md("markdown/arch.md")
    return render_template('standard.html', content=html, title="MCN Practical: Architecture")

@app.route('/_ce_state')
@cache.cached(timeout=30)
def ce_state():
    """get ce state (internal route)"""
    data = get_ce_state(app.config['ce_info'])
    return data

@app.route('/lb')
def lb():
    """lb page"""
    ns = eph_ns()
    html = render_md("markdown/lb.md")
    return render_template('exercise_standard.html', title="MCN Practical: LB", content=html, ns=ns)

@app.route('/path')
def path():
    """path page"""
    ns = eph_ns()
    html = render_md("markdown/path.md")
    return render_template('exercise_standard.html', title="MCN Practical: Path Routing", content=html, ns=ns)

@app.route('/header')
def header():
    """header page"""
    ns = eph_ns()
    html = render_md("markdown/header.md")
    return render_template('exercise_standard.html', title="MCN Practical: Headers", content=html, ns=ns)

@app.route('/_lb_aws')
def lb_aws():
    """AWS LB test"""
    try:
        ns = eph_ns()
        if not ns:
            raise Exception("Ephemeral NS not set.")
        url = f"https://{ns}.{app.config['base_url']}/raw"
        print(url)
        response = requests.get(url, timeout=5)
        print(response.text)
        print(response.json())
        response.raise_for_status()
        if response.json()['request_env'] != "AWS":
            raise Exception("Invalid request env.")
        return jsonify(status='success', data=response.json())
    except Exception as e:
        return jsonify(status='fail', error=str(e))
    
@app.route('/_lb_azure')
def lb_azure():
    """Azure LB test"""
    try:
        response = requests.get('https://ifconfig1.io/all.json')
        response.raise_for_status() 
        return jsonify(status='success', data=response.json())
    except requests.RequestException as e:
        return jsonify(status='fail', error=str(e))

if __name__ == '__main__':
    app.run(debug=False)