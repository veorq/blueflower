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


import magic

from blueflower.utils import log

"""
types handles:

'other'    unknown or unsupported

'bzip2'    bzip2
'gz'       gzip
'pdf'	   pdf
'rar'      rar
'tar'      tar archive (potentially tar.gz and tar.bz2,
           but those are processed as gz and bz2 first)
'text'	   text/* (txt, html, csv, xml, etc.)
'zip'      zip
"""


def types_filter(mime):
    (mimetype, mimesubtype) = mime.split('/')
    if mimesubtype == 'x-bzip2':
        return ('bzip2', True)
    elif mimetype == 'text':
        return ('text', True)
    elif mimesubtype == 'x-gzip':
        return ('gz', True)
    elif mimesubtype == 'pdf':
        return ('pdf', True)
    elif mimesubtype == 'x-rar':
        return ('rar', True)
    elif mimesubtype == 'x-tar':
        return ('tar', True)
    elif mimesubtype == 'zip':
        return ('zip', True)
    else:
        return ('other', False)


def types_data( data ):
    try:
        mime = magic.from_buffer(data, mime=True)
    except IOError:
        log('IOError: type_data')
        return ('other', False)
    return types_filter(mime)


def types_file( afile ):
    try:
        mime = magic.from_file(afile, mime=True)
    except IOError:
        log('IOError: %s' % afile)
        return ('other', False)
    return types_filter(mime)
  
