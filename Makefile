BASEDIR = $(DESTDIR)/usr/share/breakmywork
IMGDIR = $(DESTDIR)/usr/share/breakmywork/images
BINDIR = $(DESTDIR)/usr/bin

clean:
		rm -f *.py[co]
install:
		mkdir -p $(BASEDIR)
		mkdir -p $(IMGDIR)
		cp breakmywork.py $(BASEDIR)
		cp images/breakicon.png $(IMGDIR)
		ln -s $(BASEDIR)/breakmywork.py $(BINDIR)
uninstall:
		rm -rf $(BASEDIR)
