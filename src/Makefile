BASEDIR = $(DESTDIR)/usr/share/breakmywork
IMGDIR = $(DESTDIR)/usr/share/breakmywork/images
BINDIR = $(DESTDIR)/usr/bin

clean:
		rm -f *.py[co]
install:
		mkdir -p $(BASEDIR)
		mkdir -p $(IMGDIR)
		cp breakmywork.py $(BASEDIR)
		chmod 755 $(BASEDIR)/breakmywork.py
		cp images/breakicon.png $(IMGDIR)
		cp images/deskStretches.jpg $(IMGDIR)
uninstall:
		rm -rf $(BASEDIR)
		rm $(BINDIR)/breakmywork
