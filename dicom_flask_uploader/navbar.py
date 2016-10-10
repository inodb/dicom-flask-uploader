from flask_nav import Nav
from flask_nav.elements import Navbar, View

nav = Nav()

@nav.navigation()
def mynavbar():
    return Navbar(
        View('DICOM Uploader', 'bp.show_dicom_images'),
		View('Browse', 'bp.show_photos'),
		View('Upload', 'bp.upload'),
    )
