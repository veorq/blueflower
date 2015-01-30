#!/usr/bin/env python

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


import argparse
import getpass
import os
import re
import sys

from blueflower.utils.hashing import hash_string, key_derivation

EXTENSION = '.hashes'


def makehashes(path, regex, pwd):
    (key, verifier, salt) = key_derivation(pwd)

    # create output file at the place as input
    hashesfile = path + EXTENSION
    try:
        fout = open(hashesfile, 'w')
    except IOError:
        print 'error: failed to create %s' % hashesfile
        return 1

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

    return 0


def main():

    parser = argparse.ArgumentParser(\
        description='builds password-protected hashes for hiding strings\
            searched; see <https://github.com/veorq/blueflower#hashes-file>')
    parser.add_argument('-p', metavar='password', required=False,\
        help='password')
    parser.add_argument('path',\
        help='file containing strings to detect (one per line)')
    parser.add_argument('regex',\
        help='regex matching the strings to detect')
    args = parser.parse_args()

    # get path
    path = args.path
    if not os.path.exists(path):
        print 'error: %s does not exist' % path
        parser.print_usage()
        return 1

    # get regex and check validity
    regex = args.regex
    try:
        re.compile(regex)
    except re.error:
        print 'error: invalid regex'
        parser.print_usage()
        return 1

    # get password and derive values
    if args.p:
        pwd = args.p
    else:
        pwd = getpass.getpass('password: ')

    return makehashes(path, regex, pwd)


if __name__ == '__main__':
    sys.exit(main())
