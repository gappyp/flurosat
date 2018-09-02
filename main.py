import logging
import os

from flask import Flask, request
#from google.cloud import storage

# [start config]
app = Flask(__name__)


# Configure this environment variable via app.yaml
#CLOUD_STORAGE_BUCKET = os.environ['CLOUD_STORAGE_BUCKET']
# [end config]


@app.route('/')
def index():
    return """
<form method="POST" action="/upload" enctype="multipart/form-data">
    <input type="file" name="file">
    <input type="submit">
</form>
"""

