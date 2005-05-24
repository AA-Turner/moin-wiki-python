from math import hypot 

print "HypotIO - Written by JAM in Python 2.4.1"
print
print "What is the value of x?"
x = float(raw_input())
print
print "What is the value of y?"
y = float(raw_input())
print
print "The value of z is:"
print hypot(x, y)
print
print "Press Enter to quit."
raw_input()