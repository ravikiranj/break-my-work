#!/usr/bin/env python
#
from gi.repository import AppIndicator3 as appindicator, Gtk
import os

def show_about_dialog(widget):
    about_dialog = Gtk.AboutDialog()

    about_dialog.set_destroy_with_parent(True)
    about_dialog.set_name("Break My Work")
    about_dialog.set_version("1.0")
    about_dialog.set_authors(["Ravikiran Janardhana"])

    about_dialog.run()
    about_dialog.destroy()
    
def menuitem_response(w, buf):
    print buf

if __name__ == "__main__":
    ind = appindicator.Indicator.new("MyApp", "utilities-terminal", appindicator.IndicatorCategory.APPLICATION_STATUS)
    ind.set_status (appindicator.IndicatorStatus.ACTIVE)
    currDir = os.getcwd()
    ind.set_icon_theme_path(currDir);
    ind.set_icon("theicon")
    
    # create a menu
    menu = Gtk.Menu()
    
    aboutItem = Gtk.MenuItem()
    aboutItem.set_label("About")
    quitItem = Gtk.MenuItem()
    quitItem.set_label("Quit")

    aboutItem.connect("activate", show_about_dialog)
    quitItem.connect("activate", Gtk.main_quit)

    menu.append(aboutItem)
    menu.append(quitItem)
    menu.show_all()

    ind.set_menu(menu)
    
    Gtk.main()