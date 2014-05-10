PROGRAM=blueflower
RM=rm -rf

install:
	    python setup.py install

clean:  
	    $(RM) $(PROGRAM)-* $(PROGRAM)/*.pyc \
                               $(PROGRAM)/modules/*.pyc \
			       $(PROGRAM)/utils/*.pyc

cleanall:   clean
	    $(RM) build/ dist/ $(PROGRAM).egg-info/ 

dist:       cleanall
	    cd ..; \
	    tar zcf $(PROGRAM)-`date +%Y%m%d%H%M`.tar.gz $(PROGRAM) 
