[![Build Status](https://travis-ci.org/inodb/dicom-flask-uploader.svg?branch=master)](https://travis-ci.org/inodb/dicom-flask-uploader)
[![codecov](https://codecov.io/gh/inodb/dicom-flask-uploader/branch/master/graph/badge.svg)](https://codecov.io/gh/inodb/dicom-flask-uploader)
# dicom-flask-uploader
Python Web Server in Flask that allows users to upload & browse
[DICOM](https://en.wikipedia.org/wiki/DICOM) images.

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
flask run
```
To Run Tests
```
source activate env/
pip install -r requirements/development.txt
py.test
```
