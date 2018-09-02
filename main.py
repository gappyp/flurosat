from __future__ import print_function

from flask import Flask, request

from prep import do_he
from anoms import proc_img
from gjs import get_gj
import sys

if 'lin' in sys.platform:
    temp_fn = '/tmp/uploaded_fn'
elif 'win' in sys.platform:
    temp_fn = r'uploaded_fn'

app = Flask(__name__)

@app.route('/')
def index():
    return """
<h1>geojson</h1>
<form method="POST" action="/geojson" enctype="multipart/form-data">
    <input type="file" name="file">
    <input type="submit">
</form>

<h1>shapefile</h1>
<form method="POST" action="/shapefile" enctype="multipart/form-data">
    <input type="file" name="file">
    <input type="submit">
</form>
"""

@app.route('/geojson', methods=['POST'])
def upload():
    uploaded_file = request.files.get('file')

    if not uploaded_file:
        return 'No file uploaded.', 400

    with open(temp_fn, 'wb') as fp:
        fp.write(uploaded_file.read())

    he = do_he(temp_fn)
    proced = proc_img(he)

    return get_gj(proced, temp_fn)

@app.route('/shapefile', methods=['POST'])
def shapefile():
    return 'coming soon'

@app.errorhandler(500)
def server_error(e):
    logging.exception('An error occurred during a request.')
    return """
    An internal error occurred: <pre>{}</pre>
    See logs for full stacktrace.
    """.format(e), 500

if __name__ == '__main__':
    # This is used when running locally. Gunicorn is used to run the
    # application on Google App Engine. See entrypoint in app.yaml.
    app.run(host='127.0.0.1', port=50000, debug=True)