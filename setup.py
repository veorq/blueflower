#!/usr/bin/python
#
# setup.py
#
# This file is part of blueflower.
# 
# blueflower is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# blueflower is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with blueflower.  If not, see <http://www.gnu.org/licenses/>.
#
#
# Copyright 2014 JP Aumasson <jeanphilippe.aumasson@gmail.com>


from setuptools import setup
import blueflower

requirements = [
    'xlrd>=0.9.3',
    'pyPdf>=1.13',
    'python-magic>=0.4.6',
    'rarfile>=2.6',
]

setup(
    name='blueflower',
    version=blueflower.__version__,
    description='simple tool searching for private keys, passwords, etc.',
    long_description=open('README.md').read(),
    url='https://github.com/veorq/blueflower',
    author=blueflower.__author__,
    author_email='jeanphilippe.aumasson@gmail.com',
    license=blueflower.__licence__,
    packages=['blueflower', 'blueflower.modules'],
    entry_points={
        'console_scripts': [
            'blueflower = blueflower.__main__:main',
        ],
    },
    install_requires=requirements,
)
