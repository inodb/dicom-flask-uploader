import errno
import os
import shutil
import subprocess
from setuptools import Command


def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


def rm_rf(path):
    if os.path.isdir(path):
        shutil.rmtree(path)
    elif os.path.exists(path):
        os.remove(path)


def find_recursively(path, test_function):
    rv = []

    for root, dirs, files in os.walk(path):
        for file in files:
            if test_function(file):
                rv += [os.path.join(root, file)]

    return rv
