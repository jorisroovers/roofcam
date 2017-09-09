#!/usr/bin/env python
from setuptools import setup, find_packages
import re
import os

# There is an issue with building python packages in a shared vagrant directory because of how setuptools works
# in python < 2.7.9. We solve this by deleting the filesystem hardlinking capability during build.
# See: http://stackoverflow.com/a/22147112/381010
try:
    del os.link
except:
    pass  # Not all OSes (e.g. windows) support os.link


# shamelessly stolen from mkdocs' setup.py: https://github.com/mkdocs/mkdocs/blob/master/setup.py
def get_version(package):
    """Return package version as listed in `__version__` in `init.py`."""
    init_py = open(os.path.join(package, '__init__.py')).read()
    return re.search("__version__ = ['\"]([^'\"]+)['\"]", init_py).group(1)


setup(
    name="roofcam",
    version=get_version("roofcam"),
    classifiers=[
        "License :: OSI Approved :: MIT License"
    ],
    install_requires=[
        "Flask == 0.12.1",
        "click == 6.7",
        "Pillow==4.0.0"
    ],
    author='Joris Roovers',
    url='https://github.com/jorisroovers/roofcam',
    license='MIT',
    package_data={
        'roofcam': ['files/*']
    },
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "roofcam = roofcam.cli.web:cli",
            "roofcam-web = roofcam.cli.web:cli",
            "roofcam-tools = roofcam.cli.tools:cli"
        ],
    },
)
