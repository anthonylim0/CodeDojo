from flask import render_template
from app import application
from app.static.library import output_stun, output_seed

@application.route('/')
@application.route('/index')
def index():
    return render_template('index.html', a=output_stun()[0][0], b=output_stun()[0][1], c=output_seed(), d=output_stun())