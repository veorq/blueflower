# xlsx.py
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


from xlrd import open_workbook, XLRDError

from blueflower.modules.text import text_do_data
from blueflower.utils.log import log_error


def xlsx_do_xlsx(axl, afile):
    rows = []
    for i in xrange(axl.nsheets):
        sheet = axl.sheet_by_index(i)
        for j in xrange(sheet.nrows):
            rows.append(' '.join(sheet.row_values(j)))
 
    text = '\n\n'.join(rows)
    text_do_data(text, afile)


def xlsx_do_data(data, afile):
    try:
        axl = open_workbook(file_contents=data)
    except XLRDError:
        log_error('XLRDError', afile)
        return
    xlsx_do_xlsx(axl, afile)


def xlsx_do_file(afile):
    try:
        axl = open_workbook(afile)
    except XLRDError:
        log_error('XLRDError', afile)
        return
    xlsx_do_xlsx(axl, afile)
