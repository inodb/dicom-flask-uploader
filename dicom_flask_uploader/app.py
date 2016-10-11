import flask
from flask import Flask, send_from_directory
from flask_uploads import configure_uploads
from flask_bootstrap import Bootstrap
import os
import sys
from models import db, uploaded_dicoms, Dicom
from StringIO import StringIO
from views import bp
from navbar import nav
from utils import mkdir_p, rm_rf, find_recursively
from werkzeug.test import EnvironBuilder
from werkzeug.wrappers import Request


# init app
def create_app():
    app = Flask(__name__)
    app.config.update({
        'SECRET_KEY': 'dev key',
        'USERNAME': 'admin',
        'PASSWORD': 'default',
        'UPLOADED_DICOMS_DEST': '/tmp/dicom-flask-uploader',
        'SQLALCHEMY_DATABASE_URI': 'sqlite:////tmp/test.db',
        'SQLALCHEMY_TRACK_MODIFICATIONS': False,
        'EXAMPLE_OSIRIX_ZIP_URL':
            os.environ.get(
                'EXAMPLE_OSIRIX_ZIP_URL',
                'http://www.osirix-viewer.com/datasets/DATA/BEAUFIX.zip'
            ),
    })
    app.config.from_envvar('DICOMSLOG_SETTINGS', silent=True)
    Bootstrap(app)
    nav.init_app(app)
    db.init_app(app)
    configure_uploads(app, uploaded_dicoms)
    # add views
    app.register_blueprint(bp)

    @app.cli.command('initdb')
    def init_db_command():
        """Initialize the database."""
        db.create_all()

    @app.cli.command('importdb')
    def import_db_command():
        """Dev function to download exmple data and import"""
        import_db(app.config["EXAMPLE_OSIRIX_ZIP_URL"])

    @app.cli.command('cleardb')
    def clear_db_command():
        """Initialize the database."""
        db.drop_all()

    @app.teardown_appcontext
    def close_db(error):
        """Closes the database again at the end of the request."""
        if hasattr(flask.g, 'sqlite_db'):
            flask.g.sqlite_db.close()

    @app.route('/favicon.ico')
    def favicon():
        return send_from_directory(os.path.join(app.root_path, 'static'),
                                   'ico/favicon.ico',
                                   mimetype='dicom/vnd.microsoft.icon')

    return app


def import_db(zip_url):
    """Dev function to download example data and import"""
    # download
    import_dir = "/tmp/import"
    rm_rf(import_dir)
    mkdir_p(import_dir)
    zip_url = zip_url
    zip_file = zip_url.split('/')[-1]
    os.system("cd {} && curl {} > {}".format(import_dir, zip_url, zip_file))
    os.system("cd {} && unzip {}".format(import_dir, zip_file))

    # find files
    dcms = find_recursively(import_dir, lambda x: x.endswith(".dcm"))

    # import
    for i, filename in enumerate(dcms):
        status_line = "Importing {} of {}".format(i, len(dcms))
        sys.stdout.write(status_line)
        # TODO: contrived way to upload data using werkzeug so UploadSet can be
        # used to store the file
        builder = EnvironBuilder(
            method='POST',
            data={
                'dicom': (StringIO(filename).read(), filename.split('/')[-1])
            }
        )
        env = builder.get_environ()
        request = Request(env)

        upload_filename = uploaded_dicoms.save(request.files['dicom'])
        rec = Dicom(filename=upload_filename)
        db.session.add(rec)

        sys.stdout.write(len(status_line) * '\r')

    db.session.commit()

    # get rid of temp dir
    rm_rf(import_dir)


# launch
if __name__ == "__main__":
    app = create_app()
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
