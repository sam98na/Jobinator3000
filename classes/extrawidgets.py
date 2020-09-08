from tkinter import *
from time import *
import pandas as pd
import random

class ClockWidget(Label):

    """
    Implements updating clock functionality
    """

    def __init__(self, master):
        Label.__init__(self, master)
        self.after(200, self.tick)

    def tick(self):
        string = strftime('The day is %A, %B %d, %Y.' +  "\n"  + 'It is currently %I:%M:%S %p')
        self.config(text = string)
        self.after(500, self.tick)

class RandomCompanyWidget(Label):
    """
    Implements widget that displays a random company (and the date applied to that
    company) every 5 seconds.
    """
    def __init__(self, master, dataframe):
        Label.__init__(self, master)
        self.df = dataframe
        self.randomindex = random.randint(0, self.df.maxindex())
        text = self.df.getrow(self.randomindex, 0, 2)
        self.config(text = "Some companies you've applied to: \n" + text[0] + ": " + text[1])
        self.after(5000, self.tick)

    def tick(self):
        self.randomindex = random.randint(0, self.df.maxindex())
        text = self.df.getrow(self.randomindex, 0, 2)
        self.config(text = "Some companies you've applied to: \n" + text[0] + ": " + text[1])
        self.after(5000, self.tick)

class ListLastJobs(Label):
    """
    Implements updating widget that lists the last 5 jobs applied to.
    """
    def __init__(self, master, dataframe):
        Label.__init__(self, master)
        self.df = dataframe
        basisText = "Last Five Jobs You've Applied To:"
        for i in range(max(self.df.maxindex()-4, 0), self.df.maxindex()+1):
            row = self.df.getrow(i, 0, 3)
            basisText += "\nDate: " + row[0] + " // Name: " + row[1] + " // Status: " + row[2]
        self.config(text = basisText)

    def updateText(self):
        basisText = "Last Five Jobs You've Applied To:"
        for i in range(max(self.df.maxindex()-4, 0), self.df.maxindex()+1):
            row = self.df.getrow(i, 0, 3)
            basisText += "\nDate: " + row[0] + " // Name: " + row[1] + " // Status: " + row[2]
        self.config(text = basisText)


class JobDataFrameObject():
    """
    Implements dataframe object for data access. Stores all companies applied to, along with application status
    (U for unknown, R for rejected, and A for accepted) and date applied.
    """
    def __init__(self, address):
        self.address = address
        self.df = pd.read_csv(self.address, delimiter=":", header=0)

    def addnew(self, companyname):
        """ Adds new company (alongside date and status) to dataframe """
        self.df = self.df.append(pd.Series([strftime("%m/%d"), companyname, "U"], index = self.df.columns), ignore_index = True)

    def getcompany(self, companyname):
        """ Fetches most recent entry of a company name from the dataframe, return None if not in dataframe """
        try:
            found = self.df[self.df["Company"] == companyname]
            print(found.index.max())
            return found.iloc[-1]
        except:
            return None

    def createbackup(self, backupaddress):
        """ Creates/updates backup data csv at backupaddress """
        self.df.to_csv(backupaddress, sep=":", index = False)

    def exitprotocol(self):
        """ Saves edited/unedited dataframe back to original csv file location """
        self.df.to_csv(self.address, sep=":", index = False)

    def maxindex(self):
        """ Returns max index of dataframe """
        return self.df.index.max()

    def getrow(self, index, startcol, endcol):
        """ Returns row of dataframe with specific columns using iloc """
        return self.df.iloc[index, startcol:endcol]

    #########################
    """ TESTING FUNCTIONS """
    #########################

    def findTest(self):
        """ Prints out the outcome of trying to find a company in the dataframe """
        return self.df[self.df["Company"] == "Revature"]

    def deletelast(self):
        """ TEST FUNCTION: deletes last row of dataframe """
        self.df.drop(self.df.tail(1).index,inplace=True)
