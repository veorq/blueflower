# types.py
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


import os
import magic

from blueflower.utils import log_error
import blueflower.constants as constants


def types_from_mime(mime):
    (mimetype, mimesubtype) = mime.split('/')
    if mimesubtype == 'x-bzip2':
        return (constants.BF_BZIP2, True)
    elif mimetype == 'text':
        return (constants.BF_TEXT, True)
    elif mimesubtype == 'x-gzip':
        return (constants.BF_GZ, True)
    elif mimesubtype == 'pdf':
        return (constants.BF_PDF, True)
    elif mimesubtype == 'x-rar':
        return (constants.BF_RAR, True)
    elif mimesubtype == 'x-tar':
        return (constants.BF_TAR, True)
    elif mimesubtype == 'zip':
        return (constants.BF_ZIP, True)
    return (constants.BF_UNKNOWN, False)


def types_from_extension(filename):
    if filename == '':
        return (constants.BF_UNKNOWN, False)
    (_, ext) = os.path.splitext(filename)
    if ext in constants.EXTENSIONS:
        return (constants.EXTENSIONS[ext], True)
    return (constants.BF_UNKNOWN, False)


def types_from_signature(data):
    """guesses a file's type based on signature """
    # TODO


def types_find(mime, afile=''):
    """guess a file's type based on mime type and extension
    """
    (ftype, keep) = types_from_mime(mime)
    if ftype != constants.BF_UNKNOWN:
        return (ftype, keep)
    # no type recognized: extension heuristics 
    # TODO
    return types_from_extension(afile)



def types_data(data, afile=''):
    """guess an in-memory file's type
       optional file name (as found in archive or decompressed) 
    """
    try:
        mime = magic.from_buffer(data, mime=True)
    except IOError:
        log_error('IOError', '_data')
        return ('other', False)
    return types_find(mime, afile)
    # if unknown, test signature manually


def types_file(afile):
    """guess a file's type"""
    try:
        mime = magic.from_file(afile, mime=True)
    except IOError:
        log_error('IOError', afile)
        return ('other', False)
    return types_find(mime, afile)
    # if unknown, test signature manually
  
