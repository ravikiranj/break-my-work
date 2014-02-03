#!/usr/bin/env python

from os.path import expanduser
import os
import pickle
import sys
import copy

#global debug
DEBUG = 0

def debugLog(debugStr):
    if(DEBUG):
        print debugStr
#end debugLog

try:
    from gi.repository import Gtk, Pango, AppIndicator3 as appindicator, GdkPixbuf, GLib
except:
    print "Could not GTK3 libraries, exiting now"
    sys.exit(1)
    
class UI:
    def __init__(self, helper, config):
        self.noteBook = Gtk.Notebook()
        self.defaultMsg = "Please take a break of 2-5 mins, it will help you avoid RSI Injuries."
        self.h = helper
        self.c = config
        self.tempConfig = copy.deepcopy(config)
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
        self.breakDurationBtn.set_value(self.c['duration'])
        
        #IntervalName
        if 'intervalName' in self.c:
            if(self.c['intervalName'] == "15mins"):
                self.fifteenBtn.set_active(True)
            elif(self.c['intervalName'] == "30mins"):
                self.thirtyBtn.set_active(True)
            elif(self.c['intervalName'] == "60mins"):
                self.sixtyBtn.set_active(True)
            elif(self.c['intervalName'] == "custom"):
                self.customBtn.set_active(True)
                self.breakCustomMinsBtn.set_value(self.c['interval'])
        else:
            self.sixtyBtn.set_active(True)
        
        #Action (this should always be set)
        if('actionType' in self.c and self.c['actionType'] == "popup"):
            self.breakActionPopUpBtn.set_active(True)
            
        #Enable or Disable breaks
        if('enableBreaks' in self.c and self.c['enableBreaks']):
            self.breakEnableBtn.set_active(True)
        else:
            self.breakEnableBtn.set_active(False)
            
        if('customBreakMsg' in self.c and self.c['customBreakMsg']):
            self.breakMsgTextBuffer.set_text(self.c['customBreakMsg'])
        else:
            self.breakMsgTextBuffer.set_text(self.defaultMsg)
            
        #Enable or Disable startup
        if(self.c['startup']):
            self.breakStartupBtn.set_active(True)
        else:
            self.breakStartupBtn.set_active(False)
        self.disableApplyCancelBtns()
            
    def buildTimerTabUI(self, tabGrid):
        #Set tab grid border width
        tabGrid.set_border_width(15)
        
        #Break Settings Grid
        self.breakSettingsFrame = Gtk.Frame()
        self.breakSettingsFrame.set_border_width(5)
        self.setMargin(self.breakSettingsFrame, "10 0 10 10")
        self.breakSettingsGrid = Gtk.Grid()
        self.breakSettingsGrid.set_border_width(10)
        self.breakSettingsFrame.add(self.breakSettingsGrid)
        
        #Break Action Grid
        self.breakActionFrame = Gtk.Frame()
        self.breakActionFrame.set_border_width(5)
        self.setMargin(self.breakActionFrame, "10 0 10 10")
        self.breakActionGrid = Gtk.Grid()
        self.breakActionGrid.set_border_width(10)
        self.breakActionFrame.add(self.breakActionGrid)
        
        #Message Settings Grid
        self.breakMessageSettingsFrame = Gtk.Frame()
        self.breakMessageSettingsFrame.set_border_width(5)
        self.setMargin(self.breakMessageSettingsFrame, "10 0 10 10")
        self.breakMessageSettingsGrid = Gtk.Grid()
        self.breakMessageSettingsGrid.set_border_width(10)
        self.breakMessageSettingsFrame.add(self.breakMessageSettingsGrid)
        
        #Startup Changes Grid
        self.breakStartupGrid = Gtk.Grid()
        self.breakStartupGrid.set_border_width(10)
        
        #Save Changes Grid
        self.saveChangesGrid = Gtk.Grid()
        self.saveChangesGrid.set_border_width(10)
        
        #add them to tabGrid
        tabGrid.add(self.breakSettingsFrame)
        tabGrid.attach_next_to(self.breakActionFrame, self.breakSettingsFrame, Gtk.PositionType.BOTTOM, 1, 1)
        tabGrid.attach_next_to(self.breakMessageSettingsFrame, self.breakActionFrame, Gtk.PositionType.BOTTOM, 1, 1)
        tabGrid.attach_next_to(self.breakStartupGrid, self.breakMessageSettingsFrame, Gtk.PositionType.BOTTOM, 1, 1)
        tabGrid.attach_next_to(self.saveChangesGrid, self.breakStartupGrid, Gtk.PositionType.BOTTOM, 2, 1)
        
        #build break settings UI
        self.buildBreakSettingsUI(self.breakSettingsGrid)
        self.buildBreakActionUI(self.breakActionGrid)
        self.buildBreakMessageSettingsUI(self.breakMessageSettingsGrid)
        self.buildBreakStartupUI(self.breakStartupGrid)
        self.buildSaveChangesUI(self.saveChangesGrid)

    def buildBreakSettingsUI(self, tabGrid):
        #break label
        self.breakLabel = Gtk.Label('Break Intervals')
        self.breakLabel.modify_font(self.getFont("heading"))
        self.breakLabel.set_alignment(0, 0.5)
        self.setMargin(self.breakLabel, "10 10 10 10");
        tabGrid.add(self.breakLabel)
        
        #break enable/disable CheckBox
        self.breakEnableBtn = Gtk.CheckButton("Enable Breaks")
        self.breakEnableBtn.set_active(True)
        self.breakEnableBtn.connect("toggled", self.toggleBreaks)
        self.breakEnableBtn.set_margin_left(10)
        tabGrid.attach_next_to(self.breakEnableBtn, self.breakLabel, Gtk.PositionType.BOTTOM, 1, 1);
        
        #break vBox to hold timer choices
        self.timerChoiceBox = Gtk.Box()
        self.timerChoiceBox.set_orientation(Gtk.Orientation.VERTICAL)
        self.setMargin(self.timerChoiceBox, "10 0 10 30")
        tabGrid.attach_next_to(self.timerChoiceBox, self.breakEnableBtn, Gtk.PositionType.BOTTOM, 1, 1)
        
        #break duration hbox
        self.breakDurationBox = Gtk.Box()
        self.breakDurationBox.set_orientation(Gtk.Orientation.HORIZONTAL)
        self.setMargin(self.breakDurationBox, "0 0 5 0")
        #Disable duration as of now
        #self.timerChoiceBox.pack_start(self.breakDurationBox, True, True, 0)
        
        #break Duration label        
        breakDurationLabel = Gtk.Label("Duration")
        self.breakDurationBox.pack_start(breakDurationLabel, True, True, 0)
        
        #value, lower, upper, step_inc, page_inc, page_size
        self.breakDurationAdjustment = Gtk.Adjustment(2, 1, 10, 1, 2, 0)
        #break custom mins spinner button
        self.breakDurationBtn = Gtk.SpinButton()
        self.breakDurationBtn.set_adjustment(self.breakDurationAdjustment)
        self.breakDurationBtn.set_numeric(True)
        self.breakDurationBtn.set_digits(0)
        self.breakDurationBtn.set_update_policy(Gtk.SpinButtonUpdatePolicy.IF_VALID)
        self.breakDurationBtn.set_sensitive(True)
        self.breakDurationBtn.set_max_length(2)
        self.breakDurationBtn.set_margin_left(5)
        self.breakDurationAdjustment.connect("value_changed", self.updateBreakDuration)
        self.breakDurationBox.pack_start(self.breakDurationBtn, True, True, 0)
        
        #break Duration 'minutes' label        
        breakDurationMinsLabel = Gtk.Label("minutes")
        breakDurationMinsLabel.set_margin_left(2)
        self.breakDurationBox.pack_start(breakDurationMinsLabel, True, True, 0)
        
        #break 15 mins
        self.fifteenStr = "Once every 15 mins"
        self.fifteenBtn = Gtk.RadioButton.new_with_label_from_widget(None, self.fifteenStr);
        self.fifteenBtn.set_margin_top(5)
        self.fifteenBtn.connect("toggled", self.changeBreakTimer, "15mins");
        self.timerChoiceBox.pack_start(self.fifteenBtn, True, True, 0)
        
        #break 30 mins
        self.thirtyStr = "Once every 30 mins"
        self.thirtyBtn = Gtk.RadioButton.new_with_label_from_widget(self.fifteenBtn, self.thirtyStr);
        self.thirtyBtn.set_margin_top(5)
        self.thirtyBtn.connect("toggled", self.changeBreakTimer, "30mins");
        self.timerChoiceBox.pack_start(self.thirtyBtn, True, True, 0)
        
        #break 60 mins
        self.sixtyStr = "Once every 60 mins"
        self.sixtyBtn = Gtk.RadioButton.new_with_label_from_widget(self.fifteenBtn, self.sixtyStr);
        self.sixtyBtn.set_margin_top(5)
        self.sixtyBtn.connect("toggled", self.changeBreakTimer, "60mins");
        self.timerChoiceBox.pack_start(self.sixtyBtn, True, True, 0)
        
        #break custom mins radio button
        self.customBtn = Gtk.RadioButton.new_with_label_from_widget(self.fifteenBtn, "Custom");
        self.customBtn.set_margin_top(5)
        self.customBtn.connect("toggled", self.changeBreakTimer, "custom");
        
        #break HBOX to hold custom mins data
        self.customHBox = Gtk.Box()
        self.customHBox.set_orientation(Gtk.Orientation.HORIZONTAL)
        self.timerChoiceBox.pack_start(self.customHBox, True, True, 0)
        self.customHBox.pack_start(self.customBtn, True, True, 0)
        
        #value, lower, upper, step_inc, page_inc, page_size
        self.breakCustomMinsAdjustment = Gtk.Adjustment(60, 1, 999, 1, 10, 0)
        #break custom mins spinner button
        self.breakCustomMinsBtn = Gtk.SpinButton()
        self.breakCustomMinsBtn.set_adjustment(self.breakCustomMinsAdjustment)
        self.breakCustomMinsBtn.set_numeric(True)
        self.breakCustomMinsBtn.set_digits(0)
        self.breakCustomMinsBtn.set_update_policy(Gtk.SpinButtonUpdatePolicy.IF_VALID)
        self.breakCustomMinsBtn.set_margin_left(5)
        self.breakCustomMinsBtn.set_max_length(3)
        self.breakCustomMinsBtn.set_sensitive(False)
        self.breakCustomMinsBtn.set_wrap(True)
        self.breakCustomMinsAdjustment.connect("value_changed", self.updateCustomBreak)
        self.customHBox.pack_start(self.breakCustomMinsBtn, True, True, 0)
        
        #break custom mins label
        customLabel = Gtk.Label("minutes")
        customLabel.set_margin_left(5)
        self.customHBox.pack_start(customLabel, True, True, 0)
        
    def buildBreakActionUI(self, tabGrid):
        #break action label
        self.breakActionLabel = Gtk.Label('Break Action')
        self.breakActionLabel.modify_font(self.getFont("breakMessage"))
        self.breakActionLabel.set_alignment(0, 0.5)
        self.setMargin(self.breakActionLabel, "10 10 10 10");
        tabGrid.add(self.breakActionLabel)
        
        #break action vBox to hold choices
        self.actionChoiceBox = Gtk.Box()
        self.actionChoiceBox.set_orientation(Gtk.Orientation.VERTICAL)
        self.setMargin(self.actionChoiceBox, "0 0 10 10")
        tabGrid.attach_next_to(self.actionChoiceBox, self.breakActionLabel, Gtk.PositionType.BOTTOM, 1, 1)
        
        #break action - pop up reminder
        self.breakActionPopUpStr = "Show Pop Up Reminder"
        self.breakActionPopUpBtn = Gtk.RadioButton.new_with_label_from_widget(None, self.breakActionPopUpStr);
        self.breakActionPopUpBtn.connect("toggled", self.updateBreakAction, "breakPopUp")
        self.breakActionPopUpBtn.set_margin_top(5)
        self.actionChoiceBox.pack_start(self.breakActionPopUpBtn, True, True, 0)
        
    def buildBreakMessageSettingsUI(self, tabGrid):
        self.breakMsgSettingsLabel = Gtk.Label('Break Message')
        self.breakMsgSettingsLabel.modify_font(self.getFont("breakMessage"))
        self.breakMsgSettingsLabel.set_alignment(0, 0.5)
        self.setMargin(self.breakMsgSettingsLabel, "10 10 10 10");
        tabGrid.add(self.breakMsgSettingsLabel)
        
        self.breakMsgSettingsWindow = Gtk.ScrolledWindow()
        self.breakMsgSettingsWindow.set_hexpand(True)
        self.breakMsgSettingsWindow.set_vexpand(True)
        self.breakMsgSettingsWindow.set_size_request(200, 75)
        tabGrid.attach_next_to(self.breakMsgSettingsWindow, self.breakMsgSettingsLabel, Gtk.PositionType.BOTTOM, 1, 1)
        
        #add text entry
        self.breakMsgText = Gtk.TextView()
        self.breakMsgTextBuffer = self.breakMsgText.get_buffer()
        self.breakMsgTextBuffer.set_text(self.defaultMsg)
        self.breakMsgText.set_editable(True)
        self.breakMsgText.set_border_width(10)
        
        self.breakMsgSettingsWindow.add(self.breakMsgText)
        
    def buildBreakStartupUI(self, tabGrid):
        #add check box button
        self.startupBox = Gtk.Box()
        self.startupBox.set_orientation(Gtk.Orientation.HORIZONTAL)
        tabGrid.add(self.startupBox)
        
        #break startup enable/disable CheckBox
        self.breakStartupBtn = Gtk.CheckButton("Start BreakMyWork on system startup")
        self.breakStartupBtn.set_active(True)
        self.breakStartupBtn.connect("toggled", self.toggleStartup)
        self.breakStartupBtn.set_margin_left(10)
        self.startupBox.pack_start(self.breakStartupBtn, True, True, 0)
        
    def buildSaveChangesUI(self, tabGrid):
        #add ok, apply, cancel buttons
        self.saveChangesBox = Gtk.Box()
        self.saveChangesBox.set_orientation(Gtk.Orientation.HORIZONTAL)
        tabGrid.add(self.saveChangesBox)
        
        #OK Button
        self.timerOKBtn = Gtk.Button()
        self.timerOKBtn.set_label("OK")
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
        if(self.breakStartupBtn.get_active()):
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
        
    def updateTimer(self, name):
        newInterval = -1
        newIntervalName = ""
        if(name == "custom"):
            newInterval = self.breakCustomMinsBtn.get_value_as_int()
            newIntervalName = "custom"
            self.enableApplyCancelBtns()
        elif(name == "15mins"):
            newInterval = 15
            newIntervalName = "15mins"
            self.enableApplyCancelBtns()
        elif(name == "30mins"):
            newInterval = 30
            newIntervalName = "30mins"
            self.enableApplyCancelBtns()
        elif(name == "60mins"):
            newInterval = 60
            newIntervalName = "60mins"
            self.enableApplyCancelBtns()
            
        if(newInterval != -1):
            debugLog("Activate Break Timer every %d minutes" % (newInterval))
            self.tempConfig['interval'] = newInterval
            if(newIntervalName != ""):
                self.tempConfig['intervalName'] = newIntervalName
            
    def toggleBreaks(self, btn):        
        self.enableApplyCancelBtns()
        if(btn.get_active()):
            #enable breaks
            self.timerChoiceBox.set_sensitive(True)
            self.actionChoiceBox.set_sensitive(True)
            self.breakMessageSettingsFrame.set_sensitive(True)
            debugLog("Enable Breaks")
            self.tempConfig['enableBreaks'] = True
        else:
            #disable breaks
            self.timerChoiceBox.set_sensitive(False)
            self.actionChoiceBox.set_sensitive(False)
            self.breakMessageSettingsFrame.set_sensitive(False)
            debugLog("Disable Breaks")
            self.tempConfig['enableBreaks'] = False
        return True
            
    def changeBreakTimer(self, btn, name):
        state = 0
        if(btn.get_active()):
            state = 1
        if(name == "15mins"):
            if(state == 1):
                self.updateTimer("15mins")
        elif(name == "30mins"):
            if(state == 1):
                self.updateTimer("30mins")
        elif(name == "60mins"):
            if(state == 1):
                self.updateTimer("60mins")
        elif(name == "custom"):
            if(state == 1):
                self.breakCustomMinsBtn.set_sensitive(True)
                self.updateTimer("custom")
            else:
                self.breakCustomMinsBtn.set_sensitive(False)
        return True
                
    def updateCustomBreak(self, btn):
        self.updateTimer("custom")
        return True
    
    def updateBreakDuration(self, btn):
        newDuration = self.breakDurationBtn.get_value_as_int()
        debugLog("Break Duration =  %d mins" % (newDuration))
        self.tempConfig['duration'] = newDuration
        return True
        
    def updateBreakAction(self, btn, name):
        newAction = ""
        state = 0
        if(btn.get_active()):
            state = 1
            
        if(name == "breakToolTip"):
            if(state == 1):
                newAction = "tooltip"
                self.enableApplyCancelBtns()
        elif(name == "breakPopUp"):
            if(state == 1):
                newAction = "popup"
                self.enableApplyCancelBtns()
        elif(name == "breakDisableInp"):
            if(state == 1):
                newAction = "disableinp"
                self.enableApplyCancelBtns()
                
        if(newAction != ""):
            debugLog("Action changed = %s" % (newAction))
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
        self.exerImagePath = self.h.getExerImagePath()
        self.exerImage.set_from_file(self.exerImagePath)
        self.exerImageBtn = Gtk.Button()
        self.exerImageBtn.set_sensitive(False)
        self.exerImageBtn.add(self.exerImage)
        self.exerScrollWindow.add_with_viewport(self.exerImageBtn)
        
        #Break Settings Grid
        disclaimerStr = "Disclaimer: This tool does not provide medical advice.\nAlways consult your physician before beginning any exercise program." 
        self.disclaimerLabel = Gtk.Label(disclaimerStr)
        self.disclaimerLabel.modify_font(self.getFont("disclaimer"))
        self.setMargin(self.disclaimerLabel, "10 5 5 5")
        self.disclaimerFrame = Gtk.Frame()
        self.disclaimerFrame.set_border_width(5)
        self.disclaimerFrame.add(self.disclaimerLabel)
        self.setMargin(self.disclaimerFrame, "10 0 0 5")
        tabGrid.attach_next_to(self.disclaimerFrame, self.exerScrollWindow, Gtk.PositionType.BOTTOM, 1, 1)
        
    def saveSettings(self):
        #Extract current message in textBuffer to customBreakMsg
        if self.checkIfMessageUpdated():
            start, end = self.breakMsgTextBuffer.get_bounds()
            self.tempConfig['customBreakMsg'] = self.breakMsgTextBuffer.get_text(start, end, include_hidden_chars=True)
        
        #Save tempConfig to c
        self.c = self.tempConfig
        #Copy tempConfig to config and write it to config file
        self.h.updateConfig(self.tempConfig)
        #Load newConfig to the UI (redundant)
        self.loadConfigToUI()
        #Stop old timers and start new timers based on new config
        if('enableBreaks' in self.c and self.c['enableBreaks']):
            self.h.mainWindow.stopTimers()
            self.h.mainWindow.startTimers()
            debugLog("Breaks Enabled, so restarting timers")
        else:
            self.h.mainWindow.stopTimers()
            self.h.mainWindow.appInd.set_label("", "")
            debugLog("Breaks Disabled, canceling all timers")
        
        if('startup' in self.c and self.c['startup']):
            self.h.mainWindow.addAppToStartup()
        else:
            self.h.mainWindow.removeAppFromStartup()
            
        if('customBreakMsg' in self.c):
            self.h.mainWindow.setNewBreakMessage(self.c['customBreakMsg'])
        
    def saveChangesHandler(self, btn, name):
        if(name == "Ok"):
            debugLog("Ok Button")
            #Save settings if Apply button is enabled
            if(self.timerApplyBtn.get_sensitive() or self.checkIfMessageUpdated()):
                self.saveSettings()
                debugLog("Changes saved to file")
            #Hide the config dialog    
            self.h.hideOnClose()
        elif(name == "Apply"):
            debugLog("Apply Button")
            self.saveSettings()
            debugLog("Changes saved to file")
            self.disableApplyCancelBtns()
        elif(name == "Cancel"):
            debugLog("Cancel Button")
            #Restore tempConfig to c
            self.tempConfig = copy.deepcopy(self.c)
            self.h.hideOnClose()
        return True
    
    def checkIfMessageUpdated(self):
        start, end = self.breakMsgTextBuffer.get_bounds()
        currentMessage = self.breakMsgTextBuffer.get_text(start, end, include_hidden_chars=True)
        loadedMessage = self.tempConfig['customBreakMsg']
        return currentMessage != "" and currentMessage != loadedMessage
            
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
    def __init__(self, window, interval, action, breakMsg):
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
        
        self.breakMsg = breakMsg
        self.action = action
        self.isRunning = False
        
        self.isBreakMsgWindowDestroyed = True
        
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
        
    def setNewBreakMessage(self, breakMsg):
        self.breakMsg = breakMsg
        
    def showBreakMessageUI(self, action):
        #Destroy any previous break message windows
        self.destroyBreakMsgWindow()
            
        #Update Label Timer 
        self.timerStart = GLib.get_current_time()
        self.timerEnd = self.timerStart + self.interval
        
        #Show UI
        self.breakMessageWindow = Gtk.Window()
        self.isBreakMsgWindowDestroyed = False
        self.breakMessageWindow.set_resizable(False)
        self.breakMessageWindow.set_position(Gtk.WindowPosition.CENTER)
        self.breakMessageWindow.set_size_request(375, 100)
        
        self.breakBox = Gtk.Box()
        self.breakBox.set_orientation(Gtk.Orientation.VERTICAL)
        
        self.breakReminderText = self.breakMsg
        self.breakReminderLabel = Gtk.Label(self.breakReminderText)
        self.breakReminderLabel.modify_font(self.mainWindow.ui.getFont("heading"))
        
        self.breakActionBox = Gtk.Box()
        self.breakActionBox.set_margin_top(10)
        self.breakActionBox.set_orientation(Gtk.Orientation.HORIZONTAL)
        
        self.breakOkBtn = Gtk.Button()
        self.breakOkBtn.set_label("OK")
        self.breakOkBtn.modify_font(self.mainWindow.ui.getFont("heading"))
        self.breakOkBtn.set_size_request(60, 30)
        self.breakOkBtn.set_margin_left(140)
        self.breakOkBtn.connect("clicked", self.destroyBreakMsgWindow)
        
        self.exerciseBtnText = "Show me some Exercises"
        self.exerciseBtn = Gtk.Button()
        self.exerciseBtn.set_label(self.exerciseBtnText)
        self.exerciseBtn.set_margin_left(5)
        self.exerciseBtn.set_size_request(200, 30)
        self.exerciseBtn.modify_font(self.mainWindow.ui.getFont("heading"))
        self.exerciseBtn.connect("clicked", self.showExerciseTab)
        
        self.breakActionBox.pack_start(self.breakOkBtn, False, False, 0)
        self.breakActionBox.pack_start(self.exerciseBtn, False, False, 0)
        
        self.breakBox.pack_start(self.breakReminderLabel, True, True, 0)
        self.breakBox.pack_start(self.breakActionBox, False, False, 0)
        
        self.breakMessageWindow.add(self.breakBox)
        
        self.breakMessageWindow.set_title("Break My Work - Take a break")
        self.breakMessageWindow.set_border_width(15)
        self.breakMessageWindow.show_all()
        
        debugLog("Action = %s, Interval = %d" % (self.action, self.interval))
        
        return True
        
    def destroyBreakMsgWindow(self, widget = None):
        try:
            if(not self.isBreakMsgWindowDestroyed and isinstance(self.breakMessageWindow, Gtk.Window)):
                self.breakMessageWindow.destroy()
                self.isBreakMsgWindowDestroyed = True
        except AttributeError:
            #Do nothing (dummy)
            debugLog("self.breakMessageWindow does not exist")
        
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
            debugLog("Trying to update app label first time")
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
        debugLog("Inside UpdateAppLabel, currTime = %d, timerStart = %d, timerEnd = %d" % (self.currTime, self.timerStart, self.timerEnd))
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
        #load all config paths
        self.loadAllPaths()
        
        #Create Window UI
        self.window = Gtk.Window()
        self.window.set_resizable(False)
        self.window.set_title("Break My Work")
        
        #setup ui
        self.helper = Helper(self)
        
        #setup config
        self.config = self.loadConfig()
        debugLog("Loaded config = %s" % self.config)
        
        #setup ui
        self.ui = UI(self.helper, self.config)
        self.window.add(self.ui.getNoteBook())
        self.window.set_position(Gtk.WindowPosition.CENTER)
        
        #Build App Indicator
        self.buildAppIndicator()
        
        #Setup Timer
        self.breakScheduler = BreakScheduler(self, self.config['interval'], self.config['actionType'], self.config['customBreakMsg'])
        
        self.window.connect("delete-event", self.hideOnClose)
        if(self.config['firstRun']):
            self.window.show_all()
            self.config['firstRun'] = False
            self.writeNewConfigToFile()
            self.addAppToStartup()
        else:
            self.window.hide()
        
    def loadAllPaths(self):
        #Home Dir
        self.homeDir = expanduser("~")
        
        #Curr Dir
        self.currDir = os.getcwd()
        
        #Config dir
        self.configDir = self.homeDir + "/.breakmywork/config"
        self.configFilePath = self.configDir + "/breakmywork.pickle"
        
        #AutoStart Dirs 
        self.autoStartDestDir = self.homeDir + "/.config/autostart/"
        self.autoStartDestFilePath = self.autoStartDestDir + "break-my-work.desktop"
        
        #App Icon
        self.imageDir = "/usr/share/breakmywork/images"
        self.appIconName = "breakicon"
        self.appIconPath = self.imageDir + "/breakicon.png"
        
        #Exercise Image Path        
        self.exerImagePath = self.imageDir + "/deskStretches.jpg"
         
    def hideOnClose(self, widget=None, event=None):
        self.window.hide()
        return True
        
    def rightClickOnStatus(self, icon, button, time):
        self.configMenu.show_all()
        
    def showConfigureWindow(self, widget=None):
        self.window.show_all()
        
    def loadConfig(self):
        self.defaultBreakConfigMsg = "Please take a break of 2-5 mins, it will help you avoid RSI Injuries."
        self.defaultConfig = {'duration' : 2,
                              'interval' : 60,
                              'intervalName': '60mins',
                              'actionType' : 'popup',
                              'customBreakMsg' : self.defaultBreakConfigMsg,
                              'firstRun' : True,
                              'enableBreaks' : True,
                              'startup' : True}
        self.currConfig = None
        #Check if a config directory exists
        if(os.path.isdir(self.configDir)):
            if(os.path.isfile(self.configFilePath)):
                #Load existing config
                debugLog("Loaded existing config")
                try:
                    self.currConfig = pickle.load(open(self.configFilePath, "rb"))
                except IOError as e:
                    print "Exception error is : %s " % (e)
            else:
                #Create a new default config
                debugLog("Created a new default config file")
                self.currConfig = self.defaultConfig
                try:
                    pickle.dump(self.currConfig, open(self.configFilePath, "rb"))
                except IOError as e:
                    print "Exception error is : %s " % (e)
        else:
            #Created a new config directory and file
            self.currConfig = self.defaultConfig
            debugLog("Created a new config directory and file")
            os.makedirs(self.configDir)
            try:
                pickle.dump(self.currConfig, open(self.configFilePath, "wb"))
            except IOError as e:
                print "Exception error is : %s " % (e)
                
        return self.currConfig
    
    def writeNewConfigToFile(self):
        #Create the config directory if it does not exist
        if(not os.path.isdir(self.configDir)):
            os.makedirs(self.configDir)
            
        #Overwrite the config file
        debugLog("Overwrite Config File")
        try:
            pickle.dump(self.config, open(self.configFilePath, "wb"))
        except IOError as e:
            print "Exception error is : %s " % (e)
                
        return self.currConfig
        
    def buildAppIndicator(self):
        self.appInd = appindicator.Indicator.new("MyApp", "", appindicator.IndicatorCategory.APPLICATION_STATUS)
        self.appInd.set_status (appindicator.IndicatorStatus.ACTIVE)
        self.appIconDir = self.imageDir
        self.appInd.set_icon_theme_path(self.appIconDir);
        self.appInd.set_icon(self.appIconName)
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
        
    def cleanUp(self, widget):
        self.breakScheduler.stop()
        Gtk.main_quit()
        
    def showAboutDialog(self, widget):
        self.aboutDialog = Gtk.AboutDialog()

        self.aboutDialog.set_program_name("Break My Work")
        self.aboutDialog.set_version("1.3")
        self.aboutDialog.set_comments("Break My Work is a simple Repetitive Strain Injury Prevention Software.")
        self.aboutDialog.set_destroy_with_parent(True)
        self.logoIcon = GdkPixbuf.Pixbuf.new_from_file_at_size(self.appIconPath, 32, 32)
        self.aboutDialog.set_logo(self.logoIcon)
        self.webUrl = "http://www.ravikiranj.net"
        self.aboutDialog.set_website(self.webUrl)
        self.aboutDialog.set_authors(["Ravikiran Janardhana"])

        self.aboutDialog.run()
        self.aboutDialog.destroy()
        
    def updateAppIndicatorLabelInMins(self, mins):
        hours = int(mins / 60)
        minutes = mins % 60
        labelStr = " (" + str(hours).rjust(2, '0')+ ":" + str(minutes).rjust(2, '0') + ")"
        debugLog("Updated app label = %s" % (labelStr))
        self.appInd.set_status (appindicator.IndicatorStatus.ATTENTION)
        self.appInd.set_label(labelStr, "")

    def updateAppIndicatorLabelInSecs(self, secs):
        minutes = int(secs / 60)
        seconds = secs % 60
        labelStr = " (" + str(minutes).rjust(2, '0')+ ":" + str(seconds).rjust(2, '0') + ")"
        debugLog("Updated app label = %s" % (labelStr))
        self.appInd.set_status (appindicator.IndicatorStatus.ATTENTION)
        self.appInd.set_label(labelStr, "")
        
    def stopTimers(self):    
        self.breakScheduler.stop()
        
    def startTimers(self):
        self.breakScheduler.setNewInterval(self.config['interval'])
        
    def addAppToStartup(self):
        self.desktopFileStr = """
[Desktop Entry]
Type=Application
Exec=breakmywork
Hidden=false
NoDisplay=false
X-GNOME-Autostart-enabled=true
Name[en_US]=Break My Work
Name=Break My Work
Comment[en_US]=Break My Work is an RSI Prevention Software
Comment=Break My Work is an RSI Prevention Software
"""
        try:
            self.autoStartFileHandle = open(self.autoStartDestFilePath, "w")
            self.autoStartFileHandle.write(self.desktopFileStr)
            self.autoStartFileHandle.close()
        except IOError as e:
            print "Exception error is : %s " % (e)
            
    def removeAppFromStartup(self):
        try:
            if(os.path.isfile(self.autoStartDestFilePath)):
                os.remove(self.autoStartDestFilePath)
        except IOError as e:
            print "Exception error is : %s " % (e)
            
    def setNewBreakMessage(self, breakMsg):
        self.breakScheduler.setNewBreakMessage(breakMsg)
        
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
        
    def getExerImagePath(self):
        return self.mainWindow.exerImagePath
#end class Helper

if __name__ == "__main__":
    mainWindow = MainWindowBuilder()
    mainWindow.main()