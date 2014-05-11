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
