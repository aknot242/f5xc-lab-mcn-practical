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
from fetch import cloudapp_fetch, cloudapp_req_headers, cloudapp_res_headers

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
    html = render_md("markdown/welcome.md")
    return render_template('standard.html',
        title="MCN Practical: Overview",
        content=html
    )

@app.route('/overview')
def arch():
    """arch page"""
    html = render_md("markdown/overview.md")
    return render_template('standard.html',
        title="MCN Practical: Architecture",
        content=html
    )

@app.route('/setup', methods=['GET', 'POST'])
def setup():
    """setup page"""
    ns = eph_ns()
    if request.method == 'POST':
        action = request.form['action']
        if action == 'save':
            this_eph_ns = request.form['eph_ns'].strip()
            if not validate_eph_ns(this_eph_ns):
                flash("Invalid ephemeral NS.", "danger")
                return redirect(url_for('setup'))
            response = make_response(redirect('/setup'))
            response.set_cookie('eph_ns', this_eph_ns, max_age=60*60*24)
            flash('Ephemeral NS successfully set.', "success")
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
        ns=ns
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
        ns=ns
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

    )

@app.route('/manipulation')
def header():
    """manipulation page"""
    ns = eph_ns()
    html = render_md("markdown/manipulation.md")
    return render_template('exercise_standard.html',
        title="MCN Practical: Manipulation",
        content=html, 
        ns=ns
    )

@app.route('/portability')
def port():
    """portability page"""
    ns = eph_ns()
    html = render_md("markdown/portability.md")
    return render_template('exercise_standard.html',
        title="MCN Practical: Portability",
        content=html, 
        ns=ns
    )

@app.route('/vnet')
def vnet():
    """vnet page"""
    ns = eph_ns()
    html = render_md("markdown/reference.md")
    return render_template('coming-soon.html',
        title="MCN Practical: Reference",
        content=html, 
        ns=ns
    )

@app.route('/netpolicy')
def netp():
    """netpolicy page"""
    ns = eph_ns()
    html = render_md("markdown/reference.md")
    return render_template('coming-soon.html',
        title="MCN Practical: Reference",
        content=html, 
        ns=ns
    )

@app.route('/ref')
def ref():
    """reference page"""
    ns = eph_ns()
    html = render_md("markdown/reference.md")
    return render_template('coming-soon.html',
        title="MCN Practical: Reference",
        content=html, 
        ns=ns
    )

@app.route('/score')
def score():
    """scoreboard page"""
    ns = eph_ns()
    html = render_md("markdown/score.md")
    return render_template('coming-soon.html',
        title="MCN Practical: Scoreboard",
        content=html, 
        ns=ns
    )

@app.route('/_test1')
def ex_test():
    """Example test"""
    try:
        s = requests.Session()
        s.headers.update({"User-Agent": "MCN-Lab-Runner/1.0"})
        url = f"https://foo.{app.config['base_url']}/"
        data = cloudapp_fetch(s, url, 7, 'info', {"foo": True})
        return jsonify(status='success', data=data)
    except (LabException, requests.RequestException, ValueError) as e:
        return jsonify(status='fail', error=str(e))

@app.route('/_test2')
def ex_test2():
    """Example test"""
    try:
        s = requests.Session()
        s.headers.update({"User-Agent": "MCN-Lab-Runner/1.0"})
        url = f"https://bar.{app.config['base_url']}/"
        data = cloudapp_fetch(s, url, 7, 'info', {"bar": True})
        return jsonify(status='success', data=data)
    except (LabException, requests.RequestException, ValueError) as e:
        return jsonify(status='fail', error=str(e))

    
@app.route('/_lb1')
def lb_aws():
    """Azure LB test"""
    try:
        s = requests.Session()
        s.headers.update({"User-Agent": "MCN-Lab-Runner/1.0"})
        ns = eph_ns()
        if not ns:
            raise LabException("Ephemeral NS not set")
        url = f"https://{ns}.{app.config['base_url']}"
        data = cloudapp_fetch(s, url, 7, 'env', 'AWS')
        return jsonify(status='success', data=data)
    except (LabException, requests.RequestException, ValueError) as e:
        return jsonify(status='fail', error=str(e))
    
@app.route('/_lb2')
def lb_azure():
    """Azure LB test"""
    try:
        s = requests.Session()
        s.headers.update({"User-Agent": "MCN-Lab-Runner/1.0"})
        ns = eph_ns()
        if not ns:
            raise LabException("Ephemeral NS not set")
        url = f"https://{ns}.{app.config['base_url']}"
        data = cloudapp_fetch(s, url, 7, 'env', 'Azure')
        return jsonify(status='success', data=data)
    except (LabException, requests.RequestException, ValueError) as e:
        return jsonify(status='fail', error=str(e))
    
@app.route('/_route1')
def route1():
    """First Route Test"""
    try:
        s = requests.Session()
        s.headers.update({"User-Agent": "MCN-Lab-Runner/1.0"})
        ns = eph_ns()
        if not ns:
            raise LabException("Ephemeral NS not set")
        base_url = app.config['base_url']
        aws_url = f"https://{ns}.{base_url}/aws/raw"
        azure_url = f"https://{ns}.{base_url}/azure/raw"
        aws_data = cloudapp_fetch(s, aws_url, 7, 'env', 'AWS')
        azure_data = cloudapp_fetch(s, azure_url, 7, 'env', 'Azure')
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
        s = requests.Session()
        s.headers.update({"User-Agent": "MCN-Lab-Runner/1.0"})
        ns = eph_ns()
        if not ns:
            raise LabException("Ephemeral NS not set")
        base_url = app.config['base_url']
        aws_url = f"https://{ns}.{base_url}/"
        azure_url = f"https://{ns}.{base_url}/"
        s.headers["X-MCN-lab"] = "aws"
        aws_data = cloudapp_fetch(s, aws_url, 7, 'env', 'AWS')
        s.headers["X-MCN-lab"] = "azure"
        azure_data = cloudapp_fetch(s, azure_url, 7, 'env', 'Azure')
        data = {
            "aws": aws_data,
            "azure": azure_data
        }
        return jsonify(status='success', data=data)
    except (LabException, requests.RequestException, ValueError) as e:
        return jsonify(status='fail', error=str(e))

@app.route('/_manip1')
def manip1():
    """First Manip Test"""
    try:
        s = requests.Session()
        s.headers.update({"User-Agent": "MCN-Lab-Runner/1.0"})
        ns = eph_ns()
        if not ns:
            raise LabException("Ephemeral NS not set")
        base_url = app.config['base_url']
        url = f"https://{ns}.{base_url}/aws/raw"
        r_data = cloudapp_fetch(s, url, 5, 'info', {"method": "GET", "path": "/raw"})
        return jsonify(status='success', data=r_data)
    except (LabException, requests.RequestException, ValueError) as e:
        return jsonify(status='fail', error=str(e))
    
@app.route('/_manip2')
def manip2():
    """Second Manip Test"""
    try:
        s = requests.Session()
        s.headers.update({"User-Agent": "MCN-Lab-Runner/1.0"})
        ns = eph_ns()
        if not ns:
            raise LabException("Ephemeral NS not set")
        base_url = app.config['base_url']
        url = f"https://{ns}.{base_url}/"
        t_headers = { "x-mcn-namespace": ns, "x-mcn-src-site": app.config["ce_info"]["site_name"]}
        r_data = cloudapp_req_headers(s, url, 7, t_headers)
        return jsonify(status='success', data=r_data)
    except (LabException, requests.RequestException, ValueError) as e:
        return jsonify(status='fail', error=str(e))
    
@app.route('/_manip3')
def manip3():
    """Third Manip Test"""
    try:
        s = requests.Session()
        s.headers.update({"User-Agent": "MCN-Lab-Runner/1.0"})
        ns = eph_ns()
        if not ns:
            raise LabException("Ephemeral NS not set")
        base_url = app.config['base_url']
        aws_url = f"https://{ns}.{base_url}/aws"
        azure_url = f"https://{ns}.{base_url}/azure"
        aws_headers = { "x-mcn-dest-site": "student-awsnet" }
        azure_headers = { "x-mcn-dest-site": "student-azurenet" }
        aws_data = cloudapp_res_headers(s, aws_url, 7, aws_headers)
        azure_data = cloudapp_res_headers(s, azure_url, 7, azure_headers)
        data = {
            "aws": aws_data,
            "azure": azure_data
        }
        return jsonify(status='success', data=data)
    except (LabException, requests.RequestException, ValueError) as e:
        return jsonify(status='fail', error=str(e))
        

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=False)