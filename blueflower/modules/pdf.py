# pdf.py
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

import io

from blueflower.modules.text import text_do_data
from blueflower.utils import log_error

from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFSyntaxError
from cStringIO import StringIO


def pdf_do_pdf(astream, afile):
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    pagenos = set()
    try:
        for page in PDFPage.get_pages(astream, pagenos, maxpages=0, password='', \
                                  caching=True, check_extractable=True):
            interpreter.process_page(page)
    except PDFSyntaxError:
        log_error('pdfparser.PDFSyntaxError', afile)
    device.close()
    text = retstr.getvalue()
    retstr.close()
    text_do_data(text, afile)


def pdf_do_data(data, afile):
    astream = io.BytesIO(data)
    pdf_do_pdf(astream, afile)


def pdf_do_file(afile):
    try:
        fid = open(afile)
    except IOError:
        log_error('IOError', afile)
    pdf_do_pdf(fid, afile)
    fid.close()
