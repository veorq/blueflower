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

from binascii import b2a_hex

from blueflower.utils.siphash import SipHash

HASH_BYTES = 8
SALT_BYTES = 8
SIPHASH_FAST = SipHash(2, 2)
SIPHASH_SLOW = SipHash(1000, 100000)


def tohex(anint):
    """hex() without 0x...L"""
    return format(anint, 'x').zfill(16)


def key_derivation(pwd, salt=''):
    """returns (key, verifier, salt) where
        * key is a 128-bit int (as siphash.SipHash requires)
        * verifier is an 8-byte string
        * salt is an 8-byte string
    """
    # if salt not given, pick a random one
    if not salt:
        salt = b2a_hex(os.urandom(SALT_BYTES))

    # key generation
    salt_as_int = int(salt, 16)
    mask = 0xffffffffffffffff
    key_hi = SIPHASH_SLOW(pwd+'0', salt_as_int) & mask
    key_lo = SIPHASH_SLOW(pwd+'1', salt_as_int) & mask
    key = (key_hi << 64) | key_lo

    # verifier generation
    verifier = tohex(SIPHASH_FAST(salt, key))

    return (key, verifier, salt)


def hash_string(astring, key):
    return tohex(SIPHASH_FAST(astring, key))
