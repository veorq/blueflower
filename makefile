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


PROGRAM=blueflower
RM=rm -rf
UNINSTALL="sorry, since setuptools does not want you to uninstall modules, you have to manually remove (for example)\n/usr/local/bin/blueflower and\n/usr/local/lib/python2.7/dist-packages/blueflower-*.egg \n(these may be located elsewhere on your system)" 


install:
	    python setup.py install

uninstall:  
	    @echo $(UNINSTALL)

clean:  
	    $(RM) $(PROGRAM)-* $(PROGRAM)/*.pyc \
                               $(PROGRAM)/modules/*.pyc \
			       $(PROGRAM)/utils/*.pyc

cleanall:   clean
	    $(RM) build/ dist/ $(PROGRAM).egg-info/ 

dist:       cleanall
	    cd ..; \
	    tar zcf $(PROGRAM)-`date +%Y%m%d%H%M`.tar.gz $(PROGRAM) 
