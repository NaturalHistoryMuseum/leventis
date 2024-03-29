import io
import os
import re

from setuptools import find_packages
from setuptools import setup
from glob import glob


with open('README.rst') as readme_file:
    readme = readme_file.read()

requirements = [
    'requests',
    'requests-cache',
    'scikit-learn==0.21.2',
    'click',
    'pandas',
    'Pillow',
    'scispacy==0.2.2',
    'joblib',
    'nltk'
]


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

    ],

    description="Leventis NLP",
    long_description=readme,

    packages=find_packages(exclude=('tests',)),

    package_data={'leventis': ['data/*', 'data/models/*']},

    install_requires=requirements,
    setup_requires=setup_requirements,

    test_suite='tests',
    tests_require=test_requirements,

    entry_points={
        'console_scripts': [
            'leventis=leventis.cli:main',
        ],
    },
)
