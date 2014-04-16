# core.py
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


import logging
import os
import re
import sys

from blueflower.do       import do_file
from blueflower.settings import INFILENAME, PROGRAM, SKIP
from blueflower.types    import types_file
from blueflower.utils    import log, timestamp


def select(directory):
    selected = []

    infilename = re.compile('|'.join(INFILENAME))

    for root, dirs, files in os.walk(directory):
        for skip in SKIP:
            if skip in dirs:
                dirs.remove(skip)

        for afile in files:
            fabs = os.path.abspath(os.path.join(root, afile))

            res = infilename.search(afile.lower())
            if res:
                log('SECRET? %s in %s' % (res.group(), fabs))

            (ftype, keep) = types_file(fabs)

            if keep: 
                selected.append((fabs, ftype))
                log('SELECTED: %s' % fabs)

    return selected


def process(selected):
    for afile, ftype in selected:
        do_file(ftype, afile)


def usage():
    print 'usage: %s directory' % PROGRAM


def main(args=sys.argv[1:]):
    if (len(args) < 1):
        usage()
        return 1
    arg = args[0]

    if not os.path.exists(arg):
        print '%s does not exist' % arg
        usage(arg)
        return 1

    logfile = '%s-%s' % (PROGRAM, timestamp())
    print 'LOG to %s' % logfile
    logging.basicConfig(filename=logfile, 
                        format='%(message)s',
                        level=logging.INFO)

    log('# %s: starting %s' % (timestamp(), PROGRAM) )
    selected = select(arg)
    log('# %s: %d files selected' % (timestamp(), len(selected)) )
    process(selected)
    log('# %s: completed' % timestamp() )


if __name__ == '__main__':
    main()
