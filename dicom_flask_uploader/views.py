from flask import Blueprint
from models import db, uploaded_dicoms, Dicom
from flask import request, render_template, url_for, redirect, flash, abort

bp = Blueprint('bp', __name__, template_folder='templates')


@bp.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST' and 'dicom' in request.files:
        filename = uploaded_dicoms.save(request.files['dicom'])
        rec = Dicom(filename=filename)
        db.session.add(rec)
        db.session.commit()
        flash("Upload success!")
        return redirect(url_for('bp.show', id=rec.id))
    return render_template('upload.html')


@bp.route('/dicom/<id>')
def show(id):
    dicom = Dicom.query.get(id)
    if dicom is None:
        abort(404)
    return render_template('dicom.html', dicom=dicom)


@bp.route('/dicoms')
@bp.route('/dicoms/<int:page>')
def show_dicoms(page=1):
    DicomS_PER_PAGE = 25
    dicoms = Dicom.query.paginate(page, DicomS_PER_PAGE, False)
    return render_template('dicoms.html', dicoms=dicoms)


@bp.route('/')
def show_dicom_dicoms():
    return render_template('index.html')
