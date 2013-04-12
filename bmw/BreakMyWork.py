#!/usr/bin/python

import sys
import os
import pickle
from os.path import expanduser

try:
    from gi.repository import Gtk, Pango, AppIndicator3 as appindicator, GdkPixbuf, GLib
except:
    print "Could not GTK3 libraries"
    sys.exit(1)
    
class UI:
    def __init__(self, helper, config):
        self.noteBook = Gtk.Notebook()
        self.h = helper
        self.c = config
        self.tempConfig = {'duration' : config['duration'], 
                           'interval' : config['interval'], 
                           'intervalName' : config['intervalName'],
                           'actionType' : config['actionType'],
                           'firstRun' : config['firstRun'],
                           'enableBreaks' : config['enableBreaks'],
                           'startup' : config['startup']
                          }
        pageStrs = ["Timer", "Exercises"]
        for index in range(len(pageStrs)):
            tabLabel = Gtk.Label(pageStrs[index])
            tabGrid = Gtk.Grid()
            #Add radio button to the grid
            if(pageStrs[index] == "Timer"):
                self.buildTimerTabUI(tabGrid)
                self.loadConfigToUI()
            elif(pageStrs[index] == "Exercises"):
                self.buildExerciseTabUI(tabGrid)
                
            self.noteBook.append_page(tabGrid, tabLabel)
        
    def loadConfigToUI(self):
        #Duration
        self.shortBreakDurationBtn.set_value(self.c['duration'])
        
        #IntervalName
        if(self.c['intervalName'] == "short15"):
            self.shortFifteenBtn.set_active(True)
        elif(self.c['intervalName'] == "short30"):
            self.shortThirtyBtn.set_active(True)
        elif(self.c['intervalName'] == "short60"):
            self.shortSixtyBtn.set_active(True)
        elif(self.c['intervalName'] == "custom"):
            self.shortCustomBtn.set_active(True)
            self.shortBreakCustomMinsBtn.set_value(self.c['interval'])
        
        #Action
        if(self.c['actionType'] == "popup"):
            self.shortBreakActionPopUpBtn.set_active(True)
        elif(self.c['actionType'] == "tooltip"):
            self.shortBreakActionToolTipBtn.set_active(True)
        elif(self.c['actionType'] == "disableinp"):
            self.shortBreakActionDisableInpBtn.set_active(True)
            
        #Enable or Disable breaks
        if(self.c['enableBreaks']):
            self.shortBreakEnableBtn.set_active(True)
        else:
            self.shortBreakEnableBtn.set_active(False)
            
        #Enable or Disable startup
        if(self.c['startup']):
            self.shortBreakStartupBtn.set_active(True)
        else:
            self.shortBreakStartupBtn.set_active(False)
        self.disableApplyCancelBtns()
            
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
        self.setMargin(self.shortBreakActionFrame, "10 0 10 10")
        self.shortBreakActionGrid = Gtk.Grid()
        self.shortBreakActionGrid.set_border_width(10)
        self.shortBreakActionFrame.add(self.shortBreakActionGrid)
        
        #Startup Changes Grid
        self.shortBreakStartupGrid = Gtk.Grid()
        self.shortBreakStartupGrid.set_border_width(10)
        
        #Save Changes Grid
        self.saveChangesGrid = Gtk.Grid()
        self.saveChangesGrid.set_border_width(10)
        
        #add them to tabGrid
        tabGrid.add(self.shortBreakSettingsFrame)
        tabGrid.attach_next_to(self.shortBreakActionFrame, self.shortBreakSettingsFrame, Gtk.PositionType.BOTTOM, 1, 1)
        tabGrid.attach_next_to(self.shortBreakStartupGrid, self.shortBreakActionFrame, Gtk.PositionType.BOTTOM, 1, 1)
        tabGrid.attach_next_to(self.saveChangesGrid, self.shortBreakStartupGrid, Gtk.PositionType.BOTTOM, 2, 1)
        
        #build short and long break settings UI
        self.buildShortBreakSettingsUI(self.shortBreakSettingsGrid)
        self.buildShortBreakActionUI(self.shortBreakActionGrid)
        self.buildShortBreakStartupUI(self.shortBreakStartupGrid)
        self.buildSaveChangesUI(self.saveChangesGrid)

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
        #Disable duration as of now
        #self.shortTimerChoiceBox.pack_start(self.shortBreakDurationBox, True, True, 0)
        
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
        self.shortBreakActionLabel.modify_font(self.getFont("breakMessage"))
        self.shortBreakActionLabel.set_alignment(0, 0.5)
        self.setMargin(self.shortBreakActionLabel, "10 10 10 10");
        tabGrid.add(self.shortBreakActionLabel)
        
        #short break action vBox to hold choices
        self.shortActionChoiceBox = Gtk.Box()
        self.shortActionChoiceBox.set_orientation(Gtk.Orientation.VERTICAL)
        self.setMargin(self.shortActionChoiceBox, "0 0 10 10")
        tabGrid.attach_next_to(self.shortActionChoiceBox, self.shortBreakActionLabel, Gtk.PositionType.BOTTOM, 1, 1)
        
        #short break action - tooltip reminder
        self.shortBreakActionToolTipStr = "Show Tool Tip Reminder (gentle) - not available"
        self.shortBreakActionToolTipBtn = Gtk.RadioButton.new_with_label_from_widget(None, self.shortBreakActionToolTipStr);
        self.shortBreakActionToolTipBtn.connect("toggled", self.updateShortBreakAction, "shortBreakToolTip")
        self.shortBreakActionToolTipBtn.set_margin_top(5)
        self.shortBreakActionToolTipBtn.set_sensitive(False)
        self.shortActionChoiceBox.pack_start(self.shortBreakActionToolTipBtn, True, True, 0)
        
        #short break action - pop up reminder
        self.shortBreakActionPopUpStr = "Show Pop Up Reminder (invasive)"
        self.shortBreakActionPopUpBtn = Gtk.RadioButton.new_with_label_from_widget(self.shortBreakActionToolTipBtn, self.shortBreakActionPopUpStr);
        self.shortBreakActionPopUpBtn.connect("toggled", self.updateShortBreakAction, "shortBreakPopUp")
        self.shortBreakActionPopUpBtn.set_margin_top(5)
        self.shortActionChoiceBox.pack_start(self.shortBreakActionPopUpBtn, True, True, 0)
        
        #short break action - lock keyboard and mouse
        self.shortBreakActionDisableInpStr = "Disable Keyboard and Mouse (forces a break) - not available"
        self.shortBreakActionDisableInpBtn = Gtk.RadioButton.new_with_label_from_widget(self.shortBreakActionToolTipBtn, self.shortBreakActionDisableInpStr);
        self.shortBreakActionDisableInpBtn.connect("toggled", self.updateShortBreakAction, "shortBreakDisableInp")
        self.shortBreakActionDisableInpBtn.set_margin_top(5)
        self.shortBreakActionDisableInpBtn.set_sensitive(False)
        self.shortActionChoiceBox.pack_start(self.shortBreakActionDisableInpBtn, True, True, 0)
        
    def buildShortBreakStartupUI(self, tabGrid):
        #add check box button
        self.startupBox = Gtk.Box()
        self.startupBox.set_orientation(Gtk.Orientation.HORIZONTAL)
        tabGrid.add(self.startupBox)
        
        #short break startup enable/disable CheckBox
        self.shortBreakStartupBtn = Gtk.CheckButton("Start BreakMyWork on system startup")
        self.shortBreakStartupBtn.set_active(True)
        self.shortBreakStartupBtn.connect("toggled", self.toggleStartup)
        self.shortBreakStartupBtn.set_margin_left(10)
        self.startupBox.pack_start(self.shortBreakStartupBtn, True, True, 0)
        
    def buildSaveChangesUI(self, tabGrid):
        #add ok, apply, cancel buttons
        self.saveChangesBox = Gtk.Box()
        self.saveChangesBox.set_orientation(Gtk.Orientation.HORIZONTAL)
        tabGrid.add(self.saveChangesBox)
        
        #OK Button
        self.timerOKBtn = Gtk.Button()
        self.timerOKBtn.set_label("Ok")
        self.timerOKBtn.set_size_request(90, 30)
        self.timerOKBtn.connect("clicked", self.saveChangesHandler, "Ok")
        self.saveChangesBox.pack_start(self.timerOKBtn, True, True, 0)
        
        #Apply Button
        self.timerApplyBtn = Gtk.Button()
        self.timerApplyBtn.set_label("Apply")
        self.timerApplyBtn.set_size_request(90, 30)
        self.timerApplyBtn.set_margin_left(10)
        self.timerApplyBtn.set_sensitive(False)
        self.timerApplyBtn.connect("clicked", self.saveChangesHandler, "Apply")
        self.saveChangesBox.pack_start(self.timerApplyBtn, True, True, 0)
        
        #Cancel Button
        self.timerCancelBtn = Gtk.Button()
        self.timerCancelBtn.set_label("Cancel")
        self.timerCancelBtn.set_size_request(90, 30)
        self.timerCancelBtn.set_margin_left(10)
        self.timerCancelBtn.set_sensitive(False)
        self.timerCancelBtn.connect("clicked", self.saveChangesHandler, "Cancel")
        self.saveChangesBox.pack_start(self.timerCancelBtn, True, True, 0)
        
    def toggleStartup(self, widget):
        if(self.shortBreakStartupBtn.get_active()):
            self.tempConfig['startup'] = True
        else:
            self.tempConfig['startup'] = False
        self.enableApplyCancelBtns()
        return True
            
    def getFont(self, textType):
        if(textType == "heading"):
            return Pango.FontDescription("14")
        elif(textType == "disclaimer"):
            return Pango.FontDescription("#ff0000 12")
        elif(textType == "breakMessage"):
            return Pango.FontDescription("12")
        
        #default (normal)
        return Pango.FontDescription("12")
        
    def setMargin(self, widget, margin):
        marginArr = margin.split(" ")
        widget.set_margin_top(int(marginArr[0]))
        widget.set_margin_right(int(marginArr[1]))
        widget.set_margin_bottom(int(marginArr[2]))
        widget.set_margin_left(int(marginArr[3]))
        
    def updateShortTimer(self, name):
        newInterval = -1
        newIntervalName = ""
        if(name == "custom"):
            newInterval = self.shortBreakCustomMinsBtn.get_value_as_int()
            newIntervalName = "custom"
            self.enableApplyCancelBtns()
        elif(name == "short15"):
            newInterval = 15
            newIntervalName = "short15"
            self.enableApplyCancelBtns()
        elif(name == "short30"):
            newInterval = 30
            newIntervalName = "short30"
            self.enableApplyCancelBtns()
        elif(name == "short60"):
            newInterval = 60
            newIntervalName = "short60"
            self.enableApplyCancelBtns()
            
        if(newInterval != -1):
            print "Activate Short Break Timer every %d minutes" % (newInterval)
            self.tempConfig['interval'] = newInterval
            if(newIntervalName != ""):
                self.tempConfig['intervalName'] = newIntervalName
            
    def toggleShortBreaks(self, btn):        
        self.enableApplyCancelBtns()
        if(btn.get_active()):
            #enable short breaks
            self.shortTimerChoiceBox.set_sensitive(True)
            self.shortActionChoiceBox.set_sensitive(True)
            print "Enable short breaks"
            self.tempConfig['enableBreaks'] = True
        else:
            #disable short breaks
            self.shortTimerChoiceBox.set_sensitive(False)
            self.shortActionChoiceBox.set_sensitive(False)
            print "Disable short breaks"
            self.tempConfig['enableBreaks'] = False
        return True
            
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
        return True
                
    def updateCustomShortBreak(self, btn):
        self.updateShortTimer("custom")
        return True
    
    def updateShortBreakDuration(self, btn):
        newDuration = self.shortBreakDurationBtn.get_value_as_int()
        print "Short Break Duration =  ", newDuration, " mins"
        self.tempConfig['duration'] = newDuration
        return True
        
    def updateShortBreakAction(self, btn, name):
        newAction = ""
        state = 0
        if(btn.get_active()):
            state = 1
            
        if(name == "shortBreakToolTip"):
            if(state == 1):
                newAction = "tooltip"
                self.enableApplyCancelBtns()
        elif(name == "shortBreakPopUp"):
            if(state == 1):
                newAction = "popup"
                self.enableApplyCancelBtns()
        elif(name == "shortBreakDisableInp"):
            if(state == 1):
                newAction = "disableinp"
                self.enableApplyCancelBtns()
                
        if(newAction != ""):
            print "Action changed = %s" % (newAction)
            self.tempConfig['actionType'] = newAction
        return True
        
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
        
    def saveChangesHandler(self, btn, name):
        if(name == "Ok"):
            print "Ok Button"
            self.h.hideOnClose()
        elif(name == "Apply"):
            print "Apply Button"
            self.c = self.tempConfig
            #Copy tempConfig to config and write it to config file
            self.h.updateConfig(self.tempConfig)
            #Load newConfig to the UI (redundant)
            self.loadConfigToUI()
            #Stop old timers and start new timers based on new config
            if(self.c['enableBreaks']):
                self.h.mainWindow.stopTimers()
                self.h.mainWindow.startTimers()
                print "Breaks Enabled, so restarting timers"
            else:
                self.h.mainWindow.stopTimers()
                self.h.mainWindow.appInd.set_label("", "")
                print "Breaks Disabled, canceling all timers"
            if(self.c['startup']):
                self.h.mainWindow.addAppToStartup()
            else:
                self.h.mainWindow.removeAppFromStartup()
            print "Changes saved to file"
            self.disableApplyCancelBtns()
        elif(name == "Cancel"):
            print "Cancel Button"
            self.tempConfig = {'duration' : self.c['duration'], 
                               'interval' : self.c['interval'], 
                               'intervalName' : self.c['intervalName'], 
                               'actionType' : self.c['actionType'],
                               'firstRun' : self.c['firstRun'],
                               'enableBreaks' : self.c['enableBreaks'],
                               'startup' : self.c['startup']
                               }
            self.h.hideOnClose()
        return True
            
    def enableApplyCancelBtns(self):
        self.timerApplyBtn.set_sensitive(True)
        self.timerCancelBtn.set_sensitive(True)
        
    def disableApplyCancelBtns(self):
        self.timerApplyBtn.set_sensitive(False)
        self.timerCancelBtn.set_sensitive(False)
            
    def getNoteBook(self):
        return self.noteBook
#end class UI

class BreakScheduler(object):
    def __init__(self, window, interval, action):
        self.mainWindow = window
        self.minuteMode = 1
        
        self._timer = 0
        self._labelTimer = 0
        
        self.interval = interval
        self.labelInterval = 1
        
        if(self.minuteMode):
            #interval is in minutes, convert it to seconds
            self.interval = self.interval * 60
            #update appIndicator label once every minute
            self.labelInterval = 1 * 60
        
        self.action = action
        self.isRunning = False
        
        self.start()
        
    def setNewInterval(self, newInterval):
        self.stop()
        if(self.minuteMode):
            #interval is in minutes, convert it to seconds
            newInterval = newInterval * 60
        self.interval = newInterval
        self.start()
        
    def setNewAction(self, newAction):
        self.action = newAction
        
    def showBreakMessageUI(self, action):
        #Update Label Timer 
        self.timerStart = GLib.get_current_time()
        self.timerEnd = self.timerStart + self.interval
        
        #Show UI
        self.breakMessageWindow = Gtk.Window()
        self.breakMessageWindow.set_position(Gtk.WindowPosition.CENTER)
        self.breakMessageWindow.set_size_request(375, 100)
        
        self.breakBox = Gtk.Box()
        self.breakBox.set_orientation(Gtk.Orientation.VERTICAL)
        
        self.breakReminderText = "Please take a break of %d mins, it will help you avoid RSI Injuries." % (self.getDuration())
        self.breakReminderLabel = Gtk.Label(self.breakReminderText)
        #self.breakReminderLabel.modify_font(self.mainWindow.ui.getFont("heading"))
        
        self.breakActionBox = Gtk.Box()
        self.breakActionBox.set_orientation(Gtk.Orientation.HORIZONTAL)
        
        self.breakOkBtn = Gtk.Button()
        self.breakOkBtn.set_label("Ok")
        self.breakOkBtn.set_size_request(70, 30)
        self.breakOkBtn.connect("clicked", lambda w: self.breakMessageWindow.destroy())
        
        self.exerciseBtnText = "Show me some Exercises"
        self.exerciseBtn = Gtk.Button()
        self.exerciseBtn.set_label(self.exerciseBtnText)
        self.exerciseBtn.set_margin_left(5)
        self.exerciseBtn.set_size_request(200, 30)
        self.exerciseBtn.connect("clicked", self.showExerciseTab)
        
        self.breakActionBox.pack_start(self.breakOkBtn, False, False, 0)
        self.breakActionBox.pack_start(self.exerciseBtn, False, False, 0)
        
        self.breakBox.pack_start(self.breakReminderLabel, True, True, 0)
        self.breakBox.pack_start(self.breakActionBox, False, False, 0)
        
        self.breakMessageWindow.add(self.breakBox)
        
        self.breakMessageWindow.set_title("Break My Work - Take a break")
        self.breakMessageWindow.set_border_width(15)
        self.breakMessageWindow.show_all()
        
        print "Action = %s, Interval = %d" % (self.action, self.interval)
        
        return True
        
    def getDuration(self):
        return self.mainWindow.config['duration']
    
    def getInterval(self):
        return self.mainWindow.config['interval']
    
    def getIntervalName(self):
        return self.mainWindow.config['intervalName']
    
    def getAction(self):
        return self.mainWindow.config['actionType']
                                         
    def showExerciseTab(self, widget):
        self.mainWindow.showConfigureWindow()
        self.mainWindow.ui.getNoteBook().set_current_page(1)
        self.breakMessageWindow.destroy()
        
    def start(self):
        if not self.isRunning:
            self.timerStart = GLib.get_current_time()
            self._timer = GLib.timeout_add_seconds(self.interval, self.showBreakMessageUI, self.action)
            self.timerEnd = self.timerStart + self.interval
            self._labelTimer = GLib.timeout_add_seconds(self.labelInterval, self.updateAppLabel)
            #Call immediately to update the appLabel
            print "Trying to update app label first time"
            self.updateAppLabel()
            self.isRunning = True

    def stop(self):
        if(self._timer > 0):
            GLib.source_remove(self._timer)
        if(self._labelTimer > 0):
            GLib.source_remove(self._labelTimer)
        self.isRunning = False
        
    def updateAppLabel(self):
        self.currTime = GLib.get_current_time()
        print "Inside UpdateAppLabel, currTime = %d, timerStart = %d, timerEnd = %d" % (self.currTime, self.timerStart, self.timerEnd)
        if(self.currTime < self.timerEnd):
            if(self.minuteMode):
                diff = int((self.timerEnd - self.currTime) / 60)
                self.mainWindow.updateAppIndicatorLabelInMins(diff)
            else:
                diff = int(self.timerEnd - self.currTime)
                self.mainWindow.updateAppIndicatorLabelInSecs(diff)
        return True
#end BreakScheduler

class MainWindowBuilder():
    def __init__(self):
        #Create Window UI
        self.window = Gtk.Window()
        self.window.set_resizable(False)
        self.window.set_title("Break My Work")
        
        #setup ui
        self.helper = Helper(self)
        
        #setup config
        self.config = self.loadConfig()
        print self.config
        
        #setup ui
        self.ui = UI(self.helper, self.config)
        self.window.add(self.ui.getNoteBook())
        self.window.set_position(Gtk.WindowPosition.CENTER)
        
        #Build App Indicator
        self.buildAppIndicator()
        
        #Setup Timer
        self.breakScheduler = BreakScheduler(self, self.config['interval'], self.config['actionType'])
        
        self.window.connect("delete-event", self.hideOnClose)
        if(self.config['firstRun']):
            self.window.show_all()
            self.config['firstRun'] = False
            self.writeNewConfigToFile()
            self.addAppToStartup()
            print self.config
        else:
            self.window.hide()
        
    def hideOnClose(self, widget=None, event=None):
        self.window.hide()
        return True
        
    def rightClickOnStatus(self, icon, button, time):
        self.configMenu.show_all()
        
    def showConfigureWindow(self, widget=None):
        self.window.show_all()
        
    def loadConfig(self):
        self.defaultConfig = {'duration' : 2,
                              'interval' : 15,
                              'intervalName': 'short15',
                              'actionType' : 'popup',
                              'firstRun' : True,
                              'enableBreaks' : True,
                              'startup' : True}
        self.currConfig = None
        #Check if a config directory exists
        self.homeDir = expanduser("~")
        self.bmwConfigDir = self.homeDir + "/breakMyWork"
        self.bmwConfigFile = self.bmwConfigDir + "/bmwConfig.pickle"
        if(os.path.isdir(self.bmwConfigDir)):
            if(os.path.isfile(self.bmwConfigFile)):
                #Load existing config
                print "Loaded existing config"
                try:
                    self.currConfig = pickle.load(open(self.bmwConfigFile, "rb"))
                except IOError as e:
                    print "Exception error is : %s " % (e)
            else:
                #Create a new default config
                print "Created a new default config file"
                self.currConfig = self.defaultConfig
                try:
                    pickle.dump(self.currConfig, open(self.bmwConfigFile, "rb"))
                except IOError as e:
                    print "Exception error is : %s " % (e)
        else:
            #Created a new config directory and file
            self.currConfig = self.defaultConfig
            print "Created a new config directory and file"
            os.makedirs(self.bmwConfigDir)
            try:
                pickle.dump(self.currConfig, open(self.bmwConfigFile, "wb"))
            except IOError as e:
                print "Exception error is : %s " % (e)
                
        return self.currConfig
    
    def writeNewConfigToFile(self):
        self.bmwConfigDir = self.homeDir + "/breakMyWork"
        self.bmwConfigFile = self.bmwConfigDir + "/bmwConfig.pickle"
        #Create the config directory if it does not exist
        if(not os.path.isdir(self.bmwConfigDir)):
            os.makedirs(self.bmwConfigDir)
            
        #Overwrite the config file
        print "Overwrite Config File"
        try:
            pickle.dump(self.config, open(self.bmwConfigFile, "wb"))
        except IOError as e:
            print "Exception error is : %s " % (e)
                
        return self.currConfig
        
    def buildAppIndicator(self):
        self.appInd = appindicator.Indicator.new("MyApp", "", appindicator.IndicatorCategory.APPLICATION_STATUS)
        self.appInd.set_status (appindicator.IndicatorStatus.ACTIVE)
        self.homeDir = expanduser("~")
        self.appIconDir = self.homeDir+"/workspace/BreakMyWork/bmw"
        print self.appIconDir
        self.appInd.set_icon_theme_path(self.appIconDir);
        self.iconName = "theicon"
        self.appInd.set_icon(self.iconName)
        self.configMenu = Gtk.Menu()

        self.configureItem = Gtk.MenuItem()
        self.configureItem.set_label("Configure")
        self.aboutItem = Gtk.MenuItem()
        self.aboutItem.set_label("About")
        self.menuSeparator1 = Gtk.SeparatorMenuItem()
        self.quitItem = Gtk.MenuItem()
        self.quitItem.set_label("Quit")

        self.configureItem.connect("activate", self.showConfigureWindow)
        self.aboutItem.connect("activate", self.showAboutDialog)
        self.quitItem.connect("activate", self.cleanUp)

        self.configMenu.append(self.configureItem)
        self.configMenu.append(self.aboutItem)
        self.configMenu.append(self.menuSeparator1)
        self.configMenu.append(self.quitItem)
        
        self.appInd.set_menu(self.configMenu)
        
        self.configMenu.show_all()
        
    def showBreakMessageUI(self, action):
        print "test"
        return True
        
    def cleanUp(self, widget):
        self.breakScheduler.stop()
        Gtk.main_quit()
        
    def showAboutDialog(self, widget):
        self.aboutDialog = Gtk.AboutDialog()

        self.aboutDialog.set_program_name("Break My Work")
        self.aboutDialog.set_version("1.0")
        self.aboutDialog.set_comments("Break My Work is a simple Repetitive Strain Injury Prevention Software.")
        self.aboutDialog.set_destroy_with_parent(True)
        self.logoIcon = GdkPixbuf.Pixbuf.new_from_file_at_size("theicon.png", 32, 32)
        self.aboutDialog.set_logo(self.logoIcon)
        self.webUrl = "http://www.ravikiranj.net"
        self.aboutDialog.set_website(self.webUrl)
        self.aboutDialog.set_authors(["Ravikiran Janardhana"])

        self.aboutDialog.run()
        self.aboutDialog.destroy()
        
    def updateAppIndicatorLabelInMins(self, mins):
        hours = int(mins / 60)
        minutes = mins % 60
        labelStr = "(" + str(hours).rjust(2, '0')+ ":" + str(minutes).rjust(2, '0') + ")"
        print "Updated app label = %s" % (labelStr)
        self.appInd.set_label(labelStr, "")

    def updateAppIndicatorLabelInSecs(self, secs):
        minutes = int(secs / 60)
        seconds = secs % 60
        labelStr = "(" + str(minutes).rjust(2, '0')+ ":" + str(seconds).rjust(2, '0') + ")"
        print "Updated app label = %s" % (labelStr)
        self.appInd.set_label(labelStr, "")
        
    def stopTimers(self):    
        self.breakScheduler.stop()
        
    def startTimers(self):
        self.breakScheduler.setNewInterval(self.config['interval'])
        
    def addAppToStartup(self):
        self.desktopFileStr = """
[Desktop Entry]
Type=Application
Exec=python /home/ravikirn/workspace/BreakMyWork/bmw/BreakMyWork.py
Hidden=false
NoDisplay=false
X-GNOME-Autostart-enabled=true
Name[en_US]=Break My Work
Name=Break My Work
Comment[en_US]=
Comment="""
        self.desktopFilePath = self.homeDir + "/.config/autostart/"
        self.desktopFileName = self.desktopFilePath + "break-my-work.desktop"
        print self.desktopFileName
        try:
            self.desktopFileHandle = open(self.desktopFileName, "w")
            self.desktopFileHandle.write(self.desktopFileStr)
            self.desktopFileHandle.close()
        except IOError as e:
            print "here"
            print "Exception error is : %s " % (e)
            
    def removeAppFromStartup(self):
        self.desktopFilePath = self.homeDir + "/.config/autostart/"
        self.desktopFileName = self.desktopFilePath + "break-my-work.desktop"
        if(os.path.isfile(self.desktopFileName)):
            os.remove(self.desktopFileName)
        
    def getWindow(self):
        return self.window
        
    def main(self):
        Gtk.main()
#end class Builder

class Helper:
    def __init__(self, mainWindow):
        self.mainWindow = mainWindow
        
    def hideOnClose(self):
        self.mainWindow.hideOnClose()
        
    def getBreakScheduler(self):
        return self.mainWindow.breakScheduler
    
    def updateConfig(self, c):
        self.mainWindow.config = c
        self.writeNewConfig()
        
    def writeNewConfig(self):
        self.mainWindow.writeNewConfigToFile()
#end class Helper

if __name__ == "__main__":
    mainWindow = MainWindowBuilder()
    mainWindow.main()