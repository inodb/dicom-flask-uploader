from flask_sqlalchemy import SQLAlchemy
from flask_uploads import UploadSet
import mudicom
from dicom_handler import create_thumbnail

db = SQLAlchemy()
uploaded_dicoms = UploadSet('dicoms', extensions=('dcm'))


class Dicom(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    _filename = db.Column('filename', db.String(120))
    data_elements = db.relationship('DicomDataElement', backref='dicom',
                                    lazy='dynamic')

    def __init__(self, filename):
        self.filename = filename
        self.data_elements = self._generate_data_elements(filename)

        # Create thumbnail
        fp = uploaded_dicoms.path(self.filename)
        thumbnail_fp = fp.replace('.dcm', '.thumb.jpeg')
        create_thumbnail(str(fp), str(thumbnail_fp))

    @property
    def thumbnail_filename(self):
        return self._filename.replace(".dcm", ".thumb.jpeg")

    @property
    def filename(self):
        return self._filename

    @filename.setter
    def filename(self, filename):
        self._filename = filename

    @property
    def filename_url(self):
        return uploaded_dicoms.url(self.filename)

    @property
    def thumbnail_url(self):
        return uploaded_dicoms.url(self.thumbnail_filename)

    def _generate_data_elements(self, filename):
        mu = mudicom.load(uploaded_dicoms.path(filename))
        return [DicomDataElement(e) for e in mu.find()]


class DicomDataElement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    value = db.Column(db.Text())
    dicom_id = db.Column(db.Integer, db.ForeignKey('dicom.id'))

    def __init__(self, data_element):
        """Takes mudicom DataElement object or any other object with name, value
        attributes"""
        self.name = data_element.name
        self.value = data_element.value
