"""
Flask app for lab/guide
"""
import os
import re
import json
import requests
import base64
import urllib
from flask import Flask, render_template, jsonify, request, redirect, make_response, flash, url_for
from flask_caching import Cache
import markdown
from ce import get_ce_info, get_ce_state
from fetch import get_runner_session, cloudapp_fetch, cloudapp_req_headers, cloudapp_res_headers
from score import score_get_results, score_build_table

app = Flask(__name__)
app.config['ce_info'] = None
app.config['UDF'] = None
if os.getenv('UDF', None):
    app.config['ce_info'] = get_ce_info()
    app.config['UDF'] = True
    app.config['SESSION_COOKIE_SECURE'] = True
app.config['base_url'] = "mcn-lab.f5demos.com"
app.config['CACHE_TYPE'] = 'SimpleCache'
cache = Cache(app)
app.secret_key = "blahblahblah"
data_cookie = "mcnp-ac-data"
cookie_age = 86400

session = get_runner_session()
session.headers.update({"User-Agent": "MCN-Lab-Runner/1.0"})

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

def get_eph_ns() -> str:
    """check if ephemeral namespace is set"""
    cookie_b64 = request.cookies.get(data_cookie, None)
    if cookie_b64:
        return get_cookie_prop(cookie_b64, 'eph_ns')
    return None

def get_site() -> str:
    """check if ephemeral namespace is set"""
    if app.config['ce_info']:
        return app.config['ce_info'].get("site_name", None)
    return None

def update_cookie_prop(cookie_b64, prop, value):
    """update cookie"""
    try:
        json_bytes = base64.b64decode(cookie_b64)
        json_str = json_bytes.decode('utf-8')
        cookie_data = json.loads(json_str)
        cookie_data[prop] = value
        updated = json.dumps(cookie_data)
        base64_bytes = base64.b64encode(updated.encode('utf-8'))
        return base64_bytes.decode('utf-8')
    except json.JSONDecodeError:
        print("Error decoding cookie data")
        return "{}"
    
def get_cookie_prop(cookie_b64, prop):
    """get a cookie prop"""
    try:
        json_bytes = base64.b64decode(cookie_b64)
        json_str = json_bytes.decode('utf-8')
        c_dict = json.loads(json_str)
        return c_dict[prop]
    except json.JSONDecodeError:
        print("Error decoding cookie data")
        return None
    
def encode_data(data):
    """Encode dictionary to Base64-encoded JSON."""
    json_str = json.dumps(data)
    base64_bytes = base64.b64encode(json_str.encode('utf-8'))
    return base64_bytes.decode('utf-8')

def decode_data(encoded_data):
    """Decode Base64-encoded JSON to dictionary."""
    json_bytes = base64.b64decode(encoded_data)
    json_str = json_bytes.decode('utf-8')
    return json.loads(json_str)
    
@app.errorhandler(404)
@app.errorhandler(500)
def return_err(err):
    """common error handler"""
    img = {
        404: "/static/404.png",
        500: "/static/500.png"
    }
    return render_template("error.html", err_img=img[err.code])

@app.after_request
def cache_control(response):
    """cache control"""
    if request.path.startswith("/static/") and request.path.endswith(".png"):
        response.headers['Cache-Control'] = 'public, max-age=3600'
    return response

@app.before_request
def ensure_cookie():
    """ensure cookie"""
    """TBD: Do a little better here with a warning"""
    if request.path != '/' and data_cookie not in request.cookies:
        return redirect('/')
    
@app.route('/')
def index():
    """index page"""
    html = render_template('welcome.html',
        title="MCN Practical: Welcome"
    )
    response = make_response(html)
    if data_cookie not in request.cookies:
        response.set_cookie(data_cookie, '{}', max_age=cookie_age)
    return response

@app.route('/overview')
def overview():
    """overview page"""
    return render_template('overview.html',
        title="MCN Practical: Overview"
    )

@app.route('/setup', methods=['GET', 'POST'])
def setup_old():
    """setup page"""
    ns = get_eph_ns()
    if request.method == 'POST':
        action = request.form['action']
        if action == 'save':
            this_eph_ns = request.form['eph_ns'].strip()
            if not validate_eph_ns(this_eph_ns):
                flash("Invalid ephemeral namespace.", "danger")
                return redirect(url_for('setup'))
            response = make_response(redirect('/setup'))
            cookie_b64 = request.cookies.get('mcnp-ac-data', '{}')
            cookie_data = update_cookie_prop(cookie_b64, 'eph_ns', this_eph_ns)
            response.set_cookie(data_cookie, cookie_data)
            flash('Ephemeral namespace successfully set.', "success")
            return response
        if action == 'clear':
            response = make_response(redirect('/setup'))
            cookie_b64 = update_cookie_prop(cookie_b64, 'eph_ns', None)
            response.set_cookie(data_cookie, cookie_data)
            flash("Ephemeral namespace cleared.", "info")
            return response
    return render_template('setup.html',
        title="MCN Practical: Setup",
        ns=ns
    )

@app.route('/loadbalancing')
def lb():
    """lb page"""
    ns = get_eph_ns()
    site = get_site()
    return render_template('loadbalancing.html',
        title="MCN Practical: LB",
        site=site,
        ns=ns
    )

@app.route('/route')
def path():
    """routing page"""
    ns = get_eph_ns()
    return render_template('route.html',
        title="MCN Practical: HTTP Routing",
        ns=ns
    )

@app.route('/manipulation')
def header():
    """manipulation page"""
    ns = get_eph_ns()
    return render_template('manipulation.html',
        title="MCN Practical: Manipulation",
        ns=ns
    )

@app.route('/portability')
def port():
    """portability page"""
    ns = get_eph_ns()
    return render_template('portability.html',
        title="MCN Practical: Portability",
        ns=ns
    )

@app.route('/reference')
def ref():
    """reference page"""
    ns = get_eph_ns()
    html = render_md("markdown/reference.md")
    return render_template('coming-soon.html',
        title="MCN Practical: Reference",
        content=html, 
        ns=ns
    )

@app.route('/score')
def score():
    """scoreboard page"""
    all_cookies = request.cookies
    print(f"all cookies: {all_cookies}")
    score_cookie = request.cookies.get('mcnp_scoreboard', '%7B%7D')
    print(f"score cookie: {score_cookie}")
    try:
        decoded_cookie = urllib.parse.unquote(score_cookie)
        print(f"decoded cookie: {decoded_cookie}")
        enc_score = json.loads(decoded_cookie)
        print(f"enc score: {enc_score}")
        this_score = {urllib.parse.unquote(k): v for k, v in enc_score.items()}
        print(f"this score: {this_score}")
    except json.JSONDecodeError:
        this_score = {}
    try:
        p_score = score_get_results(this_score)
        over_table = score_build_table(p_score, 'overview', 'Overview')
        lb_table = score_build_table(p_score, 'lb', 'Load Balancing')
        route_table = score_build_table(p_score, 'route', 'Routing')
        manip_table = score_build_table(p_score, 'manip', 'Manipulation')
        port_table = score_build_table(p_score, 'port', 'Portability')
    except LabException as e:
        print(f"Couldn't build score table: {e}")
    return render_template('score.html',
            title="MCN Practical: Scoreboard",
            over_table=over_table,
            lb_table=lb_table,
            route_table=route_table,
            manip_table=manip_table,
            port_table=port_table,
        )

@app.route('/test')
def test():
    """test page"""
    ns = get_eph_ns()
    return render_template('test.html',
        title="MCN Practical: Test",
        ns=ns
    )

@app.route('/_ce_status')
def ce_state():
    """get ce state (internal route)"""
    all_cookies = request.cookies
    print(f"all cookies: {all_cookies}")
    data = get_ce_state(app.config['ce_info'])
    return data

@app.route('/_test1')
def ex_test():
    """Example test"""
    try:
        url = f"https://foo.{app.config['base_url']}/"
        data = cloudapp_fetch(session, url, 7, 'info', {"foo": True})
        return jsonify(status='success', data=data)
    except (LabException, ValueError) as e:
        return jsonify(status='fail', error=str(e))
    except requests.RequestException:
        return jsonify(status='fail', error="Connection/Request Error")

@app.route('/_test2')
def ex_test2():
    """Example test"""
    try:
        url = f"https://bar.{app.config['base_url']}/"
        data = cloudapp_fetch(session, url, 7, 'info', {"bar": True})
        return jsonify(status='success', data=data)
    except (LabException, ValueError) as e:
        return jsonify(status='fail', error=str(e))
    except requests.RequestException:
        return jsonify(status='fail', error="Connection/Request Error")

    
@app.route('/_lb1')
def lb_aws():
    """Azure LB test"""
    try:
        ns = get_eph_ns()
        if not ns:
            raise LabException("Ephemeral NS not set")
        url = f"https://{ns}.{app.config['base_url']}"
        data = cloudapp_fetch(session, url, 7, 'env', 'AWS')
        return jsonify(status='success', data=data)
    except (LabException, ValueError) as e:
        return jsonify(status='fail', error=str(e))
    except requests.RequestException:
        return jsonify(status='fail', error="Connection/Request Error")
   
@app.route('/_lb2')
def lb_azure():
    """Azure LB test"""
    try:
        ns = get_eph_ns()
        if not ns:
            raise LabException("Ephemeral NS not set")
        url = f"https://{ns}.{app.config['base_url']}"
        for _ in range(5):
            try:
                data = cloudapp_fetch(session, url, 7, 'env', 'Azure')
                return jsonify(status='success', data=data)
            except ValueError:
                pass
        raise ValueError("Failed to find Azure Origin Pool")
    except (LabException, ValueError) as e:
        return jsonify(status='fail', error=str(e))
    except requests.RequestException:
        return jsonify(status='fail', error="Connection/Request Error")
    
@app.route('/_route1')
def route1():
    """First Route Test"""
    try:
        ns = get_eph_ns()
        if not ns:
            raise LabException("Ephemeral NS not set")
        base_url = app.config['base_url']
        aws_url = f"https://{ns}.{base_url}/aws/raw"
        azure_url = f"https://{ns}.{base_url}/azure/raw"
        aws_data = cloudapp_fetch(session, aws_url, 7, 'env', 'AWS')
        azure_data = cloudapp_fetch(session, azure_url, 7, 'env', 'Azure')
        data = {
            "aws": aws_data,
            "azure": azure_data
        }
        return jsonify(status='success', data=data)
    except (LabException, ValueError) as e:
        return jsonify(status='fail', error=str(e))
    except requests.RequestException:
        return jsonify(status='fail', error="Connection/Request Error")
    
@app.route('/_route2')
def route2():
    """First Route Test"""
    try:
        ns = get_eph_ns()
        if not ns:
            raise LabException("Ephemeral NS not set")
        base_url = app.config['base_url']
        aws_url = f"https://{ns}.{base_url}/"
        azure_url = f"https://{ns}.{base_url}/"
        session.headers["X-MCN-lab"] = "aws"
        aws_data = cloudapp_fetch(session, aws_url, 7, 'env', 'AWS')
        session.headers["X-MCN-lab"] = "azure"
        azure_data = cloudapp_fetch(session, azure_url, 7, 'env', 'Azure')
        data = {
            "aws": aws_data,
            "azure": azure_data
        }
        return jsonify(status='success', data=data)
    except (LabException, ValueError) as e:
        return jsonify(status='fail', error=str(e))
    except requests.RequestException:
        return jsonify(status='fail', error="Connection/Request Error")

@app.route('/_manip1')
def manip1():
    """First Manip Test"""
    try:
        ns = get_eph_ns()
        if not ns:
            raise LabException("Ephemeral NS not set")
        base_url = app.config['base_url']
        url = f"https://{ns}.{base_url}/aws/raw"
        r_data = cloudapp_fetch(session, url, 5, 'info', {"method": "GET", "path": "/raw"})
        return jsonify(status='success', data=r_data)
    except (LabException, ValueError) as e:
        return jsonify(status='fail', error=str(e))
    except requests.RequestException:
        return jsonify(status='fail', error="Connection/Request Error")
    
@app.route('/_manip2')
def manip2():
    """Second Manip Test"""
    try:
        ns = get_eph_ns()
        site = get_site()
        if not ns:
            raise LabException("Ephemeral NS not set")
        base_url = app.config['base_url']
        url = f"https://{ns}.{base_url}/"
        t_headers = { "x-mcn-namespace": ns, "x-mcn-src-site": site}
        r_data = cloudapp_req_headers(session, url, 7, t_headers)
        return jsonify(status='success', data=r_data)
    except (LabException, ValueError) as e:
        return jsonify(status='fail', error=str(e))
    except requests.RequestException:
        return jsonify(status='fail', error="Connection/Request Error")
    
@app.route('/_manip3')
def manip3():
    """Third Manip Test"""
    try:
        ns = get_eph_ns()
        if not ns:
            raise LabException("Ephemeral NS not set")
        base_url = app.config['base_url']
        aws_url = f"https://{ns}.{base_url}/aws/"
        azure_url = f"https://{ns}.{base_url}/azure/"
        aws_headers = { "x-mcn-dest-site": "student-awsnet" }
        azure_headers = { "x-mcn-dest-site": "student-azurenet" }
        aws_data = cloudapp_res_headers(session, aws_url, 7, aws_headers)
        azure_data = cloudapp_res_headers(session, azure_url, 7, azure_headers)
        data = {
            "aws": aws_data,
            "azure": azure_data
        }
        return jsonify(status='success', data=data)
    except (LabException, ValueError) as e:
        return jsonify(status='fail', error=str(e))
    except requests.RequestException:
        return jsonify(status='fail', error="Connection/Request Error")

@app.route('/_port1')
def port1():
    """Friend test"""
    try:
        ns = get_eph_ns()
        if not ns:
            raise LabException("Ephemeral NS not set")
        url = f"https://{ns}.{app.config['base_url']}/"
        data = cloudapp_fetch(session, url, 7, 'info', {"method": "GET", "path": "/"})
        return jsonify(status='success', data=data)
    except (LabException, ValueError) as e:
        return jsonify(status='fail', error=str(e))
    except requests.RequestException:
        return jsonify(status='fail', error="Connection/Request Error")
        
@app.route('/_port2', methods=['POST'])
def port2():
    """Friend test"""
    try:
        data = request.get_json()
        eph_ns = data['userInput']
        url = f"https://{eph_ns}.{app.config['base_url']}/"
        data = cloudapp_fetch(session, url, 7, 'info', {"method": "GET", "path": "/"})
        return jsonify(status='success', data=data)
    except (LabException, ValueError) as e:
        return jsonify(status='fail', error=str(e))
    except requests.RequestException:
        return jsonify(status='fail', error="Connection/Request Error")
        

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=False)