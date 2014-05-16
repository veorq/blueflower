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


import os


from blueflower.utils.log import log_error
import blueflower.constants as const


SIGNATURES_DICT = {
'\x1f\x8b\x08': const.BF_GZ,
'\x25\x50\x44\x46': const.BF_PDF,
'\x42\x5a\x68': const.BF_BZIP2,
'\x50\x4b\x03\x04': const.BF_ZIP,
}

MAX_LEN = 1024  # to determine whether text or binary

MAX_SIG_LEN = max(len(x) for x in SIGNATURES_DICT)

is_binary_string = lambda bytes: bool(bytes.translate(None, textchars))

TEXTCHARS = ''.join(map(chr, [7,8,9,10,12,13,27] + range(0x20, 0x100)))


def is_text(data):
    """True if data is text content, False otherwise"""
    return not bool(data.translate(None, TEXTCHARS)) 


def type_from_signature(first_bytes):
    """identifies supported types from signature"""
    for sig, filetype in SIGNATURES_DICT.items():
        if first_bytes.startswith(sig):
            return (filetype, True)
    return (const.BF_UNKNOWN, False)


def type_from_extension(filename):
    """identifies supported types from file extension (for types to be
       processed, or encrypted containers);
       some types being misrecognized (some .docx as zip, etc.), it is
       called before types_from_mime
    """
    if not filename:
        return (const.BF_UNKNOWN, False)
    (_, ext) = os.path.splitext(filename)
    if ext.lower() in const.EXTENSIONS:
        return (const.EXTENSIONS[ext], True)
    return (const.BF_UNKNOWN, False)


def find_type(data, afile=''):
    """guess a file's type based on signature and extension"""
    (ftype, supported) = type_from_extension(afile)
    if supported:
        return (ftype, supported)
    if is_text(data[:MAX_LEN]):
        return (const.BF_TEXT, True)
    return type_from_signature(data[:MAX_SIG_LEN])


def type_data(data, afile=''):
    """guess an in-memory file's type
       optional file name (as found in archive or decompressed) 
    """
    return find_type(data, afile)


def type_file(afile):
    """guess a file's type"""
    try:
        fin = open(afile)
    except IOError as e:
        log_error(str(e), afile)
        return
    data = fin.read(MAX_LEN)
    return find_type(data, afile)
