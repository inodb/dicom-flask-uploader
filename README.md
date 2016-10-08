# dicom-flask-uploader
Python Web Server in Flask that allows users to upload & browse
[DICOM](https://en.wikipedia.org/wiki/DICOM) images.

## How to run
### Using conda
To Deploy
```bash
conda create -p env/ flask pillow pip
source activate
# You need to install gdcm
conda install --channel https://conda.anaconda.org/conda-forge gdcm
pip install mudicom
```
To Run Tests
```
pip install -r requirements/development.txt
pytest
```
