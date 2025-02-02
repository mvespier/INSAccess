# server.py
from flask import Flask, render_template, url_for

app = Flask(__name__, static_folder='static', template_folder='templates')

@app.route("/")
def home():
    return render_template('calendar.html', sheet_css=url_for('static', filename='style.css'), script_js=url_for('static', filename='script.js'), data_json=url_for('static', filename='data.json'))

if __name__ == "__main__":
    app.run(port=8000, debug=True)
