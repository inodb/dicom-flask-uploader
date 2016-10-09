import flask
from flask import Flask, request, session, render_template, url_for, redirect, \
    flash, send_from_directory
from werkzeug.utils import secure_filename
from flask_uploads import UploadSet, configure_uploads, UploadNotAllowed
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
import os
from models import db, Photo, uploaded_photos
from views import bp


# init app
def create_app():
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
    Bootstrap(app)
    db.init_app(app)
    configure_uploads(app, uploaded_photos)
    # add views
    app.register_blueprint(bp)

    @app.cli.command('initdb')
    def init_db_command():
        """Initialize the database."""
        db.create_all()

    @app.cli.command('cleardb')
    def clear_db_command():
        """Initialize the database."""
        db.drop_all()

    @app.teardown_appcontext
    def close_db(error):
        """Closes the database again at the end of the request."""
        if hasattr(flask.g, 'sqlite_db'):
            g.sqlite_db.close()

    return app


# launch
if __name__ == "__main__":
    app = create_app()
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
