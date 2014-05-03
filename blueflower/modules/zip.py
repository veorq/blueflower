# zip.py
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


import io
import os
import re
import zipfile

from blueflower.do import do_data
from blueflower.constants import BF_ZIP, ENCRYPTED, INFILENAME
from blueflower.types import types_data
from blueflower.utils import log_encrypted, log_error, log_secret


def zip_do_zip(azip, afile):
    """ azip:ZipFile, afile:source archive(s) name """
    # test if encrypted
    try:
        azip.testzip()
    except RuntimeError as exception:
        if 'encrypted' in str(exception):
            log_encrypted(BF_ZIP, afile)
            return

    infilename = re.compile('|'.join(INFILENAME))

    # iterate directly over file names 
    for member in azip.namelist():
        # sort directories out
        if member.endswith('/'):
            continue
        # check file name
        filename =  os.path.basename(member).lower()
        res = infilename.search(filename)
        if res:
            log_secret(res.group(), afile+':'+member)

        # check file content, calling other modules
        data = azip.read(member)
        (ftype, keep) = types_data(data, member)
        if keep:
            if ftype in ENCRYPTED:
                log_encrypted(ftype, member)
            else:
                do_data(ftype, data, afile+':'+member)


def zip_do_data(data, afile):
    filelike = io.BytesIO(data)
    try:
        azip = zipfile.ZipFile(filelike)
    except zipfile.BadZipfile:
        log_error('zipfile.BadZipFile', afile)
        return
    zip_do_zip(azip, afile)
    azip.close()


def zip_do_file(afile):
    try:
        azip = zipfile.ZipFile(afile)
    except zipfile.BadZipfile:
        log_error('zipfile.BadZipFile', afile)
        return
    zip_do_zip(azip, afile)
    azip.close()

