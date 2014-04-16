# do.py
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


def do_data(ftype, data, afile):
    if ftype == 'tar': 
        from blueflower.modules.tar import tar_do_data
        tar_do_data(data, afile)
    elif ftype == 'text': 
        from blueflower.modules.text import text_do_data
        text_do_data(data, afile)
    elif ftype == 'zip': 
        from blueflower.modules.zip import zip_do_data
        zip_do_data(data, afile)


def do_file(ftype, afile):
    if ftype == 'tar': 
        from blueflower.modules.tar import tar_do_file
        tar_do_file(afile)
    elif ftype == 'text': 
        from blueflower.modules.text import text_do_file
        text_do_file(afile)
    elif ftype == 'zip': 
        from blueflower.modules.zip import zip_do_file
        zip_do_file(afile)

