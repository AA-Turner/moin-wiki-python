#A doodle that tells the user what version of Windows they are using, the version, CSD level, and processor configuration.  It gives the
#win32_ver function of the platform module a nice output engine.

from platform import win32_ver

SystemInformation = win32_ver(release='', version='', csd='', ptype='')
print 'Opperating System: Microsoft Windows', SystemInformation[0]
print 'Version:', SystemInformation[1]
print 'CSD:', SystemInformation[2]
print 'Processor Configuration:', SystemInformation[3]
print
raw_input('Press Enter to quit. ')