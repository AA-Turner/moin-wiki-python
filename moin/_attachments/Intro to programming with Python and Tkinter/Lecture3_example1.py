#!/usr/bin/python

from Tkinter import *           #Importing the library (tool box)



root = Tk()                     #Creating a background window

li = ['Carl','Patrick','Lindsay','Helmut','Chris','Gwen']
                                #Creating a list


listb = Listbox(root)           # Creating a listbox widget

for item in li:                 # Insert each item inside li into the listb
    listb.insert(0,item)

listb.pack()                    # Pack listb into the main window

root.mainloop()                 # Go into the loopback
