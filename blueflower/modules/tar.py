# tar.py
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
import tarfile

from blueflower.do import do_data
from blueflower.settings import INFILENAME
from blueflower.types import types_data
from blueflower.utils import log


def tar_do_tar(atar, afile):
    """ atar:TarFile, afile:source archive(s) name """
    infilename = re.compile('|'.join(INFILENAME))

    # iterate over TarInfo's
    for member in atar.getmembers():
        # only process files
        if not member.isfile():
            continue
        # check file name
        filename = os.path.basename(member.name).lower()
        res = infilename.search(filename)
        if res:
            log('SECRET: %s in %s:%s' % \
                (res.group(), afile, member.name))

        # check file content, calling other modules
        data = atar.extractfile(member).read()
        (ftype, keep) = types_data(data)
        if keep:
            do_data(ftype, data, afile+':'+member.name)


def tar_do_data(data, afile):
    filelike = io.BytesIO(data)
    try:
        atar = tarfile.open(fileobj=filelike)
    except tarfile.TarError:
        log('tarfile.TarError: %s' % afile)
        return
    except tarfile.ReadError:
        log('tarfile.ReadError: %s' % afile)
        return
    tar_do_tar(atar, afile)
    atar.close()


def tar_do_file(afile):
    try:
        atar = tarfile.open(afile)
    except tarfile.TarError:
        log('tarfile.TarError: %s' % afile)
        return
    except tarfile.ReadError:
        log('tarfile.ReadError: %s' % afile)
        return
    tar_do_tar(atar, afile)
    atar.close()

