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


import getpass
import os
import re
import sys

from blueflower.utils.hashing import hash_string, key_derivation


EXTENSION = '.hashes'


def usage():
    print 'usage: %s file' % os.path.basename(__file__)
    print 'file must include one string per line'


def main():
    if (len(sys.argv) < 2):
        usage()
        return 1 

    if not os.path.exists(sys.argv[1]):
        print '%s does not exist' % sys.argv[1]
        usage()
        return 1
    else:
        path = sys.argv[1]

    # ask for regex, check, copy at top of file
    regex = raw_input('regex: ')
    try:
        re.compile(regex)
    except re.error:
        print 'error: invalid regex'
        return 1

    # prompt for password, derive key
    pwd = getpass.getpass('password: ')
    (key, verifier, salt) = key_derivation(pwd)  

    # create output file at the place as input
    hashesfile = path + EXTENSION
    try:
        fout = open(hashesfile, 'w')
    except IOError:
        print 'error: failed to create %s' % hashesfile

    # write regex, salt, and verifier
    towrite = '%s\n%s,%s\n' % (regex, salt, verifier)
    fout.write(towrite)

    # speed not critical, so write line per line
    with open(path) as fin:
        for line in fin:
            linestring = line.rstrip('\n').strip()
            towrite = '%s\n' % hash_string(linestring, key)
            fout.write(towrite)
    fout.close()


if __name__ == '__main__':
    sys.exit(main())
