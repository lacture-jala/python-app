from flask import Flask
app = Flask(__name__)

@app.route('/')
def home():
    return "Welcome to Home Route"

@app.route('/<name>')
def name(name):
    return f"Welcome to Home Route <b>{name}</b>"



app.run(host="0.0.0.0",port=5000,debug=True)