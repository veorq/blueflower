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


import re

from blueflower.constants import INFILE
from blueflower.core import HASHES, HASH_KEY, HASH_REGEX
from blueflower.utils.hashing import hash_string
from blueflower.utils.log import log_secret, log_error


def search_hashes(text, afile):
    for match in re.finditer(HASH_REGEX, text):
        ahash = hash_string(match.group(0), HASH_KEY)
        if ahash in HASHES:
            log_secret('hash %s' % ahash, afile)


def text_do_text(text, afile):
    """text: lowercase test, afile: source file name """
    regex = '|'.join(INFILE)
    for match in re.finditer(regex, text):
        log_secret(match.group(), afile)
    if HASHES:
        search_hashes(text, afile)


def text_do_data(data, afile):
    text = data.lower()
    text_do_text(text, afile)


def text_do_file(afile):
    try:
        fid = open(afile)
    except IOError as e:
        log_error(str(e), afile)
        return
    data = fid.read().lower()
    fid.close()
    text_do_data(data, afile)
