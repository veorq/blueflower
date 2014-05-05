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
import signal
import sys
import threading

from __init__ import __version__
from blueflower.do       import do_file
from blueflower.constants import ENCRYPTED, INFILENAME, PROGRAM, SKIP
from blueflower.types    import types_file
from blueflower.utils    import log_comment, log_encrypted, log_secret, \
                                log_selected, timestamp

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
                log_secret(res.group(), fabs)

            (ftype, keep) = types_file(fabs)

            if keep: 
                # if encrypted, log and do not process
                if ftype in ENCRYPTED:
                    log_encrypted(ftype, afile)
                # otherwise, select file for processing
                else:
                    selected.append((fabs, ftype))
                    log_selected(ftype, fabs)

    return selected


def process(selected):
    for afile, ftype in selected:
        do_file(ftype, afile)


def usage():
    print 'usage: %s directory' % PROGRAM


def signal_handler(signal, frame):
    log_comment('SIGINT received, quitting')
    sys.exit(1)


def main(args=sys.argv[1:]):
    if (len(args) < 1):
        usage()
        return 1

    if not os.path.exists(args[0]):
        print '%s does not exist' % arg
        usage()
        return 1
    else:
        path=args[0]

    signal.signal(signal.SIGINT, signal_handler)

    logfile = '%s-%s' % (PROGRAM, timestamp())
    logging.basicConfig(filename=logfile, 
                        format='%(message)s',
                        level=logging.INFO)

    log_comment('starting %s version %s' % (PROGRAM, __version__))
    log_comment('writing to %s' % logfile)

    selected = select(path)
    log_comment('%d files selected' % len(selected))
    process(selected)
    log_comment('processing completed')

