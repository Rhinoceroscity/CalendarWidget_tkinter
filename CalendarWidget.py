import tkinter as tk
from tkinter import ttk
import time

class CalendarWidget():
    def __init__(self, startTime):
        #Abbreviations for the days as they will be displayed at the top of the frame
        self.dayAbbreviations = ("Mo","Tu","We","Th","Fr","Sa","Su")
        
        #In case you want a calendar with Sunday first, or Wednesday, for some reason
        #You can reorder them here
        self.dayPositions = {
        "Monday" : 1,
        "Tuesday" : 2,
        "Wednesday" : 3,
        "Thursday" : 4,
        "Friday" : 5,
        "Saturday" : 6,
        "Sunday" : 7,
        }
        
        #Create the window as a toplevel instead of a root window so it'll work in any project
        self.calendarWindow = tk.Toplevel()
        self.calendarWindow.wm_resizable(0,0)
        self.calendarWindow.title("Select Date")
        self.calendarWindow.config(padx = 5, pady = 5)
        self.calendarWindow.rowconfigure(0, weight=1)

       # self.calendarFrame = tk.LabelFrame()
        #self.calendarFrame.destroy()
        
        buttonsFrame = tk.Frame(self.calendarWindow)
        buttonsFrame.pack(side=tk.TOP, fill=tk.X, expand=1)
        
        #Create the previous and next buttons
        tk.Button(buttonsFrame, text = "< Prev", command = self.previousMonth).pack(side=tk.LEFT)
        tk.Button(buttonsFrame, text = "Next >", command = self.nextMonth).pack(side=tk.RIGHT)
        
        #Initialize a calendar originating in your current month.
        self.initializeCalendarUI(round(startTime))
        
    
    def initializeCalendarUI(self, startTime):
        #find the first day of the month
        dayNum = int(time.strftime("%d", time.localtime(startTime)))
        self.currentTime = startTime - (dayNum * 86400) + 86400
        print(time.strftime("%d %B %A", time.localtime(self.currentTime)))
        
        #Next find the month we're in, and then find the amount of days
        #I have the program do this procedurally so we don't have to rely on extra libraries or dictionaries of any sort
        self.currentMonth = time.strftime("%m",time.localtime(self.currentTime))
        #We start at index 27, since no month is shorter than 28 days ever.
        monthLength=27
        for i in range(5):
            _t = self.currentTime + (86400*(i+27))
            print(time.strftime("%B", time.localtime(_t)))
            if time.strftime("%m", time.localtime(_t))!=self.currentMonth:
                print(monthLength)
                break
            monthLength+=1
            
        #Now that we have the starting day and the length of the month, we can generate the calendar properly
        #Destroy any calendar frames that exist.
        try:
            if (self.calendarFrame.winfo_exists()==True):
                self.calendarFrame.destroy()
        except Exception:
            print("Ignoring " + str(Exception) + ", first time calendarFrame is being created")
        
        self.calendarFrame = tk.LabelFrame(self.calendarWindow, text = time.strftime("%B %Y", time.localtime(self.currentTime)))
        self.calendarFrame.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        
        #Generate the initial abbreviation labels at the top of the frame
        for index, i in enumerate(self.dayAbbreviations):
            _t = tk.Frame(self.calendarFrame)
            _t.grid(column=index+1, row=0)
            tk.Label(_t, text = i).grid(column=1, row=1)
        
        #Define the return function that will be used in a moment
        #This returns a seconds time since the epoch that can
        #Be converted into strings with the time module
        def buttonFunction(returnTime):
            return_time = self.currentTime + (86400*returnTime)
            print(return_time)
            print(time.strftime("%A %d %B %Y", time.localtime(return_time)))
            self.calendarWindow.destroy()
        
        #Create all the buttons
        row=1
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

    #Move to the next month by scanning forwards for a new month
    def nextMonth(self):
        for i in range (32):
            _c = time.strftime("%m", time.localtime(self.currentTime + (86400*i)))
            if _c!=self.currentMonth:
                self.currentTime += 86400*i
                self.initializeCalendarUI(self.currentTime)
                break
    
    #Move to the previous month by scanning forwards for a new month
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
