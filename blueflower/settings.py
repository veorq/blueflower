# settings.py
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


INFILE = (
'pass phrase',
'passphrase',
'password',
'private key',
'secret key',
'sshhostkeys',
)

INFILENAME = (
'connect.inc',      # sql
'default.pass',     # dbman
'htaccess',         # apache/nginx
'id_ecdsa',         # openssh
'id_dsa',           # openssh
'id_rsa',           # openssh
'localconf',        # typo3
'localsettings',    # wikimedia
'passwd',           # *nix & htpasswd
'passlist',         # misc
'passwords',        # misc
'pgplog',           # pgp
'pgppolicy.xml',    # pgp
'pgpprefs.xml',     # pgp
'private',          # misc
'secret',           # misc
'secring',          # gnupg
'sftp-config',      # sftp
'shadow',           # *nix
'spwd.bd',          # freebsd
'users.xml',        # .net
'wallet.dat',       # bitcoin
)

PROGRAM = 'blueflower'

SKIP = (
'.hg', 
'.git', 
'.svn',
)

