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
import threading

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


class blueflowerThread(threading.Thread):
    def __init__(self, path, index):
        self.path = path
        self.index = index
        super(blueflowerThread, self).__init__()

    def run(self):
        selected = select(self.path)
        log_comment('thread %d: %d files selected' % (self.index, len(selected)))
        process(selected)
        log_comment('thread %d: processing completed' % self.index)


def main(args=sys.argv[1:]):
    if (len(args) < 1):
        usage()
        return 1

    for arg in args:
        if not os.path.exists(arg):
            print '%s does not exist' % arg
            usage()
            return 1

    logfile = '%s-%s' % (PROGRAM, timestamp())
    print 'logging to %s' % logfile
    logging.basicConfig(filename=logfile, 
                        format='%(message)s',
                        level=logging.INFO)

    log_comment('starting %s' % PROGRAM)

    bfthreads = []
    for i in xrange(len(args)):
        arg = args[i]
        log_comment('creating thread %d: %s' % (i, arg))
        thread = blueflowerThread(arg, i)
        bfthreads.append(thread)

    log_comment('%d threads created, now starting' % len(bfthreads))

    for thread in bfthreads:
        thread.start()
        
    for thread in bfthreads:
        thread.join()


if __name__ == '__main__':
    main()
