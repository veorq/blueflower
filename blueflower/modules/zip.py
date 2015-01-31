# copyright (c) 2014 JP Aumasson <jeanphilippe.aumasson@gmail.com>
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


import io
import os
import zipfile

from blueflower.do import do_data
from blueflower.constants import BF_ZIP, ENCRYPTED
from blueflower.types import type_data
from blueflower.utils.log import log_encrypted, log_error, log_secret
from blueflower.core import RGX_INFILENAME


def zip_do_zip(azip, afile):
    """ azip:ZipFile, afile:source archive(s) name """
    # test if encrypted
    try:
        azip.testzip()
    except RuntimeError as e:
        if 'encrypted' in str(e):
            log_encrypted(BF_ZIP, afile)
            return
        else:
            log_error(str(e), afile)

    # iterate directly over file names
    for member in azip.namelist():
        # sort directories out
        if member.endswith('/'):
            continue
        # check file name
        filename = os.path.basename(member).lower()
        res = RGX_INFILENAME.search(filename)
        if res:
            log_secret(res.group(), afile+':'+member)

        # check file content, calling other modules
        data = azip.read(member)
        (ftype, supported) = type_data(data, member)
        if supported:
            if ftype in ENCRYPTED:
                log_encrypted(ftype, member)
            else:
                do_data(ftype, data, afile+':'+member)


def zip_do_data(data, afile):
    filelike = io.BytesIO(data)
    try:
        azip = zipfile.ZipFile(filelike)
    except zipfile.BadZipfile as e:
        log_error(str(e), afile)
        return
    zip_do_zip(azip, afile)
    azip.close()


def zip_do_file(afile):
    try:
        azip = zipfile.ZipFile(afile)
    except zipfile.BadZipfile as e:
        log_error(str(e), afile)
        return
    zip_do_zip(azip, afile)
    azip.close()
