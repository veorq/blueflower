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


import math
from blueflower.utils.log import log_error


def entropy2(data):
    if not data:
        return 0
    entropy = 0
    for byte in range(256):
        prob = float(data.count(chr(byte)))/len(data)
        if prob:
            entropy += - prob*math.log(prob, 2)
    return entropy


def looks_uniform(data='', filename=''):
    """to detect compressed/encrypted data, packed executables etc.
       unreliable for short samples (<~100 bytes)
       if no data given, opens the file"""
    if not data:
        try:
            data_local = open(filename).read()
        except IOError as e:
            log_error(str(e), filename)
            return False
    else:
        # beware mutable default args
        data_local = data
    datalen = len(data_local)
    entropy = entropy2(data_local)
    if datalen < 250:
        return entropy > 6
    if datalen < 1000:
        return entropy > 7
    return entropy > 7.5

