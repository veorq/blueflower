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

from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage, PDFTextExtractionNotAllowed


def pdf_do_pdf(astream, afile):
    outstream = io.BytesIO()
    laparams = LAParams()
    rsrcmgr = PDFResourceManager(caching=True)
    device = TextConverter(rsrcmgr, outstream, codec='utf-8', laparams=laparams,
                               imagewriter=None)
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    try:
        for page in PDFPage.get_pages(astream, set(),
                                      maxpages=0, password='',
                                      caching=True, check_extractable=True):
            interpreter.process_page(page)
    except PDFTextExtractionNotAllowed as e:
        log_error(str(e), afile)
        return
    text = outstream.getvalue()
    text_do_data(text, afile)
    outstream.close()


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
