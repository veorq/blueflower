#
# hashing.py
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

# hashes file format:
#
# 1st line: regex (checked to be valid)
# 2nd line: verifier, salt0
# 3rd line: siphash-2-2(salt1+value1, key), salt1
# 4th line: siphash-2-2(salt2+value2, key), salt2
# etc.
#
# where 
#       (key, verifier, salt) = key_derivation(pwd)
#       '+' denotes strings concatenation
#       hashes are represented as 8-byte hex strings
#       salts are represented as 8-byte hex strings       

import os

from binascii import b2a_hex

from blueflower.utils.siphash import SipHash

HASH_BYTES = 8
SALT_BYTES = 8
SIPHASH = SipHash(2, 2)


def tohex(anint):
    """hex() without 0x...L"""
    return format(anint, 'x').zfill(16)


def key_derivation(pwd, salt=''):
    """returns (key, verifier, salt) where 
        * key is a 128-bit int (as siphash.SipHash requires)
        * verifier is an 8-byte string
        * salt is an 8-byte string
    the same salt is used for key and verifier generation
    """
    c_key = 1000
    d_key = 100000
    siphash_key = SipHash(c_key, d_key)

    c_verifier = 2
    d_verifier = 2
    siphash_verifier = SipHash(c_verifier, d_verifier)

    # if salt not given, pick a random one
    if not salt:
        salt = b2a_hex(os.urandom(8))

    salt_as_int = int(salt, 16)

    key = (siphash_key(pwd+'0', salt_as_int)<<64) | \
           siphash_key(pwd+'1', salt_as_int)

    verifier = tohex(siphash_verifier(salt, key))
    return (key, verifier, salt)


def hash_string(astring, key):

    return tohex(SIPHASH(astring, key))
