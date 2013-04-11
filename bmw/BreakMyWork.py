#!/usr/bin/python

import sys
try:
    from gi.repository import Gtk, Pango
except:
    print "Could not GTK3 libraries"
    sys.exit(1)
    
class UI:
    def __init__(self, helper):
        self.noteBook = Gtk.Notebook()
        self.h = helper
        pageStrs = ["Timer", "Exercises"]
        for index in range(len(pageStrs)):
            tabLabel = Gtk.Label(pageStrs[index])
            tabGrid = Gtk.Grid()
            #Add radio button to the grid
            if(pageStrs[index] == "Timer"):
                self.buildTimerTabUI(tabGrid, helper)
            elif(pageStrs[index] == "Exercises"):
                self.buildExerciseTabUI(tabGrid)
                
            self.noteBook.append_page(tabGrid, tabLabel)
        
    def buildTimerTabUI(self, tabGrid, helper):
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
        self.setMargin(self.shortBreakActionFrame, "10 0 10 10")
        self.shortBreakActionGrid = Gtk.Grid()
        self.shortBreakActionGrid.set_border_width(10)
        self.shortBreakActionFrame.add(self.shortBreakActionGrid)
        
        #Save Changes Grid
        self.saveChangesGrid = Gtk.Grid()
        self.saveChangesGrid.set_border_width(10)
        
        #add them to tabGrid
        tabGrid.add(self.shortBreakSettingsFrame)
        tabGrid.attach_next_to(self.shortBreakActionFrame, self.shortBreakSettingsFrame, Gtk.PositionType.BOTTOM, 1, 1)
        tabGrid.attach_next_to(self.saveChangesGrid, self.shortBreakActionFrame, Gtk.PositionType.BOTTOM, 2, 1)
        
        #build short and long break settings UI
        self.buildShortBreakSettingsUI(self.shortBreakSettingsGrid)
        self.buildShortBreakActionUI(self.shortBreakActionGrid)
        self.buildSaveChangesUI(self.saveChangesGrid, helper)

    def buildShortBreakSettingsUI(self, tabGrid):
        #short break label
        self.shortBreakLabel = Gtk.Label('Break Intervals')
        self.shortBreakLabel.modify_font(self.getFont("heading"))
        self.shortBreakLabel.set_alignment(0, 0.5)
        self.setMargin(self.shortBreakLabel, "10 10 10 10");
        tabGrid.add(self.shortBreakLabel)
        
        #short break enable/disable CheckBox
        self.shortBreakEnableBtn = Gtk.CheckButton("Enable Breaks")
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
        
        #short break 60 mins
        self.shortSixtyStr = "Once every 60 mins"
        self.shortSixtyBtn = Gtk.RadioButton.new_with_label_from_widget(self.shortFifteenBtn, self.shortSixtyStr);
        self.shortSixtyBtn.set_margin_top(5)
        self.shortSixtyBtn.connect("toggled", self.changeShortBreakTimer, "short60");
        self.shortTimerChoiceBox.pack_start(self.shortSixtyBtn, True, True, 0)
        
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
        self.shortBreakActionLabel = Gtk.Label('Break Action')
        self.shortBreakActionLabel.modify_font(self.getFont("heading"))
        self.shortBreakActionLabel.set_alignment(0, 0.5)
        self.setMargin(self.shortBreakActionLabel, "10 10 10 10");
        tabGrid.add(self.shortBreakActionLabel)
        
        #short break action vBox to hold choices
        self.shortActionChoiceBox = Gtk.Box()
        self.shortActionChoiceBox.set_orientation(Gtk.Orientation.VERTICAL)
        self.setMargin(self.shortActionChoiceBox, "0 0 10 10")
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
        
    def buildSaveChangesUI(self, tabGrid, helper):
        #add ok, apply, cancel buttons
        self.saveChangesBox = Gtk.Box()
        self.saveChangesBox.set_orientation(Gtk.Orientation.HORIZONTAL)
        tabGrid.add(self.saveChangesBox)
        
        #OK Button
        self.timerOKBtn = Gtk.Button()
        self.timerOKBtn.set_label("Ok")
        self.timerOKBtn.set_size_request(90, 30)
        self.timerOKBtn.connect("clicked", self.saveChangesHandler, "Ok", helper)
        self.saveChangesBox.pack_start(self.timerOKBtn, True, True, 0)
        
        #Apply Button
        self.timerApplyBtn = Gtk.Button()
        self.timerApplyBtn.set_label("Apply")
        self.timerApplyBtn.set_size_request(90, 30)
        self.timerApplyBtn.set_margin_left(10)
        self.timerApplyBtn.set_sensitive(False)
        self.timerApplyBtn.connect("clicked", self.saveChangesHandler, "Apply", helper)
        self.saveChangesBox.pack_start(self.timerApplyBtn, True, True, 0)
        
        #Cancel Button
        self.timerCancelBtn = Gtk.Button()
        self.timerCancelBtn.set_label("Cancel")
        self.timerCancelBtn.set_size_request(90, 30)
        self.timerCancelBtn.set_margin_left(10)
        self.timerCancelBtn.set_sensitive(False)
        self.timerCancelBtn.connect("clicked", self.saveChangesHandler, "Cancel", helper)
        self.saveChangesBox.pack_start(self.timerCancelBtn, True, True, 0)
        
    def getFont(self, textType):
        if(textType == "heading"):
            return Pango.FontDescription("14")
        elif(textType == "disclaimer"):
            return Pango.FontDescription("#ff0000 12")
        
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
            self.enableApplyCancelBtns()
        elif(name == "short15"):
            print "Activate Short Break Timer Once every 15 mins"
            self.enableApplyCancelBtns()
        elif(name == "short30"):
            print "Activate Short Break Timer Once every 30 mins"
            self.enableApplyCancelBtns()
        elif(name == "short60"):
            print "Activate Short Break Timer Once every 60 mins"
            self.enableApplyCancelBtns()
            
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
        elif(name == "short60"):
            if(state == 1):
                self.updateShortTimer("short60")
        elif(name == "shortCustom"):
            if(state == 1):
                self.shortBreakCustomMinsBtn.set_sensitive(True)
                self.updateShortTimer("custom")
            else:
                self.shortBreakCustomMinsBtn.set_sensitive(False)
                
    def updateCustomShortBreak(self, btn):
        self.updateShortTimer("custom")
    
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
                self.enableApplyCancelBtns()
        elif(name == "shortBreakPopUp"):
            if(state == 1):
                print "Short Break Action - Pop Up Reminder"
                self.enableApplyCancelBtns()
        elif(name == "shortBreakDisableInp"):
            if(state == 1):
                print "Short Break Action - Disable Input"
                self.enableApplyCancelBtns()
        
    def buildExerciseTabUI(self, tabGrid):
        #Set tab grid border width
        tabGrid.set_border_width(15)
        
        #Scrolled Window
        self.exerScrollWindow = Gtk.ScrolledWindow()
        self.exerScrollWindow.set_size_request(620, 470)
        self.exerScrollWindow.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        tabGrid.add(self.exerScrollWindow)
        
        #Image
        self.exerImage = Gtk.Image()
        self.exerImagePath = "deskStretches.jpg"
        self.exerImage.set_from_file(self.exerImagePath)
        self.exerImageBtn = Gtk.Button()
        self.exerImageBtn.set_sensitive(False)
        self.exerImageBtn.add(self.exerImage)
        self.exerScrollWindow.add_with_viewport(self.exerImageBtn)
        
        #Short Break Settings Grid
        disclaimerStr = "Disclaimer: This tool does not provide medical advice.\nAlways consult your physician before beginning any exercise program." 
        self.disclaimerLabel = Gtk.Label(disclaimerStr)
        self.disclaimerLabel.modify_font(self.getFont("disclaimer"))
        self.setMargin(self.disclaimerLabel, "10 5 5 5")
        self.disclaimerFrame = Gtk.Frame()
        self.disclaimerFrame.set_border_width(5)
        self.disclaimerFrame.add(self.disclaimerLabel)
        self.setMargin(self.disclaimerFrame, "10 0 0 5")
        tabGrid.attach_next_to(self.disclaimerFrame, self.exerScrollWindow, Gtk.PositionType.BOTTOM, 1, 1)
        
        
    def saveChangesHandler(self, btn, name, helper):
        if(name == "Ok"):
            print "Ok Button"
            helper.hideOnClose() 
        elif(name == "Apply"):
            print "Apply Button"
            print "Changes saved to file"
            self.disableApplyCancelBtns()
        elif(name == "Cancel"):
            print "Cancel Button"
            helper.hideOnClose() 
            
    def enableApplyCancelBtns(self):
        self.timerApplyBtn.set_sensitive(True)
        self.timerCancelBtn.set_sensitive(True)
        
    def disableApplyCancelBtns(self):
        self.timerApplyBtn.set_sensitive(False)
        self.timerCancelBtn.set_sensitive(False)
            
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
        #Create Window UI
        self.window = Gtk.Window()
        self.window.set_resizable(False)
        self.window.set_title("Break My Work")
        self.helper = Helper(self)
        self.ui = UI(self.helper)
        self.window.add(self.ui.getNoteBook())
        
        #Status Icon
        self.statusIcon = Gtk.StatusIcon()
        self.statusIcon.set_from_stock(Gtk.STOCK_HOME)
        self.statusIcon.connect("popup-menu", self.rightClickOnStatus)
        
        self.window.connect("destroy", lambda w: Gtk.main_quit())
        self.window.show_all()
        
    def rightClickOnStatus(self, icon, button, time):
        self.menu = Gtk.Menu()

        aboutItem = Gtk.MenuItem()
        aboutItem.set_label("About")
        quitItem = Gtk.MenuItem()
        quitItem.set_label("Quit")

        aboutItem.connect("activate", self.show_about_dialog)
        quitItem.connect("activate", Gtk.main_quit)

        self.menu.append(aboutItem)
        self.menu.append(quitItem)

        self.menu.show_all() 
        
        def pos(menu, icon):
                return (Gtk.StatusIcon.position_menu(menu, icon))
            
        self.menu.popup(None, None, pos, self.statusicon, button, time) 
        
    def show_about_dialog(self, widget):
        about_dialog = Gtk.AboutDialog()

        about_dialog.set_destroy_with_parent(True)
        about_dialog.set_name("Break My Work")
        about_dialog.set_version("1.0")
        about_dialog.set_authors(["Ravikiran Janardhana"])

        about_dialog.run()
        about_dialog.destroy()
        
    def hideOnClose(self):
        self.window.hide_on_delete()
        self.statusIcon.set_tooltip_text('Window is hidden')
        return True
        
    def getWindow(self):
        return self.window
        
    def main(self):
        Gtk.main()
#end class Builder

class Helper:
    def __init__(self, builder):
        self.b = builder
        
    def hideOnClose(self):
        self.b.window.hide_on_delete()
        self.statusIcon.set_tooltip_text('Window is hidden')
        return True
#end class Helper

if __name__ == "__main__":
    b = Builder()
    b.main()