# bzip2.py
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
import bz2

from blueflower.do import do_data
from blueflower.types import types_data
from blueflower.utils import log

# except when reading the file
def bzip2_do_bzip2(abzip2, afile):
    """abzip2:raw bytes, afile:source file name"""
    try:
        data = bz2.decompress(abzip2)
    except IOError:
        log('IOError: %s' % afile)
        return
    (ftype, keep) = types_data(data)
    if keep:
        # strip any .bz2 extension 
        (root, ext) = os.path.splitext(afile)
        if ext.lower() == '.bz2':
            do_data(ftype, data, afile+':'+root)
        else:
            do_data(ftype, data, afile)


def bzip2_do_data(data, afile):
    bzip2_do_bzip2(data, afile)


def bzip2_do_file(afile):
    try:
        fid = open(afile)
        abzip2 = fid.read()
    except IOError:
        log('IOError: %s' % afile)
        return
    bzip2_do_bzip2(abzip2, afile)
    fid.close()
