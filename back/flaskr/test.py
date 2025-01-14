from markupsafe import escape
from flask import Flask

app = Flask(__name__)

@app.route("/<name>")
def hello(name):
    return f"Hello, {escape(name)}!"


@app.route("/<name>/<toto>")
def hello2(name,toto):
    return f"Hello {escape(name)}, YIPEEE {escape(toto)}!"

