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


import blueflower.constants as constants


def do_data(ftype, data, afile):
    if ftype == constants.BF_UNKNOWN:
        return
    elif ftype == constants.BF_BZIP2:
        from blueflower.modules.bzip2 import bzip2_do_data
        bzip2_do_data(data, afile)
    elif ftype == constants.BF_DOCX:
        from blueflower.modules.docx import docx_do_data
        docx_do_data(data, afile)
    elif ftype == constants.BF_GZ:
        from blueflower.modules.gz import gz_do_data
        gz_do_data(data, afile)
    elif ftype == constants.BF_PDF:
        from blueflower.modules.pdf import pdf_do_data
        pdf_do_data(data, afile)
    elif ftype == constants.BF_TAR:
        from blueflower.modules.tar import tar_do_data
        tar_do_data(data, afile)
    elif ftype == constants.BF_TEXT:
        from blueflower.modules.text import text_do_data
        text_do_data(data, afile)
    elif ftype == constants.BF_XLSX:
        from blueflower.modules.xlsx import xlsx_do_data
        xlsx_do_data(data, afile)
    elif ftype == constants.BF_ZIP:
        from blueflower.modules.zip import zip_do_data
        zip_do_data(data, afile)


def do_file(ftype, afile):
    if ftype == constants.BF_UNKNOWN:
        return
    elif ftype == constants.BF_BZIP2:
        from blueflower.modules.bzip2 import bzip2_do_file
        bzip2_do_file(afile)
    elif ftype == constants.BF_GZ:
        from blueflower.modules.gz import gz_do_file
        gz_do_file(afile)
    elif ftype == constants.BF_DOCX:
        from blueflower.modules.docx import docx_do_file
        docx_do_file(afile)
    elif ftype == constants.BF_PDF:
        from blueflower.modules.pdf import pdf_do_file
        pdf_do_file(afile)
    elif ftype == constants.BF_TAR:
        from blueflower.modules.tar import tar_do_file
        tar_do_file(afile)
    elif ftype == constants.BF_TEXT:
        from blueflower.modules.text import text_do_file
        text_do_file(afile)
    elif ftype == constants.BF_XLSX:
        from blueflower.modules.xlsx import xlsx_do_file
        xlsx_do_file(afile)
    elif ftype == constants.BF_ZIP:
        from blueflower.modules.zip import zip_do_file
        zip_do_file(afile)
