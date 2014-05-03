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


# regexes, case insensitive
INFILE = (
'begin certificate',
'pass phrase',
'passphrase',
'password',
'privatekey',
'private key',
'rsakeypair',
'secret key',
'secretkey',
'sshhostkeys',
)

# regexes, case insensitive
# extensions \.* match names like *.pgd.backup etc.
# signature
# extensions of encrypted containers in types_from_extension
# if extension is missing, type may be detected in types_from_signature
INFILENAME = (
'\.jks',            # java key store
'\.kdb',            # keypass (matches .kdbx)
'\.keychain',       # apple keychain
'\.kwallet',        # kwallet
'\.psafe3',         # passwordsafe
'connect.inc',      # sql
'default\.pass',    # dbman
'htaccess',         # apache/nginx
'id_dsa',           # openssh
'id_ecdsa',         # openssh
'id_rsa',           # openssh
'localconf',        # typo3
'localsettings',    # wikimedia
'passlist',         # misc
'passwd',           # *nix & htpasswd
'passwords',        # misc
'pgplog',           # pgp
'pgppolicy\.xml',   # pgp
'pgpprefs\.xml',    # pgp
'private',          # misc
'secret',           # misc
'secring',          # gnupg
'sftp-config',      # sftp
'shadow',           # *nix
'spwd\.bd',         # freebsd
'users\.xml',       # .net
'wallet\.dat',      # bitcoin
)

PROGRAM = 'blueflower'

SKIP = (
'.hg', 
'.git', 
'.svn',
)

BF_BZIP2 = 'bzip2'
BF_DOC = 'doc'
BF_DOCX = 'docx'
BF_GZ = 'gz'
BF_PDF = 'pdf'
BF_RAR = 'rar'
BF_TAR = 'tar'
BF_TEXT = 'text'
BF_ZIP = 'zip'
BF_PGP = 'pgp'
BF_PGD = 'pgd'
BF_GPG = 'gpg'
BF_TRUECRYPT = 'truecrypt'

BF_UNKNOWN = 'unknown'

EXTENSIONS = {
'.doc':BF_DOC,
'.docx':BF_DOCX,
'.gpg':BF_GPG,
'.pgd':BF_PGD,
'.pgp':BF_PGP,
'.tc':BF_TRUECRYPT,
}

ENCRYPTED = (
BF_GPG,
BF_PGD,
BF_PGP,
BF_TRUECRYPT,
)
