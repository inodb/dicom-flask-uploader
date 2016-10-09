import flask
from flask import Flask, request, session, render_template, url_for, redirect, \
	flash, send_from_directory
from werkzeug.utils import secure_filename
from flask_uploads import UploadSet, configure_uploads, UploadNotAllowed
from flask_sqlalchemy import SQLAlchemy
import os
from models import db, Photo


# init app
app = Flask(__name__)
app.config.update({
    'SECRET_KEY': 'dev key',
    'USERNAME': 'admin',
    'PASSWORD': 'default',
	'UPLOADED_PHOTOS_DEST': '/tmp/dicom-flask-uploader',
	'SQLALCHEMY_DATABASE_URI': 'sqlite:////tmp/test.db',
	'SQLALCHEMY_TRACK_MODIFICATIONS': False,
})
app.config.from_envvar('PHOTOLOG_SETTINGS', silent=True)
db.init_app(app)

# uploads
uploaded_photos = UploadSet('photos', extensions=('dcm', 'jpeg'))
configure_uploads(app, uploaded_photos)


@app.cli.command('initdb')
def init_db_command():
	"""Initialize the database."""
	db.create_all()


@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(flask.g, 'sqlite_db'):
		g.sqlite_db.close()


@app.route('/upload', methods=['GET', 'POST'])
def upload():
	if request.method == 'POST' and 'photo' in request.files:
		filename = uploaded_photos.save(request.files['photo'])
		user = flask.g.get('user', None)
		rec = Photo(filename=filename)
		db.session.add(rec)
		db.session.commit()
		flash("Upload success!")
		return redirect(url_for('show', id=rec.id))
	return render_template('upload.html')


@app.route('/photo/<id>')
def show(id):
    photo = Photo.query.get(id)
    if photo is None:
        abort(404)
    url = uploaded_photos.url(photo.filename)
    return render_template('show.html', url=url, photo=photo)


@app.route('/photos')
def show_photos():
	photos = Photo.query.all()
	for photo in photos:
		photo.url = uploaded_photos.url(photo.filename)
	return render_template('dicom_images_list.html', photos=photos)


@app.route('/')
def show_dicom_images():
    return 'Hello, World!'


# launch
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
