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
import io
import csv

from blueflower.core import HASHES, HASH_KEY, HASH_REGEX, RGX_INFILE
from blueflower.utils.hashing import hash_string
from blueflower.utils.log import log_secret, log_error, log_comment


def search_hashes(text, afile):
    for match in re.finditer(HASH_REGEX, text):
        ahash = hash_string(match.group(0), HASH_KEY)
        if ahash in HASHES:
            log_secret('hash %s' % ahash, afile)


def text_do_text(text, afile):
    """text: lowercase test, afile: source file name """
    loggedFilename = False
    lines = text.splitlines()
    for lineno in range(len(lines)):
        line = lines[lineno]
        for match in re.finditer(RGX_INFILE, line):
            start = match.start()
            offset = start - text.rfind('\n', 0, start)
            wrd = match.group(0)

            if not loggedFilename:
                log_secret("")
                log_secret("%s" % (afile))
                loggedFilename = True
            log_secret(",%s,%s,%s" % (lineno, offset, wrd))
     
            if len(lines) > lineno - 2 and 0 < lineno -2 :
                log_text_and_line_number((lineno - 2), lines[lineno-2])
            if len(lines) > lineno - 1 and 0 < lineno -1:
                log_text_and_line_number((lineno - 1), lines[lineno-1])
            log_text_and_line_number(lineno,lines[lineno])
            if len(lines) > lineno + 1:
                log_text_and_line_number((lineno + 1), lines[lineno+1])
            if len(lines) > lineno + 2:
                log_text_and_line_number((lineno + 2), lines[lineno+2])

        #log_secret(match.group(), afile)
    if HASHES:
        search_hashes(text, afile)

def log_text_and_line_number(lineno, text):
    output = io.BytesIO()
    writer = csv.writer(output)
    writer.writerow([text])
    log_secret(",,,,%s %s" % (lineno, output.getvalue().splitlines()[0]))

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

