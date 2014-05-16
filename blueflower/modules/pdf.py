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


import io

from blueflower.modules.text import text_do_data
from blueflower.utils.log import log_error

from PyPDF2 import PdfFileReader


def pdf_do_pdf(astream, afile):
    """astream: stream, afile: source file name"""
    text = ''
    try:
        pdf = PdfFileReader(astream)
        for i in range(0, pdf.getNumPages()):
            text += pdf.getPage(i).extractText() + "/n"
    except Exception as e:  # pyPdf raises Exception..
        log_error(str(e), afile)
        return
    text_do_data(text, afile)


def pdf_do_data(data, afile):
    astream = io.BytesIO(data)
    pdf_do_pdf(astream, afile)


def pdf_do_file(afile):
    try:
        fid = open(afile, 'rb')
    except IOError as e:
        log_error(str(e), afile)
    pdf_do_pdf(fid, afile)
    fid.close()
