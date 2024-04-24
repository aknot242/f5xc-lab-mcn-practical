from flask import Flask, render_template, jsonify
import requests
import json

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/appConnect1')
def make_request():
    try:
        response = requests.get('https://ifconfig.io/all.json')
        response.raise_for_status()  # Raises an HTTPError for bad responses
        return jsonify(status='success', data=response.json())
    except requests.RequestException as e:
        return jsonify(status='fail', error=str(e))

@app.route('/page2')
def page2():
    return render_template('page2.html')

@app.route('/page3')
def page3():
    return render_template('page3.html')

@app.route('/page4')
def page4():
    return render_template('page4.html')

if __name__ == '__main__':
    app.run(debug=True)