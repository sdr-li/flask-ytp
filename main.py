from flask import Flask
from flask import render_template
from flask import url_for

from about import about
from convert import convert
app = Flask(__name__)
app.register_blueprint(about)
app.register_blueprint(convert)
app.secret_key = 'FG4983UJT089G7UEHIOUETO5TUI8P890K03WE0IK0FDJ897JY8DR57JH'



@app.route("/")
def main():
    return render_template('home.html')


if __name__ == "__main__":
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(host="127.0.0.1", port=8080, debug=False)

