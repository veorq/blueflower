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
import gzip

from blueflower.do import do_data
from blueflower.types import type_data
from blueflower.utils.log import log_error


# except when reading the file
def gz_do_gz(agz, afile):
    """agz:GzipFile, afile:source file name"""
    try:
        data = agz.read()
    except IOError as e:
        log_error(str(e), afile)
        return
    (ftype, supported) = type_data(data)
    if supported:
        # strip any .gz extension 
        (root, ext) = os.path.splitext(afile)
        if ext.lower() == '.gz':
            do_data(ftype, data, afile+':'+root)
        else:
            do_data(ftype, data, afile)


def gz_do_data(data, afile):
    filelike = io.BytesIO(data)
    try:
        agz = gzip.GzipFile(fileobj=filelike)
    except IOError as e:
        log_error(str(e), afile)
        return
    gz_do_gz(agz, afile)
    agz.close()


def gz_do_file(afile):
    try:
        agz = gzip.GzipFile(afile)
    except IOError as e:
        log_error(str(e), afile)
        return
    gz_do_gz(agz, afile)
    agz.close()
