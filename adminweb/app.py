from flask import Flask
from flask import render_template, json

from . import tree

db_path = 'data'
app = Flask(__name__, static_url_path='')

loader = tree.TreeLoader(db_path)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/help_formats')
def help_formats():
    return render_template('help_formats.html')


@app.route('/organism/all')
def organism_all():
    node = loader.organism()
    return json.dumps([node.as_dict()])


if __name__ == '__main__':
    app.run(debug=True)
