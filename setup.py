import io
import os
import re

from setuptools import find_packages
from setuptools import setup


with open('README.rst') as readme_file:
    readme = readme_file.read()

# with open('HISTORY.rst') as history_file:
#     history = history_file.read()

requirements = ['Click>=6.0', ]

setup_requirements = []

test_requirements = []


setup(
    name="leventis",
    version="0.1.0",
    url="https://github.com/NaturalHistoryMuseum/leventis",
    license='MIT',

    author="Ben Scott",
    author_email="ben@benscott.co.uk",

    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],

    description="Leventis OCR",
    long_description=readme,

    packages=find_packages(exclude=('tests',)),

    install_requires=requirements,
    setup_requires=setup_requirements,

    test_suite='tests',
    tests_require=test_requirements,

    entry_points={
        'console_scripts': [
            'leventis=leventis.cli:leventis',
        ],
    },
)
