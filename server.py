import os
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def hello():
	return render_template('index.html')
    # return 'Hello World!'

@app.route('/customerDashboard')
def dashboard():
	return render_template('customerDashboard.html')

@app.route('/about')
def about():
	return render_template('contactUs.html')

@app.route('/services')
def services():
	return render_template('services.html')

@app.route('/contact')
def contact():
	return render_template('contactUs.html')


if __name__ == '__main__':
	app.run(host="0.0.0.0",port=5000,debug=True)