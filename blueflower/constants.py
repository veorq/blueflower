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


PROGRAM = 'blueflower'

# regexes, enter string in lowercase for insensitive matching
INFILE = (
    'begin certificate',
    'begin pgp message',
    'passphrase',
    'password',
    'private[ _-]key',
    'privatekey',
    'rsakeypair',
    'secret[ _-]key',
    'secretkey',
    'sshhostkeys',
)

# regexes, case insensitive
# extensions \.* match names like *.pgd.backup etc.
# signature
# extensions of encrypted containers in types_from_extension
# if extension is missing, type may be detected in types_from_signature
INFILENAME = (
    '\.bek',            # bitlocker
    '\.tpm',            # bitlocker
    '\.fve',            # bitlocker
    '\.asc',            # ascii keys/messages
    '\.crt',            # certs
    '\.jks',            # java key store
    '\.kdb',            # keypass (matches .kdbx)
    '\.key',            # openssl .key, apple .keychain, etc.
    '\.log',            # misc log
    '\.pem',            # PEM-format key
    '\.kwallet',        # kwallet
    '\.ovpn',           # OpenVPN config
    '\.psafe3',         # passwordsafe
    '\.p12',            # PKCS12 data
    '\.p15',            # PKCS15 tokens
    '\.pfx',            # PRX-format keys
    'cert8.db',         # mozilla
    'connect.inc',      # sql
    'default\.pass',    # dbman
    'htaccess',         # apache/nginx
    'id_dsa',           # openssh
    'id_ecdsa',         # openssh
    'id_ed25519',       # openssh
    'id_rsa',           # openssh
    'key3.db',          # mozilla
    'localconf',        # typo3
    'localsettings',    # wikimedia
    'netrc',            # ~/.netrc
    'otr.fingerprints', # libpurple otr fingerprints
    'otr.private_key',  # libpurple otr keys
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

SKIP = (
    '.hg',
    '.git',
    '.svn',
)

BF_BZIP2 = 'bzip2'
BF_DOCX = 'docx'
BF_ELF = 'elf'
BF_GPG = 'gpg'
BF_GZ = 'gz'
BF_PDF = 'pdf'
BF_PE = 'pe'
BF_PGD = 'pgd'
BF_PGP = 'pgp'
BF_TAR = 'tar'
BF_TEXT = 'text'
BF_TRUECRYPT = 'truecrypt'
BF_XLSX = 'xlsx'
BF_ZIP = 'zip'

BF_UNKNOWN = 'unknown'

EXTENSIONS = {
    '.docx': BF_DOCX,
    '.gpg': BF_GPG,
    '.pgd': BF_PGD,
    '.pgp': BF_PGP,
    '.tar': BF_TAR,
    '.tc': BF_TRUECRYPT,
    '.xlsx': BF_XLSX,
}

ENCRYPTED = (
    BF_GPG,
    BF_PGD,
    BF_PGP,
    BF_TRUECRYPT,
)

EXE = (
    BF_ELF,
    BF_PE,
)
