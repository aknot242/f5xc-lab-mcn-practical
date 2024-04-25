from flask import Flask, render_template, jsonify
import requests
import markdown

app = Flask(__name__)

@app.route('/')
def index():
    with open("markdown/overview.md", "r") as file:
        content = file.read()
    html = markdown.markdown(content)
    return render_template('overview.html', content=html)

@app.route('/lb')
def lb():
    with open("markdown/lb.md", "r") as file:
        content = file.read()
    #html = markdown.markdown(content)
    html = markdown.markdown(
        content,
        extensions=['markdown.extensions.attr_list','markdown.extensions.codehilite','markdown.extensions.fenced_code']
        )
    return render_template('lb.html', content=html)

@app.route('/page3')
def page3():
    return render_template('page3.html')

@app.route('/page4')
def page4():
    return render_template('page4.html')

@app.route('/appConnect1')
def make_request():
    try:
        response = requests.get('https://ifconfig.io/all.json')
        response.raise_for_status() 
        return jsonify(status='success', data=response.json())
    except requests.RequestException as e:
        return jsonify(status='fail', error=str(e))
    
@app.route('/appCon-aws')
def make_request():
    try:
        response = requests.get('https://ifconfig.io/all.json')
        response.raise_for_status() 
        return jsonify(status='success', data=response.json())
    except requests.RequestException as e:
        return jsonify(status='fail', error=str(e))
    
@app.route('/appCon-azure')
def make_request():
    try:
        response = requests.get('https://ifconfig.io/all.json')
        response.raise_for_status() 
        return jsonify(status='success', data=response.json())
    except requests.RequestException as e:
        return jsonify(status='fail', error=str(e))

if __name__ == '__main__':
    app.run(debug=True)