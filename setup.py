# -*- coding: utf-8 -*-
import sys
from setuptools import setup, find_packages

classifiers = [
]

install_requires = [
    'Sphinx',
    'catkin_pkg',
]

test_require = ['sphinx-testing', 'beautifulsoup4']

if sys.version_info < (3, 3):
    test_require.append('mock')

setup(
    name='sphinxcontrib-ros',
    version='0.1.0',
    description='Sphinx extension for ROS(Robot Operating System)',
    classifiers=classifiers,
    keywords=['sphinx', 'ros'],
    author='otamachan',
    author_email='otamachan at gmail.com',
    url='https://github.com/otamachan/sphinxcontrib-ros.git',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    include_package_data=True,
    install_requires=install_requires,
    tests_require=test_require,
)
