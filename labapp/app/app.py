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
app.config['ce_info'] = None
app.config['UDF'] = None
if os.getenv('UDF', None):
    app.config['ce_info'] = get_ce_info()
    app.config['UDF'] = True
app.config['base_url'] = "mcn-lab.f5demos.com"
app.config['CACHE_TYPE'] = 'SimpleCache'
cache = Cache(app)
app.secret_key = "blahblahblah"

class LabException(Exception):
    """lab exception"""

def render_md(file: str) -> str:
    """render markdown w/ common extentions"""
    with open(file, "r", encoding="utf-8") as md:
        content = md.read()
    html = markdown.markdown(
        content,
        extensions=['markdown.extensions.attr_list','markdown.extensions.fenced_code']
        )
    return html

def validate_eph_ns(input_name):
    """validate ephemeral namespace name"""
    pattern = r'^[a-zA-Z]+-[a-zA-Z]+$'
    return bool(re.match(pattern, input_name))

def eph_ns() -> str:
    """check if ephemeral namespace is set"""
    this_eph_ns = request.cookies.get('eph_ns', None)
    return this_eph_ns

def cloudapp_fetch(url, timeout, prop, value, headers = {}):
    """
    Fetch data from URL
    Validate prop and value in the JSON response
    """
    response = requests.get(url, timeout=timeout, headers=headers)
    response.raise_for_status()
    data = response.json()
    if data.get(prop) != value:
        raise ValueError(f"Invalid {prop}: expected {value}, got {data.get(prop)}")
    clean_headers = headers_cleaner(data['request_headers'])
    data['request_headers'] = clean_headers
    return data

def headers_cleaner(headers):
    """
    Remove headers that contain specific substrings.
    """
    unwanted_substrings = ['x-envoy', 'cloudfront', 'x-k8se'] 
    filtered_headers = {
        key: value for key, value in headers.items()
        if not any(substring in key.lower() for substring in unwanted_substrings)
    }
    return filtered_headers

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
    return render_template('standard.html',
        title="MCN Practical: Overview",
        content=html, 
        udf=app.config['UDF'] 
    )

@app.route('/setup', methods=['GET', 'POST'])
def setup():
    """setup page"""
    if request.method == 'POST':
        action = request.form['action']
        if action == 'save':
            this_eph_ns = request.form['eph_ns'].strip()
            if not validate_eph_ns(this_eph_ns):
                flash("Invalid ephemeral NS.", "danger")
                return redirect(url_for('setup'))
            response = make_response(redirect('/setup'))
            response.set_cookie('eph_ns', this_eph_ns, max_age=60*60*24)
            flash("Ephemeral NS successfully set.", "success")
            return response
        if action == 'clear':
            response = make_response(redirect('/setup'))
            response.set_cookie('eph_ns', '', expires=0)
            flash("Ephemeral NS cleared.", "info")
            return response
    html = render_md("markdown/setup.md")
    return render_template('setup.html',
        title="MCN Practical: Setup",
        content=html,
        udf=app.config['UDF']
    )

@app.route('/arch')
def arch():
    """arch page"""
    html = render_md("markdown/arch.md")
    return render_template('standard.html',
        title="MCN Practical: Architecture",
        content=html,
        udf=app.config['UDF']
    )

@app.route('/_ce_status')
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
    return render_template('exercise_standard.html',
        title="MCN Practical: LB",
        content=html,
        ns=ns,
        udf=app.config['UDF']
    )

@app.route('/route')
def path():
    """routing page"""
    ns = eph_ns()
    html = render_md("markdown/route.md")
    return render_template('exercise_standard.html',
        title="MCN Practical: HTTP Routing",
        content=html,
        ns=ns,
        udf=app.config['UDF']
    )

@app.route('/header')
def header():
    """header page"""
    ns = eph_ns()
    html = render_md("markdown/header.md")
    return render_template('exercise_standard.html',
        title="MCN Practical: Headers",
        content=html, 
        ns=ns,
        udf=app.config['UDF']
    )

@app.route('/_lb1')
def lb_aws():
    """Azure LB test"""
    try:
        ns = eph_ns()
        if not ns:
            raise LabException("Ephemeral NS not set")
        url = f"https://{ns}.{app.config['base_url']}/raw"
        data = cloudapp_fetch(url, 5, 'request_env', 'AWS')
        return jsonify(status='success', data=data)
    except (LabException, requests.RequestException, ValueError) as e:
        return jsonify(status='fail', error=str(e))
    
@app.route('/_lb2')
def lb_azure():
    """Azure LB test"""
    try:
        ns = eph_ns()
        if not ns:
            raise LabException("Ephemeral NS not set")
        url = f"https://{ns}.{app.config['base_url']}/raw"
        data = cloudapp_fetch(url, 5, 'request_env', 'Azure')
        return jsonify(status='success', data=data)
    except (LabException, requests.RequestException, ValueError) as e:
        return jsonify(status='fail', error=str(e))
    
@app.route('/_route1')
def route1():
    """First Route Test"""
    try:
        ns = eph_ns()
        if not ns:
            raise LabException("Ephemeral NS not set")
        base_url = app.config['base_url']
        aws_url = f"https://{ns}.{base_url}/aws/raw"
        azure_url = f"https://{ns}.{base_url}/azure/raw"
        aws_data = cloudapp_fetch(aws_url, 5, 'request_env', 'AWS')
        azure_data = cloudapp_fetch(azure_url, 5, 'request_env', 'Azure')
        data = {
            "aws": aws_data,
            "azure": azure_data
        }
        return jsonify(status='success', data=data)
    except (LabException, requests.RequestException, ValueError) as e:
        return jsonify(status='fail', error=str(e))
    
@app.route('/_route2')
def route2():
    """First Route Test"""
    try:
        ns = eph_ns()
        if not ns:
            raise LabException("Ephemeral NS not set")
        base_url = app.config['base_url']
        aws_url = f"https://{ns}.{base_url}/aws/raw"
        azure_url = f"https://{ns}.{base_url}/azure/raw"
        aws_data = cloudapp_fetch(aws_url, 5, 'request_env', 'AWS', headers={"X-MCN-lab": "aws"})
        azure_data = cloudapp_fetch(azure_url, 5, 'request_env', 'Azure', headers={"X-MCN-lab": "azure"})
        data = {
            "aws": aws_data,
            "azure": azure_data
        }
        return jsonify(status='success', data=data)
    except (LabException, requests.RequestException, ValueError) as e:
        return jsonify(status='fail', error=str(e))
        

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=False)