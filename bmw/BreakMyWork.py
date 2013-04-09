#!/usr/bin/python

import sys
try:
    from gi.repository import Gtk, Pango
except:
    print "Could not GTK3 libraries"
    sys.exit(1)
    
class UI:
    def __init__(self):
        self.noteBook = Gtk.Notebook()
        pageStrs = ["Timer", "Exercise"]
        for index in range(len(pageStrs)):
            tabLabel = Gtk.Label(pageStrs[index])
            tabGrid = Gtk.Grid()
            #Add radio button to the grid
            if(pageStrs[index] == "Timer"):
                self.buildTimerTabUI(tabGrid)
            else:
                self.addLabelToGrid(tabGrid, pageStrs[index])
                
            self.noteBook.append_page(tabGrid, tabLabel)
        
    def buildTimerTabUI(self, tabGrid):
        #short break label
        self.shortBreakLabel = Gtk.Label('Short Breaks')
        self.shortBreakLabel.modify_font(self.getFont("heading"))
        self.shortBreakLabel.set_alignment(0, 0.5)
        self.setMargin(self.shortBreakLabel, "10 10 10 10");
        tabGrid.add(self.shortBreakLabel)
        
        #short break 15 mins
        self.shortFifteenStr = "Once every 15 mins"
        self.shortFifteenBtn = Gtk.RadioButton.new_with_label_from_widget(None, self.shortFifteenStr);
        self.shortFifteenBtn.connect("toggled", self.on_button_toggled, "short15");
        tabGrid.attach_next_to(self.shortFifteenBtn, self.shortBreakLabel, Gtk.PositionType.BOTTOM, 1, 1);
        
        #short break 30 mins
        self.shortThirtyStr = "Once every 30 mins"
        self.shortThirtyBtn = Gtk.RadioButton.new_with_label_from_widget(self.shortFifteenBtn, self.shortThirtyStr);
        self.shortThirtyBtn.connect("toggled", self.on_button_toggled, "short30");
        tabGrid.attach_next_to(self.shortThirtyBtn, self.shortFifteenBtn, Gtk.PositionType.BOTTOM, 1, 1);
        
        #short break custom mins radio button
        self.shortCustomBtn = Gtk.RadioButton.new_with_label_from_widget(self.shortFifteenBtn, "Custom");
        self.shortCustomBtn.connect("toggled", self.on_button_toggled, "shortCustom");
        shortCustomHBox = Gtk.Box()
        shortCustomHBox.pack_start(self.shortCustomBtn, True, True, 0)
        
        #value, lower, upper, step_inc, page_inc, page_size
        self.shortBreakAdjustment = Gtk.Adjustment(60, 1, 999, 1, 10, 0)
        #short break custom mins spinner button
        self.shortBreakSpinBtn = Gtk.SpinButton()
        self.shortBreakSpinBtn.set_adjustment(self.shortBreakAdjustment)
        self.shortBreakSpinBtn.set_numeric(True)
        self.shortBreakSpinBtn.set_digits(0)
        self.shortBreakSpinBtn.set_update_policy(Gtk.SpinButtonUpdatePolicy.IF_VALID)
        self.shortBreakSpinBtn.set_margin_left(5)
        self.shortBreakSpinBtn.set_sensitive(False)
        self.shortBreakSpinBtn.set_wrap(True)
        self.shortBreakAdjustment.connect("value_changed", self.updateCustomShortBreak)
        shortCustomHBox.pack_start(self.shortBreakSpinBtn, True, True, 0)
        
        #short break custom mins label
        shortCustomLabel = Gtk.Label("minutes")
        shortCustomLabel.set_margin_left(5)
        shortCustomHBox.pack_start(shortCustomLabel, True, True, 0)
        
        #Add HBox to the grid
        tabGrid.attach_next_to(shortCustomHBox, self.shortThirtyBtn, Gtk.PositionType.BOTTOM, 1, 1);
        
    def getFont(self, type):
        if(type == "heading"):
            return Pango.FontDescription("14")
        
        #default (normal)
        return Pango.FontDescription("12")
        
    def setMargin(self, widget, margin):
        marginArr = margin.split(" ")
        widget.set_margin_top(int(marginArr[0]))
        widget.set_margin_right(int(marginArr[1]))
        widget.set_margin_bottom(int(marginArr[2]))
        widget.set_margin_left(int(marginArr[3]))
        
    def getButtonLabel(self, btn):
        if btn.get_use_stock():
            return btn.child.get_children()[1]
        elif isinstance(btn.child, Gtk.Label):
            return btn.child
        else:
            raise ValueError("button does not have a label")
            
    def shortBreakCustomEntryChanged(self, btn, name):
        if(name == "custom"):
            self.updateShortTimer(name)
            
    def updateShortTimer(self, name):
        if(name == "custom"):
            currVal = self.shortBreakSpinBtn.get_value_as_int()
            print "Activate Timer Once every ", currVal, " mins (custom)"
        elif(name == "short15"):
            print "Activate Timer Once every 15 mins"
        elif(name == "short30"):
            print "Activate Timer Once every 30 mins"
            
            
    def addLabelToGrid(self, tabGrid, labelName):
        containerLabel = Gtk.Label(labelName+" is inside tab")
        containerLabel.show()
        tabGrid.add(containerLabel)
        
    def on_button_toggled(self, btn, name):
        state = 0
        if(btn.get_active()):
            state = 1
        if(name == "short15"):
            if(state == 1):
                self.updateShortTimer("short15")
        elif(name == "short30"):
            if(state == 1):
                self.updateShortTimer("short30")
        elif(name == "shortCustom"):
            if(state == 1):
                self.shortBreakSpinBtn.set_sensitive(True)
                self.updateShortTimer("custom")
            else:
                self.shortBreakSpinBtn.set_sensitive(False)
        
    def updateCustomShortBreak(self, btn):
        self.updateShortTimer("custom")
            
    def numbify(self, widget):
        def filter_numbers(entry, *args):
            text = entry.get_text().strip()
            entry.set_text(''.join([i for i in text if i in '0123456789']))

        widget.connect('changed', filter_numbers)
        
    def getNoteBook(self):
        return self.noteBook
#end class UI

class Builder:
    def __init__(self):
        self.window = Gtk.Window()
        self.window.set_default_size(200, 200)
        self.window.set_title("Break My Work")
        self.ui = UI()
        self.window.add(self.ui.getNoteBook())
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