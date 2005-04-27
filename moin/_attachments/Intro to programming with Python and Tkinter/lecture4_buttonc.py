#!/usr/bin/python               
                            #Souce section   1

#mandatory for unix and linux
#---------------------------------------------------------------

from Tkinter import *       #This library give us windows and buttons
from random import *        #This library allows us to generate random numbers
                            #import library section   2

#
#What not to use??? 
#---------------------------------------------------------------

def one_to_ten():
    ran = uniform(1,10)
    print ran
    
def GoWork():           # def starts a function, or define a function
    sum = 3*5 
    print sum               #Function section   3 
	
#----------------------------------------------------------------


	
                            #Code section    4
    
window = Tk()      #i am the parent, button = child

stacy = Button(window, text = 'yoyo', command = one_to_ten)  
#A rose with any other name would be just as sweet


stacy.pack()        #you can name it after your fish (ignored)
window.mainloop()         #youcan use your fish's name 

