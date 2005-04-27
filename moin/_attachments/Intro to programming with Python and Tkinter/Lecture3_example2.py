#!/usr/bin/python

from Tkinter import *           #Importing the library (tool box)



root = Tk()                     #Creating a background window

li = ['Carl','Patrick','Lindsay','Helmut','Chris','Gwen']
                                #Creating a list

movie = ['God Father','Beauty and the Beast','Brave heart']

listb = Listbox(root)           # Creating a listbox widget
listb2 = Listbox(root)

for item in li:                 # Insert each item inside li into the listb
    listb.insert(0,item)
for item in movie:
    listb2.insert(0,item)

listb.pack()                    # Pack listb into the main window
listb2.pack()

root.mainloop()                 # Go into the loopback
