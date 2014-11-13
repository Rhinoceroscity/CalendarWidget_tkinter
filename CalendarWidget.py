import tkinter as tk
from tkinter import ttk
import time

class CalendarWidget():
    def __init__(self, startTime):
        self.dayAbbreviations = (
        "Mo","Tu","We","Th","Fr","Sa","Su")
        
        self.dayPositions = {
        "Monday" : 1,
        "Tuesday" : 2,
        "Wednesday" : 3,
        "Thursday" : 4,
        "Friday" : 5,
        "Saturday" : 6,
        "Sunday" : 7,
        }
        
        self.calendarWindow = tk.Toplevel()
        self.calendarWindow.wm_resizable(0,0)
        self.calendarWindow.title("Select Date")
        self.calendarWindow.config(padx = 5, pady = 5)
        self.calendarWindow.rowconfigure(0, weight=1)
        
        self.calendarFrame = tk.LabelFrame()
        self.calendarFrame.destroy()
        
        buttonsFrame = tk.Frame(self.calendarWindow)
        buttonsFrame.pack(side=tk.TOP, fill=tk.X, expand=1)
        
        tk.Button(buttonsFrame, text = "< Prev", command = self.previousMonth).pack(side=tk.LEFT)
        tk.Button(buttonsFrame, text = "Next >", command = self.nextMonth).pack(side=tk.RIGHT)
        
        self.initializeCalendarUI(round(startTime))
        
    
    def initializeCalendarUI(self, startTime):
                #find the first day of the month
        dayNum = int(time.strftime("%d", time.localtime(startTime)))
        self.currentTime = startTime - (dayNum * 86400) + 86400
        print(time.strftime("%d %B %A", time.localtime(self.currentTime)))
        
        #Next find the month we're in, and then find the amount of days
        #I have the program do this procedurally so we don't have to rely on extra libraries or dictionaries of any sort
        self.currentMonth = time.strftime("%m",time.localtime(self.currentTime))
        monthLength=0
        for i in range(32):
            _t = self.currentTime + (86400*i)
            print(time.strftime("%B", time.localtime(_t)))
            if time.strftime("%m", time.localtime(_t))!=self.currentMonth:
                print(monthLength)
                break
            monthLength+=1
        #Now that we have the starting day and the length of the month, we can generate the calendar properly
        if (self.calendarFrame.winfo_exists()==True):
            self.calendarFrame.destroy()
        self.calendarFrame = tk.LabelFrame(self.calendarWindow, text = time.strftime("%B %Y", time.localtime(self.currentTime)))
        self.calendarFrame.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        
        #Generate the initial abbreviation labels at the top of the frame
        index=1
        for i in self.dayAbbreviations:
            _t = tk.Frame(self.calendarFrame)
            _t.grid(column=index, row=0)
            tk.Label(_t, text = i).grid(column=1, row=1)
            index+=1
        
        row=1
        
        def buttonFunction(returnTime):
            print(self.currentTime + (86400*i))
            self.calendarWindow.destroy()
        
        for i in range(monthLength):
            _d = time.localtime(self.currentTime + (86400*i))
            _day = time.strftime("%A",_d)
            
            #_f = tk.Frame(self.calendarFrame)
            #_f.grid(column = dayPositions[_day], row=row, sticky=tk.N+tk.E+tk.W+tk.S)
            
            tk.Button(self.calendarFrame, text = (i+1), command = lambda i=i: buttonFunction(i)).grid(column = self.dayPositions[_day], row=row, sticky=tk.N+tk.E+tk.W+tk.S)
            if self.dayPositions[_day]==7:
                row+=1
        
        for i in range(7):
            self.calendarFrame.columnconfigure(i+1, weight=1)
        for i in range(5):
            self.calendarFrame.rowconfigure(i+1, weight=1)

    def nextMonth(self):
        for i in range (32):
            _c = time.strftime("%m", time.localtime(self.currentTime + (86400*i)))
            if _c!=self.currentMonth:
                self.currentTime += 86400*i
                self.initializeCalendarUI(self.currentTime)
                break
    
    def previousMonth(self):
        for i in range (32):
            _c = time.strftime("%m", time.localtime(self.currentTime - (86400*i)))
            if _c!=self.currentMonth:
                self.currentTime -= 86400*i
                self.initializeCalendarUI(self.currentTime)
                break

class GUI():
    def __init__(self):
        self.root = tk.Tk()
        tk.Button(self.root, text = "Show Calendar", command = lambda: CalendarWidget(time.time())).pack(side=tk.TOP)
        #CalendarWidget(time.time())

new = GUI()
new.root.mainloop()
