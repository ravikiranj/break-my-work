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
        #Set tab grid border width
        tabGrid.set_border_width(15)
        
        #Short Break Settings Grid
        self.shortBreakSettingsFrame = Gtk.Frame()
        self.shortBreakSettingsFrame.set_border_width(5)
        self.setMargin(self.shortBreakSettingsFrame, "10 0 10 10")
        self.shortBreakSettingsGrid = Gtk.Grid()
        self.shortBreakSettingsGrid.set_border_width(10)
        self.shortBreakSettingsFrame.add(self.shortBreakSettingsGrid)
        
        #Short Break Action Grid
        self.shortBreakActionFrame = Gtk.Frame()
        self.shortBreakActionFrame.set_border_width(5)
        self.setMargin(self.shortBreakActionFrame, "10 15 10 20")
        self.shortBreakActionGrid = Gtk.Grid()
        self.shortBreakActionGrid.set_border_width(10)
        self.shortBreakActionFrame.add(self.shortBreakActionGrid)
        
        #Long Break Settings Grid
        self.longBreakSettingsFrame = Gtk.Frame()
        self.longBreakSettingsFrame.set_border_width(5)
        self.setMargin(self.longBreakSettingsFrame, "20 0 10 10")
        self.longBreakSettingsGrid = Gtk.Grid()
        self.longBreakSettingsGrid.set_border_width(10)
        self.longBreakSettingsFrame.add(self.longBreakSettingsGrid)
        
        #Long Break Action Grid
        self.longBreakActionFrame = Gtk.Frame()
        self.longBreakActionFrame.set_border_width(5)
        self.setMargin(self.longBreakActionFrame, "20 15 10 20")
        self.longBreakActionGrid = Gtk.Grid()
        self.longBreakActionGrid.set_border_width(10)
        self.longBreakActionFrame.add(self.longBreakActionGrid)
        
        #add them to tabGrid
        tabGrid.add(self.shortBreakSettingsFrame)
        tabGrid.attach_next_to(self.shortBreakActionFrame, self.shortBreakSettingsFrame, Gtk.PositionType.RIGHT, 1, 1)
        tabGrid.attach_next_to(self.longBreakSettingsFrame, self.shortBreakSettingsFrame, Gtk.PositionType.BOTTOM, 1, 1)
        tabGrid.attach_next_to(self.longBreakActionFrame, self.longBreakSettingsFrame, Gtk.PositionType.RIGHT, 1, 1)
        
        #build short and long break settings UI
        self.buildShortBreakSettingsUI(self.shortBreakSettingsGrid)
        self.buildLongBreakSettingsUI(self.longBreakSettingsGrid)
        self.buildShortBreakActionUI(self.shortBreakActionGrid)
        self.buildLongBreakActionUI(self.longBreakActionGrid)

    def buildShortBreakSettingsUI(self, tabGrid):
        #short break label
        self.shortBreakLabel = Gtk.Label('Short Breaks')
        self.shortBreakLabel.modify_font(self.getFont("heading"))
        self.shortBreakLabel.set_alignment(0, 0.5)
        self.setMargin(self.shortBreakLabel, "10 10 10 10");
        tabGrid.add(self.shortBreakLabel)
        
        #short break enable/disable CheckBox
        self.shortBreakEnableBtn = Gtk.CheckButton("Enable Short Breaks")
        self.shortBreakEnableBtn.set_active(True)
        self.shortBreakEnableBtn.connect("toggled", self.toggleShortBreaks)
        self.shortBreakEnableBtn.set_margin_left(10)
        tabGrid.attach_next_to(self.shortBreakEnableBtn, self.shortBreakLabel, Gtk.PositionType.BOTTOM, 1, 1);
        
        #short break vBox to hold timer choices
        self.shortTimerChoiceBox = Gtk.Box()
        self.shortTimerChoiceBox.set_orientation(Gtk.Orientation.VERTICAL)
        self.setMargin(self.shortTimerChoiceBox, "10 0 10 30")
        tabGrid.attach_next_to(self.shortTimerChoiceBox, self.shortBreakEnableBtn, Gtk.PositionType.BOTTOM, 1, 1)
        
        #short break duration hbox
        self.shortBreakDurationBox = Gtk.Box()
        self.shortBreakDurationBox.set_orientation(Gtk.Orientation.HORIZONTAL)
        self.setMargin(self.shortBreakDurationBox, "0 0 5 0")
        self.shortTimerChoiceBox.pack_start(self.shortBreakDurationBox, True, True, 0)
        
        #short break Duration label        
        shortBreakDurationLabel = Gtk.Label("Duration")
        self.shortBreakDurationBox.pack_start(shortBreakDurationLabel, True, True, 0)
        
        #value, lower, upper, step_inc, page_inc, page_size
        self.shortBreakDurationAdjustment = Gtk.Adjustment(2, 1, 10, 1, 2, 0)
        #short break custom mins spinner button
        self.shortBreakDurationBtn = Gtk.SpinButton()
        self.shortBreakDurationBtn.set_adjustment(self.shortBreakDurationAdjustment)
        self.shortBreakDurationBtn.set_numeric(True)
        self.shortBreakDurationBtn.set_digits(0)
        self.shortBreakDurationBtn.set_update_policy(Gtk.SpinButtonUpdatePolicy.IF_VALID)
        self.shortBreakDurationBtn.set_sensitive(True)
        self.shortBreakDurationBtn.set_max_length(2)
        self.shortBreakDurationBtn.set_margin_left(5)
        self.shortBreakDurationAdjustment.connect("value_changed", self.updateShortBreakDuration)
        self.shortBreakDurationBox.pack_start(self.shortBreakDurationBtn, True, True, 0)
        
        #short break Duration 'minutes' label        
        shortBreakDurationMinsLabel = Gtk.Label("minutes")
        shortBreakDurationMinsLabel.set_margin_left(2)
        self.shortBreakDurationBox.pack_start(shortBreakDurationMinsLabel, True, True, 0)
        
        #short break 15 mins
        self.shortFifteenStr = "Once every 15 mins"
        self.shortFifteenBtn = Gtk.RadioButton.new_with_label_from_widget(None, self.shortFifteenStr);
        self.shortFifteenBtn.set_margin_top(5)
        self.shortFifteenBtn.connect("toggled", self.changeShortBreakTimer, "short15");
        self.shortTimerChoiceBox.pack_start(self.shortFifteenBtn, True, True, 0)
        
        #short break 30 mins
        self.shortThirtyStr = "Once every 30 mins"
        self.shortThirtyBtn = Gtk.RadioButton.new_with_label_from_widget(self.shortFifteenBtn, self.shortThirtyStr);
        self.shortThirtyBtn.set_margin_top(5)
        self.shortThirtyBtn.connect("toggled", self.changeShortBreakTimer, "short30");
        self.shortTimerChoiceBox.pack_start(self.shortThirtyBtn, True, True, 0)
        
        #short break custom mins radio button
        self.shortCustomBtn = Gtk.RadioButton.new_with_label_from_widget(self.shortFifteenBtn, "Custom");
        self.shortCustomBtn.set_margin_top(5)
        self.shortCustomBtn.connect("toggled", self.changeShortBreakTimer, "shortCustom");
        
        #short break HBOX to hold custom mins data
        self.shortCustomHBox = Gtk.Box()
        self.shortCustomHBox.set_orientation(Gtk.Orientation.HORIZONTAL)
        self.shortTimerChoiceBox.pack_start(self.shortCustomHBox, True, True, 0)
        self.shortCustomHBox.pack_start(self.shortCustomBtn, True, True, 0)
        
        #value, lower, upper, step_inc, page_inc, page_size
        self.shortBreakCustomMinsAdjustment = Gtk.Adjustment(60, 1, 999, 1, 10, 0)
        #short break custom mins spinner button
        self.shortBreakCustomMinsBtn = Gtk.SpinButton()
        self.shortBreakCustomMinsBtn.set_adjustment(self.shortBreakCustomMinsAdjustment)
        self.shortBreakCustomMinsBtn.set_numeric(True)
        self.shortBreakCustomMinsBtn.set_digits(0)
        self.shortBreakCustomMinsBtn.set_update_policy(Gtk.SpinButtonUpdatePolicy.IF_VALID)
        self.shortBreakCustomMinsBtn.set_margin_left(5)
        self.shortBreakCustomMinsBtn.set_max_length(3)
        self.shortBreakCustomMinsBtn.set_sensitive(False)
        self.shortBreakCustomMinsBtn.set_wrap(True)
        self.shortBreakCustomMinsAdjustment.connect("value_changed", self.updateCustomShortBreak)
        self.shortCustomHBox.pack_start(self.shortBreakCustomMinsBtn, True, True, 0)
        
        #short break custom mins label
        shortCustomLabel = Gtk.Label("minutes")
        shortCustomLabel.set_margin_left(5)
        self.shortCustomHBox.pack_start(shortCustomLabel, True, True, 0)
        
    def buildShortBreakActionUI(self, tabGrid):
        #short break action label
        self.shortBreakActionLabel = Gtk.Label('Short Breaks Action')
        self.shortBreakActionLabel.modify_font(self.getFont("heading"))
        self.shortBreakActionLabel.set_alignment(0, 0.5)
        self.setMargin(self.shortBreakActionLabel, "10 10 10 10");
        tabGrid.add(self.shortBreakActionLabel)
        
        #short break action vBox to hold choices
        self.shortActionChoiceBox = Gtk.Box()
        self.shortActionChoiceBox.set_orientation(Gtk.Orientation.VERTICAL)
        self.setMargin(self.shortActionChoiceBox, "10 0 10 10")
        tabGrid.attach_next_to(self.shortActionChoiceBox, self.shortBreakActionLabel, Gtk.PositionType.BOTTOM, 1, 1)
        
        #short break action - tooltip reminder
        self.shortBreakActionToolTipStr = "Show Tool Tip Reminder (gentle)"
        self.shortBreakActionToolTipBtn = Gtk.RadioButton.new_with_label_from_widget(None, self.shortBreakActionToolTipStr);
        self.shortBreakActionToolTipBtn.connect("toggled", self.updateShortBreakAction, "shortBreakToolTip")
        self.shortBreakActionToolTipBtn.set_margin_top(5)
        self.shortActionChoiceBox.pack_start(self.shortBreakActionToolTipBtn, True, True, 0)
        
        #short break action - pop up reminder
        self.shortBreakActionPopUpStr = "Show Pop Up Reminder (invasive)"
        self.shortBreakActionPopUpBtn = Gtk.RadioButton.new_with_label_from_widget(self.shortBreakActionToolTipBtn, self.shortBreakActionPopUpStr);
        self.shortBreakActionPopUpBtn.connect("toggled", self.updateShortBreakAction, "shortBreakPopUp")
        self.shortBreakActionPopUpBtn.set_margin_top(5)
        self.shortActionChoiceBox.pack_start(self.shortBreakActionPopUpBtn, True, True, 0)
        
        #short break action - lock keyboard and mouse
        self.shortBreakActionDisableInpStr = "Disable Keyboard and Mouse (forces a break)"
        self.shortBreakActionDisableInpBtn = Gtk.RadioButton.new_with_label_from_widget(self.shortBreakActionToolTipBtn, self.shortBreakActionDisableInpStr);
        self.shortBreakActionDisableInpBtn.connect("toggled", self.updateShortBreakAction, "shortBreakDisableInp")
        self.shortBreakActionDisableInpBtn.set_margin_top(5)
        self.shortActionChoiceBox.pack_start(self.shortBreakActionDisableInpBtn, True, True, 0)
        
    def buildLongBreakSettingsUI(self, tabGrid):
        #long break label
        self.longBreakLabel = Gtk.Label('Long Breaks')
        self.longBreakLabel.modify_font(self.getFont("heading"))
        self.longBreakLabel.set_alignment(0, 0.5)
        self.setMargin(self.longBreakLabel, "10 10 10 10");
        tabGrid.add(self.longBreakLabel)
        
        #long break enable/disable CheckBox
        self.longBreakEnableBtn = Gtk.CheckButton("Enable Long Breaks")
        self.longBreakEnableBtn.set_active(True)
        self.longBreakEnableBtn.connect("toggled", self.toggleLongBreaks)
        self.longBreakEnableBtn.set_margin_left(10)
        tabGrid.attach_next_to(self.longBreakEnableBtn, self.longBreakLabel, Gtk.PositionType.BOTTOM, 1, 1);
        
        #long break vBox to hold timer choices
        self.longTimerChoiceBox = Gtk.Box()
        self.longTimerChoiceBox.set_orientation(Gtk.Orientation.VERTICAL)
        self.setMargin(self.longTimerChoiceBox, "10 0 10 30")
        tabGrid.attach_next_to(self.longTimerChoiceBox, self.longBreakEnableBtn, Gtk.PositionType.BOTTOM, 1, 1)
        
        #long break duration hbox
        self.longBreakDurationBox = Gtk.Box()
        self.longBreakDurationBox.set_orientation(Gtk.Orientation.HORIZONTAL)
        self.setMargin(self.longBreakDurationBox, "0 0 5 0")
        self.longTimerChoiceBox.pack_start(self.longBreakDurationBox, True, True, 0)
        
        #long break Duration label        
        longBreakDurationLabel = Gtk.Label("Duration")
        self.longBreakDurationBox.pack_start(longBreakDurationLabel, True, True, 0)
        
        #value, lower, upper, step_inc, page_inc, page_size
        self.longBreakDurationAdjustment = Gtk.Adjustment(5, 1, 20, 1, 2, 0)
        #long break custom mins spinner button
        self.longBreakDurationBtn = Gtk.SpinButton()
        self.longBreakDurationBtn.set_adjustment(self.longBreakDurationAdjustment)
        self.longBreakDurationBtn.set_numeric(True)
        self.longBreakDurationBtn.set_digits(0)
        self.longBreakDurationBtn.set_update_policy(Gtk.SpinButtonUpdatePolicy.IF_VALID)
        self.longBreakDurationBtn.set_sensitive(True)
        self.longBreakDurationBtn.set_max_length(2)
        self.longBreakDurationBtn.set_margin_left(5)
        self.longBreakDurationAdjustment.connect("value_changed", self.updateLongBreakDuration)
        self.longBreakDurationBox.pack_start(self.longBreakDurationBtn, True, True, 0)
        
        #long break Duration 'minutes' label        
        longBreakDurationMinsLabel = Gtk.Label("minutes")
        longBreakDurationMinsLabel.set_margin_left(2)
        self.longBreakDurationBox.pack_start(longBreakDurationMinsLabel, True, True, 0)
        
        #long break 1 hour
        self.longOneHourStr = "Once every 1 hour"
        self.longOneHourBtn = Gtk.RadioButton.new_with_label_from_widget(None, self.longOneHourStr);
        self.longOneHourBtn.set_margin_top(5)
        self.longOneHourBtn.connect("toggled", self.changeLongBreakTimer, "long1hr");
        self.longTimerChoiceBox.pack_start(self.longOneHourBtn, True, True, 0)
        
        #long break 2 hours
        self.longTwoHourStr = "Once every 2 hours"
        self.longTwoHourBtn = Gtk.RadioButton.new_with_label_from_widget(self.longOneHourBtn, self.longTwoHourStr);
        self.longTwoHourBtn.set_margin_top(5)
        self.longTwoHourBtn.connect("toggled", self.changeLongBreakTimer, "long2hr");
        self.longTimerChoiceBox.pack_start(self.longTwoHourBtn, True, True, 0)
        
        #long break custom mins radio button
        self.longCustomBtn = Gtk.RadioButton.new_with_label_from_widget(self.longOneHourBtn, "Custom");
        self.longCustomBtn.set_margin_top(5)
        self.longCustomBtn.connect("toggled", self.changeLongBreakTimer, "longCustom");
        
        #long break HBOX to hold custom mins data
        self.longCustomHBox = Gtk.Box()
        self.longCustomHBox.set_orientation(Gtk.Orientation.HORIZONTAL)
        self.longTimerChoiceBox.pack_start(self.longCustomHBox, True, True, 0)
        self.longCustomHBox.pack_start(self.longCustomBtn, True, True, 0)
        
        #value, lower, upper, step_inc, page_inc, page_size
        self.longBreakCustomMinsAdjustment = Gtk.Adjustment(1, 1, 12, 1, 2, 0)
        #long break custom mins spinner button
        self.longBreakCustomMinsBtn = Gtk.SpinButton()
        self.longBreakCustomMinsBtn.set_adjustment(self.longBreakCustomMinsAdjustment)
        self.longBreakCustomMinsBtn.set_numeric(True)
        self.longBreakCustomMinsBtn.set_digits(0)
        self.longBreakCustomMinsBtn.set_update_policy(Gtk.SpinButtonUpdatePolicy.IF_VALID)
        self.longBreakCustomMinsBtn.set_margin_left(5)
        self.longBreakCustomMinsBtn.set_max_length(2)
        self.longBreakCustomMinsBtn.set_sensitive(False)
        self.longBreakCustomMinsBtn.set_wrap(True)
        self.longBreakCustomMinsAdjustment.connect("value_changed", self.updateCustomLongBreak)
        self.longCustomHBox.pack_start(self.longBreakCustomMinsBtn, True, True, 0)
        
        #long break custom hours label
        longCustomLabel = Gtk.Label("hour(s)")
        longCustomLabel.set_margin_left(5)
        self.longCustomHBox.pack_start(longCustomLabel, True, True, 0)
        
    def buildLongBreakActionUI(self, tabGrid):
        #long break action label
        self.longBreakActionLabel = Gtk.Label('Long Breaks Action')
        self.longBreakActionLabel.modify_font(self.getFont("heading"))
        self.longBreakActionLabel.set_alignment(0, 0.5)
        self.setMargin(self.longBreakActionLabel, "10 10 10 10");
        tabGrid.add(self.longBreakActionLabel)
        
        #long break action vBox to hold choices
        self.longActionChoiceBox = Gtk.Box()
        self.longActionChoiceBox.set_orientation(Gtk.Orientation.VERTICAL)
        self.setMargin(self.longActionChoiceBox, "10 0 10 10")
        tabGrid.attach_next_to(self.longActionChoiceBox, self.longBreakActionLabel, Gtk.PositionType.BOTTOM, 1, 1)
        
        #long break action - tooltip reminder
        self.longBreakActionToolTipStr = "Show Tool Tip Reminder (gentle)"
        self.longBreakActionToolTipBtn = Gtk.RadioButton.new_with_label_from_widget(None, self.longBreakActionToolTipStr);
        self.longBreakActionToolTipBtn.connect("toggled", self.updateLongBreakAction, "longBreakToolTip")
        self.longBreakActionToolTipBtn.set_margin_top(5)
        self.longActionChoiceBox.pack_start(self.longBreakActionToolTipBtn, True, True, 0)
        
        #long break action - pop up reminder
        self.longBreakActionPopUpStr = "Show Pop Up Reminder (invasive)"
        self.longBreakActionPopUpBtn = Gtk.RadioButton.new_with_label_from_widget(self.longBreakActionToolTipBtn, self.longBreakActionPopUpStr);
        self.longBreakActionPopUpBtn.connect("toggled", self.updateLongBreakAction, "longBreakPopUp")
        self.longBreakActionPopUpBtn.set_margin_top(5)
        self.longActionChoiceBox.pack_start(self.longBreakActionPopUpBtn, True, True, 0)
        
        #long break action - lock keyboard and mouse
        self.longBreakActionDisableInpStr = "Disable Keyboard and Mouse (forces a break)"
        self.longBreakActionDisableInpBtn = Gtk.RadioButton.new_with_label_from_widget(self.longBreakActionToolTipBtn, self.longBreakActionDisableInpStr);
        self.longBreakActionDisableInpBtn.connect("toggled", self.updateLongBreakAction, "longBreakDisableInp")
        self.longBreakActionDisableInpBtn.set_margin_top(5)
        self.longActionChoiceBox.pack_start(self.longBreakActionDisableInpBtn, True, True, 0)
        
    def getFont(self, textType):
        if(textType == "heading"):
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
            
    def updateShortTimer(self, name):
        if(name == "custom"):
            currVal = self.shortBreakCustomMinsBtn.get_value_as_int()
            print "Activate Short Break Timer Once every ", currVal, " mins (custom)"
        elif(name == "short15"):
            print "Activate Short Break Timer Once every 15 mins"
        elif(name == "short30"):
            print "Activate Short Break Timer Once every 30 mins"
            
    def updateLongTimer(self, name):
        if(name == "custom"):
            currVal = self.longBreakCustomMinsBtn.get_value_as_int()
            print "Activate Long Break Once every ", currVal, " hour(s) (custom)"
        elif(name == "long1hr"):
            print "Activate Long Break Once Every 1 Hour"
        elif(name == "long2hr"):
            print "Activate Long Break Once Every 2 Hours"
            
    def toggleShortBreaks(self, btn):        
        if(btn.get_active()):
            #enable short breaks
            self.shortTimerChoiceBox.set_sensitive(True)
            self.shortActionChoiceBox.set_sensitive(True)
            print "Enable short breaks"
        else:
            #disable short breaks
            self.shortTimerChoiceBox.set_sensitive(False)
            self.shortActionChoiceBox.set_sensitive(False)
            print "Disable short breaks"
            
    def toggleLongBreaks(self, btn):        
        if(btn.get_active()):
            #enable long breaks
            self.longTimerChoiceBox.set_sensitive(True)
            self.longActionChoiceBox.set_sensitive(True)
            print "Enable long breaks"
        else:
            #disable long breaks
            self.longTimerChoiceBox.set_sensitive(False)
            self.longActionChoiceBox.set_sensitive(False)
            print "Disable long breaks"
            
    def addLabelToGrid(self, tabGrid, labelName):
        containerLabel = Gtk.Label(labelName+" is inside tab")
        containerLabel.show()
        tabGrid.add(containerLabel)
        
    def changeShortBreakTimer(self, btn, name):
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
                self.shortBreakCustomMinsBtn.set_sensitive(True)
                self.updateShortTimer("custom")
            else:
                self.shortBreakCustomMinsBtn.set_sensitive(False)
                
    def changeLongBreakTimer(self, btn, name):
        state = 0
        if(btn.get_active()):
            state = 1
        if(name == "long1hr"):
            if(state == 1):
                self.updateLongTimer("long1hr")
        elif(name == "long2hr"):
            if(state == 1):
                self.updateLongTimer("long2hr")
        elif(name == "longCustom"):
            if(state == 1):
                self.longBreakCustomMinsBtn.set_sensitive(True)
                self.updateLongTimer("custom")
            else:
                self.longBreakCustomMinsBtn.set_sensitive(False)
        
    def updateCustomShortBreak(self, btn):
        self.updateShortTimer("custom")
    
    def updateCustomLongBreak(self, btn):
        self.updateLongTimer("custom")
        
    def updateShortBreakDuration(self, btn):
        currVal = self.shortBreakDurationBtn.get_value_as_int()
        print "Short Break Duration =  ", currVal, " mins"
        
    def updateShortBreakAction(self, btn, name):
        state = 0
        if(btn.get_active()):
            state = 1
            
        if(name == "shortBreakToolTip"):
            if(state == 1):
                print "Short Break Action - Tool Tip Reminder"
        elif(name == "shortBreakPopUp"):
            if(state == 1):
                print "Short Break Action - Pop Up Reminder"
        elif(name == "shortBreakDisableInp"):
            if(state == 1):
                print "Short Break Action - Disable Input"
        
    def updateLongBreakAction(self, btn, name):
        state = 0
        if(btn.get_active()):
            state = 1
            
        if(name == "longBreakToolTip"):
            if(state == 1):
                print "Long Break Action - Tool Tip Reminder"
        elif(name == "longBreakPopUp"):
            if(state == 1):
                print "Long Break Action - Pop Up Reminder"
        elif(name == "longBreakDisableInp"):
            if(state == 1):
                print "Long Break Action - Disable Input"
                
    def updateLongBreakDuration(self, btn):
        currVal = self.longBreakDurationBtn.get_value_as_int()
        print "Long Break Duration =  ", currVal, " mins"
            
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
        self.window.set_default_size(400, 400)
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