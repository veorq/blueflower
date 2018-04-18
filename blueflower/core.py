# copyright (c) 2014-15 JP Aumasson <jeanphilippe.aumasson@gmail.com>
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
import logging
import os
import re
import signal
import sys

from blueflower import __version__
from blueflower.constants import ENCRYPTED, EXE, INFILE, INFILENAME, PROGRAM, SKIP
from blueflower.do import do_file
from blueflower.types import type_file
from blueflower.utils.hashing import key_derivation, HASH_BYTES
from blueflower.utils.log import log_comment, log_encrypted, log_error, \
    log_secret, log_exe, log_packed, timestamp
from blueflower.utils.heuristics import looks_uniform


HASHES = frozenset()
HASH_KEY = 0
HASH_REGEX = ''

# compiled regexes used by modules
RGX_INFILE = re.compile('')
RGX_INFILENAME = re.compile('')


class BFException(Exception):
    pass


def get_hashes(hashesfile, pwd):
    """create hashes list from hashesfile using the given password"""
    global HASHES
    global HASH_KEY
    global HASH_REGEX
    log_comment('verifying hashes file %s...' % hashesfile)
    fin = open(hashesfile)
    regex = fin.readline().rstrip('\n')
    try:
        (salt, verifier_from_file) = fin.readline().rstrip('\n').split(',')
    except ValueError:
        raise BFException('failed to extract verifier and salt')

    (key, verifier_from_pwd, salt) = key_derivation(pwd, salt)

    fail = False

    if verifier_from_pwd != verifier_from_file:
        log_comment('verifier does not match (incorrect password?)')
        fail = True
    else:
        HASH_KEY = key
        HASH_REGEX = regex

    try:
        re.compile(regex)
    except re.error:
        log_comment('invalid regex')
        fail = True

    # file pointer is now at the 3rd line:
    hashes = []

    for line in fin:
        ahash = line.strip()
        if len(ahash) != 2*HASH_BYTES:
            log_comment('invalid hash length (%d bytes): %s' %
                        (len(ahash), ahash))
            fail = True
        # check that the hash is an hex value
        try:
            int(ahash, 16)
        except ValueError:
            log_comment('invalid hash value: %s' % ahash)
            fail = True
        if not fail:
            hashes.append(ahash)

    if fail:
        raise BFException('hashes file failed to verify')

    # record hashes and key, notifies of duplicates
    HASHES = frozenset(hashes)
    log_comment('%d hashes read, %d uniques' % (len(hashes), len(HASHES)))
    log_comment('using regex %s' % HASH_REGEX)
    log_comment('hashes file successfully verified')


def init(path):
    """determines size and number of files"""
    log_comment('initializing...')
    total_size = 0
    count = 0

    for root, dirs, files in os.walk(path):
        for skip in SKIP:
            if skip in dirs:
                dirs.remove(skip)
        for filename in files:
            apath = os.path.join(root, filename)
            count += 1
            try:
                total_size += os.path.getsize(apath)
            except OSError as e:
                log_error(str(e), filename)

    readable = total_size

    for unit in ['bytes', 'KiB', 'MiB', 'GiB', 'TiB']:
        if readable < 1024:
            log_comment('%d files, %3.1f %s' % (count, readable, unit))
            return count
        readable /= 1024.0


def scan(path, count):
    """selects files to process, checks file names"""
    log_comment('scanning %s:' % path)
    scanned = 0
    bar_width = 32
    if count < bar_width:
        bar_width = count
    if count == 0:
        bar_width = 1
    sys.stdout.write('%s\n' % ("=" * bar_width))
    bar_blocksize = count / bar_width
    bar_left = bar_width
    bar_count = 0

    for root, dirs, files in os.walk(path):
        for skip in SKIP:
            if skip in dirs:
                dirs.remove(skip)
        for filename in files:
            abspath = os.path.abspath(os.path.join(root, filename))
            res = RGX_INFILENAME.search(filename.lower())
            if res:
                log_secret(res.group(), abspath)

            try:
                ftype, supported = type_file(abspath)
            except TypeError as e:
                log_error(str(e), abspath)
                continue

            if supported:
                if ftype in ENCRYPTED:  
                    # report but do not process
                    log_encrypted(ftype, abspath)
                if ftype in EXE:  
                    # report but do not process
                    if looks_uniform(filename=abspath):
                        log_packed(ftype, abspath)
                    else:
                        log_exe(ftype, abspath)
                else:
                    # process the file
                    do_file(ftype, abspath)
                    scanned += 1

            # update progress bar
            bar_count += 1
            if bar_count >= bar_blocksize and bar_left:
                sys.stdout.write("=")
                sys.stdout.flush()
                bar_count = 0
                bar_left -= 1

    sys.stdout.write("\n")
    log_comment('%d files supported were processed' % scanned)
    return scanned


def count_logged(logfile):
    logs = open(logfile).read()
    secrets = logs.count('SECRET,')
    log_comment('%d files or strings may contain secrets' % secrets)
    encrypted = logs.count('ENCRYPTED,')
    log_comment('%d files look encrypted' % encrypted)
    exe = logs.count('EXE,')
    packed = logs.count('EXE PACKED,')
    log_comment('%d files look executable (including %d packed)' % \
        (exe+packed, packed))


def bye():
    print 'terminating'


def banner():
    print 'starting %s v%s'  % (PROGRAM, __version__)


def signal_handler(*_):
    """interrupt upon ^C"""
    sys.stdout.write("\n")
    log_comment('SIGINT received, quitting')
    sys.exit(0)


def main():
    """main function"""
    parser = argparse.ArgumentParser(description='blueflower\
        <https://github.com/veorq/blueflower>')
    parser.add_argument('path', 
        help='directory to explore')
    parser.add_argument('-H', metavar='hashesfile', required=False,\
        help='hashes file')
    parser.add_argument('-p', metavar='password',\
        help='hashes file password (optional, interactive prompt otherwise)')
    parser.add_argument('-o', metavar='output_file',required=False,\
        help='directory to save the log file')
    parser.add_argument('-d', metavar='dictionaryfile', required=False,\
        help='dictionary file')

    args = parser.parse_args()
    path = args.path
    hashesfile = args.H  # = None if argument missing
    dictionaryfile = args.d # = None if argument missing
    output_file = args.o

    if hashesfile:
        pwd = args.p  # = None if argument missing
        if not pwd:
            pwd = getpass.getpass('password: ')
    else:
        pwd = ''

    signal.signal(signal.SIGINT, signal_handler)

    try:
        blueflower(path, hashesfile, dictionaryfile, pwd, output_file)
    except BFException as e:
        print str(e)
        parser.print_usage()
        return -1
    bye()
    return 0


def blueflower(path, hashesfile, dictionaryfile, pwd, output_file):
    """runs blueflower, returns name of the log file"""
    global RGX_INFILE
    global RGX_INFILENAME

    if not os.path.exists(path):
        raise BFException('%s does not exist' % path)

    if hashesfile and not os.path.exists(hashesfile):
        raise BFException('%s does not exist' % hashesfile)

    if dictionaryfile and not os.path.exists(dictionaryfile):
        raise BFException('%s does not exist' % dictionaryfile)

    if output_file:
        if os.path.isfile(output_file):
            logfile = output_file
        else:
            logfile = output_file + '/%s-%s-%s.csv' % (PROGRAM, os.path.basename(os.path.normpath(path)), timestamp())
    else:
        logfile = '%s-%s-%s.csv' % (PROGRAM, os.path.basename(os.path.normpath(path)), timestamp())

    # reset any existing logger
    logger = logging.getLogger()
    if logger.handlers:
        logger.handlers[0].stream.close()
        logger.removeHandler(logger.handlers[0])

    # instantiate logger
    logging.basicConfig(filename=logfile,
                        format='%(message)s',
                        level=logging.INFO)

    banner()
    log_comment('writing to %s' % logfile)

    # hash file support
    if hashesfile and pwd:
        try:
            get_hashes(hashesfile, pwd)
        except BFException:
            raise

    # read the dictionary and add to INFILE
    if(dictionaryfile):
        extradictionary = load_dictionary_file(dictionaryfile)
    else:
        extradictionary=[]

    # precompile the regexes
    rgx_infile = '|'.join(set(INFILE) | set(extradictionary))
    log_comment(rgx_infile)
    try:
        RGX_INFILE = re.compile(rgx_infile, re.IGNORECASE)
    except re.error:
        raise BFException('invalid infile regex %s' % rgx_infile)
    rgx_infilename = '|'.join(INFILENAME)
    try:
        RGX_INFILENAME = re.compile(rgx_infilename, re.IGNORECASE)
    except re.error:
        raise BFException('invalid infilename regex %s' % rgx_infilename)

    # start slow operations
    count = init(path)
    scan(path, count)
    count_logged(logfile)

    return logfile

def load_dictionary_file(afile):
    log_comment('adding custom dictionary %s to infile' % afile)
    try:
        fid = open(afile)
    except IOError as e:
        log_error(str(e), afile)
        return
    data = fid.read().lower()
    fid.close()
    return data.splitlines()
    
