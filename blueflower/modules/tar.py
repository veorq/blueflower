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
import tarfile

from blueflower.do import do_data
from blueflower.constants import ENCRYPTED
from blueflower.types import type_data
from blueflower.utils.log import log_encrypted, log_error, log_secret
from blueflower.core import RGX_INFILENAME


def tar_do_tar(atar, afile):
    """ atar:TarFile, afile:source archive(s) name """
    # iterate over TarInfo's
    for member in atar.getmembers():
        # only process files
        if not member.isfile():
            continue
        # check file name
        filename = os.path.basename(member.name).lower()
        res = RGX_INFILENAME.search(filename)
        if res:
            log_secret(res.group(), afile+':'+member.name)

        # check file content, calling other modules
        data = atar.extractfile(member).read()
        (ftype, supported) = type_data(data, member.name)
        if supported:
            if ftype in ENCRYPTED:
                log_encrypted(ftype, member.name)
            else:
                do_data(ftype, data, afile+':'+member.name)


def tar_do_data(data, afile):
    filelike = io.BytesIO(data)
    try:
        atar = tarfile.open(fileobj=filelike)
    except tarfile.TarError as e:
        log_error(str(e), afile)
        return
    tar_do_tar(atar, afile)
    atar.close()


def tar_do_file(afile):
    try:
        atar = tarfile.open(afile)
    except tarfile.TarError as e:
        log_error(str(e), afile)
        return
    tar_do_tar(atar, afile)
    atar.close()
