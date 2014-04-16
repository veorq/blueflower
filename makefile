PROGRAM=blueflower
RM=rm -rf

install:
	    sudo python setup.py install

clean:  
	    $(RM) $(PROGRAM)-* $(PROGRAM)/*.pyc $(PROGRAM)/modules/*.pyc

cleanall:   clean
	    sudo $(RM) build/ dist/ $(PROGRAM).egg-info/ 

dist:       cleanall
	    cd ..; \
	    tar zcf $(PROGRAM)-`date +%Y%m%d%H%M`.tar.gz $(PROGRAM) 
