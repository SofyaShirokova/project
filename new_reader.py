from app import app
from flask import render_template

@app.route('/new_sportsmen', methods=['GET'])
def new_sportsmen():
    html = render_template(
        'new_sportsmen.html',
    )
    return html
