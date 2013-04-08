#!/usr/bin/python

import sys
try:
    from gi.repository import Gtk
except:
    print "Could not GTK3 libraries"
    sys.exit(1)
    
class NoteBook:
    def __init__(self):
        self.noteBook = Gtk.Notebook()
        pageStrs = ["Timer", "Exercise"]
        for index in range(len(pageStrs)):
            tabLabel = Gtk.Label(pageStrs[index])
            tabGrid = Gtk.Grid()
            containerLabel = Gtk.Label(pageStrs[index]+" is inside tab")
            containerLabel.show()
            tabGrid.add(containerLabel)
            self.noteBook.append_page(tabGrid, tabLabel)
        
    def getNoteBook(self):
        return self.noteBook
#end class NoteBook

class Builder:
    def __init__(self):
        self.window = Gtk.Window()
        self.window.set_default_size(200, 200)
        self.window.set_title("Break My Work")
        self.nb = NoteBook()
        self.window.add(self.nb.getNoteBook())
        self.window.connect("delete-event", Gtk.main_quit)
        self.window.show_all()
        
    def getWindow(self):
        return self.window
        
    def main(self):
        Gtk.main()
#end class Builder

if __name__ == "__main__":
    b = Builder()
    b.main()