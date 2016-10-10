import pytest
from dicom_flask_uploader.dicom_handler import create_thumbnail
import os
import py

FILE_PATH = os.path.realpath(__file__)
TEST_DIR_PATH = py.path.local(os.path.dirname(FILE_PATH))
DATA_PATH = py.path.local(TEST_DIR_PATH).join("data")


def test_create_thumbnail_exists(tmpdir):
    infile = str(DATA_PATH.join("IM-0001-0001.dcm"))
    outfile = str(tmpdir.join("thumb.jpeg"))

    create_thumbnail(infile, outfile)
    assert os.path.exists(outfile)

def test_create_thumbnail_same_contents(tmpdir):
    infile = str(DATA_PATH.join("IM-0001-0001.dcm"))
    outfile = str(tmpdir.join("thumb.jpeg"))
    comparefile = str(DATA_PATH.join("IM-0001-0001.thumb.jpeg"))

    create_thumbnail(infile, outfile, size=(64,64))
    assert open(outfile).read() == open(comparefile).read()
