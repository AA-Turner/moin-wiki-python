#!/usr/bin/python

from Tkinter import *	


def Callme():
    print 'hi'              
    print 'doggy dog'    

def SecondFunction():
    label = Label(root, text = 'jimmy poo', fg = 'blue')
    label.pack()

    

root = Tk()				

bobby = Button(root, text = 'Press', command = Callme , fg = 'white', bg = 'black')
bobby.pack()

jimmy = Button(root, command = SecondFunction, text = 'I am jimmy')
jimmy.pack()

	
root.mainloop()			

