from flask_nav import Nav
from flask_nav.elements import Navbar, View

nav = Nav()

@nav.navigation()
def mynavbar():
    return Navbar(
        View('Dicom Uploader', 'bp.show_dicom_dicoms'),
        View('Browse', 'bp.show_dicoms'),
        View('Upload', 'bp.upload'),
    )
