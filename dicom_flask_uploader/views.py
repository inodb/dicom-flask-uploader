import flask
from flask import Blueprint
from models import db, uploaded_photos, Photo
from flask import request, session, render_template, url_for, redirect, \
    flash, send_from_directory
from dicom_handler import create_thumbnail_mudicom

bp = Blueprint('bp', __name__, template_folder='templates')


@bp.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST' and 'photo' in request.files:
        filename = uploaded_photos.save(request.files['photo'])
        fp = uploaded_photos.path(filename)
        thumbnail_fp = fp.replace('.dcm', '.thumb.jpeg')
        create_thumbnail_mudicom(str(fp), str(thumbnail_fp))
        user = flask.g.get('user', None)
        rec = Photo(filename=filename)
        db.session.add(rec)
        db.session.commit()
        flash("Upload success!")
        return redirect(url_for('bp.show', id=rec.id))
    return render_template('upload.html')


@bp.route('/photo/<id>')
def show(id):
    photo = Photo.query.get(id)
    if photo is None:
        abort(404)
    return render_template('show.html', photo=photo)


@bp.route('/photos')
def show_photos():
    photos = Photo.query.all()
    return render_template('dicom_images_list.html', photos=photos)


@bp.route('/')
def show_dicom_images():
    return render_template('index.html')
