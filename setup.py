"""
Setup script for the project.

This script provides information about the project and dependencies,
and allows you to build, install, and distribute the project.

Usage
-----
To build the project:
    python setup.py build

To install the project:
    python setup.py install

To distribute the project:
    python setup.py sdist bdist_wheel

Author
------
Nimba SMS <open-source@nimbasms.com>
"""

import setuptools

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name="nimbasms",
    version="1.0.2",
    author="Nimba SMS",
    description="Python Client Nimba SMS API",
    author_email='open-source@nimbasms.com',
    url='https://github.com/nimbasms/nimbasms-python',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    py_modules=["nimbasms"],
    install_requires=['requests']
)
