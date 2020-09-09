from tkinter import *
from time import *
from classes.extrawidgets import *

backupLocation = "backupdata/backup.csv"
df = JobDataFrameObject("data/data.csv")

class InputNewJob:
    """
    Class to implement functionality for the input new job window
    """
    def __init__(self, master):
        global df
        self.top = top = Toplevel(master)

        self.text = Label(top, text="Please enter company name here")
        self.text.grid(row=0, pady = 10, padx=10)

        self.entry = Entry(top)
        self.entry.grid(row=1, pady=10, padx=10)
        self.entry.focus()

        self.confirm = Button(top, text="OK", command = self.quit)
        self.confirm.grid(row=3, pady=10, padx=10)

        windowWidth = top.winfo_reqwidth()
        windowHeight = top.winfo_reqheight()
        positionRight = int(top.winfo_screenwidth()/2 - windowWidth/2)
        positionDown = int(top.winfo_screenheight()/2 - windowHeight/2)
        top.geometry("+{}+{}".format(positionRight, positionDown))

    def quit(self):
        df.addnew(self.entry.get())
        self.top.destroy()

class UpdateJob:
    """
    Class to implement functionality for the update job window
    """
    def __init__(self, master):
        global df
        self.top = top = Toplevel(master)

        self.text = Label(top, text="Company Name")
        self.text.grid(row=0, pady = 10, padx=10)

        self.entry = Entry(top)
        self.entry.grid(row=1, pady=10, padx=10)
        self.entry.focus()

        self.confirm = Button(top, text="OK", command = self.quit)
        self.confirm.grid(row=3, pady=10, padx=10)

        windowWidth = top.winfo_reqwidth()
        windowHeight = top.winfo_reqheight()
        positionRight = int(top.winfo_screenwidth()/2 - windowWidth/2)
        positionDown = int(top.winfo_screenheight()/2 - windowHeight/2)
        top.geometry("+{}+{}".format(positionRight, positionDown))

    def quit(self):
        df.addnew(self.entry.get())
        self.top.destroy()

class CheckJob:
    """
    Class to implement functionality for the checking job/company window
    """
    def __init__(self, master):
        global df
        self.top = top = Toplevel(master)

        self.text = Label(top, text="Enter Company Name")
        self.text.grid(row=0, pady = 10, padx=10)

        self.entry = Entry(top)
        self.entry.grid(row=1, pady=10, padx=10)
        self.entry.focus()

        self.confirm = Button(top, text="OK", command = self.check)
        self.confirm.grid(row=3, pady=10, padx=10)

        self.results = Label(top, text = "Enter Company Name then Press OK")
        self.results.grid(row=4, pady = 10, padx = 10)

        windowWidth = top.winfo_reqwidth()
        windowHeight = top.winfo_reqheight()
        positionRight = int(top.winfo_screenwidth()/2 - windowWidth/2)
        positionDown = int(top.winfo_screenheight()/2 - windowHeight/2)
        top.geometry("+{}+{}".format(positionRight, positionDown))

    def check(self):
        result = df.getcompany(self.entry.get())
        try:
            self.results.config(text = "Date applied: " + result[0] + " \n Company Name: " + result[1] + " \n Status: " + result[2])
        except:
            self.results.config(text = "Company not in database")


class App:
    def __init__(self, master):
        global df
        self.master = master

        # Welcome Text #
        self.prompt = Label(master, text="the jobinator 3000", font = ("Comic Sans", 20))
        self.prompt.grid(row=0, column=0, pady=20, padx = 30)

        # Clock #
        self.clock = ClockWidget(master)
        self.clock.grid(row=1,column=0, pady=10)

        # Random Company Text Widget #
        self.company = RandomCompanyWidget(master, df)
        self.company.grid(row=2 ,column=0, pady=10)

        # Last Five Companies Text Widget #
        self.lastFive = ListLastJobs(master, df)
        self.lastFive.grid(row=3, column = 0, pady=10, padx=10)

        # New Entry Button #
        self.newEntry = Button(master, text="New Job Entry", command= self.newJobPopup)
        self.newEntry.grid(row=0, column=1, padx=20, pady=20)

        # Check Previous Entry Button #
        self.checkEntry = Button(master, text = "Check Company", command = self.checkCompanyPopup)
        self.checkEntry.grid(row=1, column=1, padx=20, pady=20)

        # Update Previous Entry Button #
        self.updateEntry = Button(master, text="Update Previous Entry")
        self.updateEntry.grid(row=2, column=1, padx=20, pady=20)

        #TESTING BUTTON: DELETE LAST ROW OF DATAFRAME#
        #self.deleteTest = Button(master, text="TEST: Delete last row of dataframe", command = df.deletelast)
        #self.deleteTest.grid(row = 3, column=1, padx=20, pady=20)

        # Create backup csv #
        self.backup = Button(master, text = "Backup Data File", command = df.createbackup(backupLocation))
        self.backup.grid(row = 3, column = 1, padx = 20, pady=20)


    def newJobPopup(self):
        """
        Implements functionality for the "adding new company" popup window
        """
        self.w = InputNewJob(self.master)
        self.newEntry["state"] = "disabled"
        self.master.wait_window(self.w.top)
        self.newEntry["state"] = "normal"
        self.lastFive.updateText()

    def checkCompanyPopup(self):
        """
        Implements functionality for the "checking company status" popup window
        """
        self.w = CheckJob(self.master)
        self.checkEntry["state"] = "disabled"
        self.master.wait_window(self.w.top)
        self.checkEntry["state"] = "normal"

    def updatePopup(self):
        """
        Implements functionality for the "updating company status" popup window
        """
        self.w = InputNewJob(self.master)
        self.newEntry["state"] = "disabled"
        self.master.wait_window(self.w.top)
        self.newEntry["state"] = "normal"
        self.lastFive.updateText()



### MAIN FUNCTION ###
if __name__ == "__main__":
    root = Tk()

    def disable_event():
        df.exitprotocol()
        root.destroy()

    ### Centering window on screen code (Taken from Yagisanatode) ###
    windowWidth = root.winfo_reqwidth()
    windowHeight = root.winfo_reqheight()
    positionRight = int(root.winfo_screenwidth()/2 - windowWidth/2) - 175
    positionDown = int(root.winfo_screenheight()/2 - windowHeight/2) - 40
    root.geometry("+{}+{}".format(positionRight, positionDown))

    app = App(root)
    root.protocol("WM_DELETE_WINDOW", disable_event)

    root.mainloop()
