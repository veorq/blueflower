# text.py
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


import re

from blueflower.settings import INFILE
from blueflower.utils import log


def text_do_data(data, afile):
    buf = data.lower()
    infile = re.compile('|'.join(INFILE)) 
    res = infile.search(buf)
    if res:
        log('SECRET? %s in %s' % (res.group(), afile))


def text_do_file(afile):
    try:
        fid = open(afile, 'r') 
    except IOError:
        log('IOError: %s' % afile)
        return
    data = fid.read()
    fid.close()
    text_do_data(data, afile)


