from pcaw_site import app
from flask import redirect, render_template, url_for

@app.route('/')
@app.route('/index')
def index():
    return render_template('home/index.html')