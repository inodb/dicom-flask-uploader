from setuptools import Command, setup
import subprocess

# -----------------------------------------------------------------------------


def system(command):
    class SystemCommand(Command):
        user_options = []

        def initialize_options(self):
            pass

        def finalize_options(self):
            pass

        def run(self):
            subprocess.check_call(command, shell=True)

    return SystemCommand


# -----------------------------------------------------------------------------

setup(
    name='dicom-flask-uploader',
    version='0.1.0',
    description="DICOM image uploader in flask",
    url='https://github.com/inodb/dicom-flask-uploader',
    author="Ino de Bruijn",
    author_email='ino@ino.pm',
    license='MIT',
    classifiers=(
        'Development Status :: 2 - Pre-Alpha',
        'Framework :: Flask',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ),
    keywords='dicom flask',
    packages=('dicom_flask_uploader',),
    install_requires=(
        'Flask >= 0.11.1',
        'Flask-Bootstrap >= 3.3.7.0',
        'flask-nav >= 0.5',
        'Flask-SQLAlchemy >= 2.1',
        'Flask-Uploads >= 0.2.1',
        'mudicom >= 0.1.2',
        'pillow >= 3.4.1',
        'mudicom >= 0.1.2',
    ),
    cmdclass={
        'clean': system('rm -rf build dist *.egg-info'),
        'package': system('python setup.py pandoc sdist bdist_wheel'),
        'pandoc': system('pandoc README.md -o README.rst'),
        'publish': system('twine upload dist/*'),
        'release': system('python setup.py clean package publish'),
        'test': system('py.test'),
    },
)
