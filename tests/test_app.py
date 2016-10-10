import pytest
from flask import url_for
from dicom_flask_uploader.app import create_app
from dicom_flask_uploader.app import db
from StringIO import StringIO
import os
import py

FILE_PATH = os.path.realpath(__file__)
TEST_DIR_PATH = py.path.local(os.path.dirname(FILE_PATH))
DATA_PATH = py.path.local(TEST_DIR_PATH).join("data")

@pytest.fixture
def app():
    app = create_app()
    return app

@pytest.mark.options(debug=False)
def test_app(app):
    assert not app.debug, 'Ensure the app not in debug mode'

def test_show_dicom(client):
    assert client.get('/').status_code == 200

def test_dicom_upload(client):
    resp = client.post(
        '/upload',
        data = {
           'photo': (StringIO(DATA_PATH.join('IM-0001-0001.dcm').read()), 'IM-0001-0001.dcm')
        },
        follow_redirects=True
    )
    assert resp.data.find('IM-0001-0001') > -1
    # image thumbnail is shown
    assert resp.data.find('.thumb.jpeg') > -1
