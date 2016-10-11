[![Build Status](https://travis-ci.org/inodb/dicom-flask-uploader.svg?branch=master)](https://travis-ci.org/inodb/dicom-flask-uploader)
[![codecov](https://codecov.io/gh/inodb/dicom-flask-uploader/branch/master/graph/badge.svg)](https://codecov.io/gh/inodb/dicom-flask-uploader)
[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)
# dicom-flask-uploader
Python Web Server in Flask that allows users to upload & browse
[DICOM](https://en.wikipedia.org/wiki/DICOM) images. Under the hood
[mudicom](https://github.com/neurosnap/mudicom) and
[gdcm](https://github.com/malaterre/GDCM) are used to get key/value info from
the DICOM files. The [pillow](https://github.com/python-pillow/Pillow) library
is used to make the thumbnail.

## How to run
### Using conda + pip
To Deploy, install the dependencies
```bash
conda create -p env/
source activate env/
# You need to install gdcm
conda config --add channels conda-forge
conda install --file requirements/conda.txt
pip install -e .
```
Then run
```bash
export FLASK_APP=dicom-flask-uploader.runapp
flask initdb
flask importdb
flask run
```
To Run Tests
```
source activate env/
pip install -r requirements/development.txt
py.test
```

## Design choices
- Using simple sqlite db at the moment for quick prototyping, but could be
  changed for any other type of relational db that
[flask-sqlalchemy](http://flask-sqlalchemy.pocoo.org/2.1/) supports.
    - Data element key/value sizes picked arbitrarily. Not sure what max limits
      are for DICOM
    - Might actually be better to use nosql db for this, since key/values can
      be different between DICOMs
- Use gdcm so compressed DICOM images can be handled
- Using Jinja2 templating with flask for quick prototyping
- A few tests to show system works

## Further Ideas
- Use that lovely
  [flask-resty-tenants](https://github.com/4Catalyzer/flask-resty-tenants)
library to create REST API
- Add authentication on a per user basis
- Store static files in a persistent manner using
  [flask-annex](https://github.com/4Catalyzer/flask-annex) 
- Seems like some thumbnails are not always properly converted, probably issue
  in mudicom or gdcm
- Add some better error checking (for uploading incorrect image type for
  instance)
- Validate DICOM files and show info to user
- Query DICOM key/value
