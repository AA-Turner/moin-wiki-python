#!/usr/bin/env python
# See http://www.mplayerhq.hu/DOCS/tech/slave.txt
# and mplayer -input cmdlist
#from qt import *
from PyQt4.QtCore import pyqtProperty, pyqtSignature, Qt, QSize, QTimer, SIGNAL
from PyQt4.QtGui import qApp, QWidget
import commands, popen2, atexit


class Process:

    CMD = ("mplayer -slave -quiet -noconsolecontrols -nomouseinput "
           "-vo %(VO)s -ao %(AO)s -wid %(WID)s %(FILENAME)r")
    
    CFG = dict(
        AO = "alsa",
        VO = "xv" #VO = "x11"
    )
    
    def __init__(self, winId, filename = ""):
    
        self.CFG["WID"] = winId
        self.CFG["FILENAME"] = filename
        self.process_in = None
        self.process_out = None
        self.running = False
    
    def run(self):
    
        if self.CFG["FILENAME"]:
            self.process_out, self.process_in = popen2.popen2(self.CMD % self.CFG, 1)
            self.running = True
    
    def setFileName(self, filename):
    
        self.CFG["FILENAME"] = filename
    
    def __del__(self):
    
        self.command("pause")
        self.command("quit")
        if self.process_in:
            self.process_in.close()
            self.process_in = None
        if self.process_out:
            self.process_out.close()
            self.process_out = None
    
    def command(self, cmd, args = (), result_prefix = "", result_type = None):
    
        if not self.running:
            if result_type:
                return result_type()
            else:
                return
        
        if args:
            args = map(lambda arg: str(arg), args)
            self.process_in.write("\n%s %s\n" % (cmd, " ".join(args)))
        else:
            self.process_in.write("\n%s\n" % cmd)
        
        if result_type != None:
            line = self.process_out.readline()
            value = line.lstrip(result_prefix).rstrip()
            try:
                return result_type(value)
            except ValueError:
                return result_type()


class MPlayerWidget(QWidget):

    __pyqtSignals__ = ("muteChanged(bool)", "playing(bool)", "paused(bool)",
                       "fullScreenChanged(bool)", "percentPosition(int)",
                       "timePosition(int)", "volumeChanged(int)")
    
    def __init__(self, parent = None):
    
        QWidget.__init__(self, parent)
        self.timer = QTimer()
        self.connect(self.timer, SIGNAL("timeout()"), self.updateTime)
        self._process = Process(self.winId())
        self._path = u""
        self._playing = False
        self._paused = False
        self._fullscreen = False
        self._muted = False
        self._volume = 0
        self._default_volume = 10
    
    def sizeHint(self):
        return QSize(100, 100)
    
    def osd(self, msg):
        self._process.command("osd_show_text", msg)
    
    def updateTime(self):
    
        percentage = self._process.command("get_percent_pos", (), "ANS_PERCENT_POSITION=", int)
        self.emit(SIGNAL("percentPosition(int)"), percentage)
        seconds = int(percentage/100.0 * self.getLength())
        self.emit(SIGNAL("timePosition(int)"), seconds)
    
    @pyqtSignature("load(QString)")
    def load(self, url):
        self.setFileName(url)
    
    def fileName(self):
        return self._path
    
    def setFileName(self, url):
    
        url = str(url)
        self._process.setFileName(url)
        self._path = url
    
    fileName = pyqtProperty("QString", fileName, setFileName)
    
    @pyqtSignature("play()")
    def play(self):
        if self._process.running:
            return
        
        self.setAttribute(Qt.WA_NoSystemBackground)
        self._process.run()
        
        self._playing = True
        self.emit(SIGNAL("playing(bool)"), True)
        self.setVolume(self._default_volume)
        self.setPaused(False)
        self.update()
    
    @pyqtSignature("stop()")
    def stop(self):
        
        if not self._process.running:
            return
        
        self._playing = False
        self.setPaused(False)
        self.emit(SIGNAL("playing(bool)"), False)
        
        self._process = Process(self.winId(), self._path)
        self.setAttribute(Qt.WA_NoSystemBackground, False)
    
    def isPlaying(self):
        return self._playing
    
    def setPlaying(self, enable):
    
        if not self._process.running:
            return
        
        if self._playing != enable:
            if enable:
                self.play()
            else:
                self.stop()
    
    playing = pyqtProperty("bool", isPlaying, setPlaying)
    
    def isMuted(self):
        return self._muted
    
    @pyqtSignature("setMuted(bool)")
    def setMuted(self, enable):
    
        if not self._process.running:
            return
        
        if enable != self._muted:
            self._process.command("mute")
            self._muted = enable
            self.emit(SIGNAL("muteChanged(bool)"), enable)
    
    muted = pyqtProperty("bool", isMuted, setMuted)
    
    def isPaused(self):
        return self._paused
    
    @pyqtSignature("setPaused(bool)")
    def setPaused(self, enable):
    
        if not self._process.running:
            return
        
        if not enable and self._playing:
            self.timer.start(100)
        else:
            self.timer.stop()
        
        if enable != self._paused:
            self._process.command("pause")
            self._paused = enable
            self.emit(SIGNAL("paused(bool)"), enable)

    paused = pyqtProperty("bool", isPaused, setPaused)

    def isFullScreen(self):
        return self._fullscreen
    
    @pyqtSignature("setFullScreen(bool)")
    def setFullScreen(self, enable):
    
        if not self._process.running:
            return
        
        if enable != self._fullscreen:
            self._process.command("vo_fullscreen")
            self._fullscreen = enable
            self.emit(SIGNAL("fullScreenChanged(bool)"), enable)
    
    fullScreen = pyqtProperty("bool", isFullScreen, setFullScreen)
    
    def getLength(self):
    
        if not self._process.running:
            return -1
        else:
            return self._process.command("get_time_length", (), "ANS_LENGTH=", int)
    
    def getVolume(self):
    
        return self._volume
    
    @pyqtSignature("setVolume(int)")
    def setVolume(self, value):
    
        volume = max(0, min(value, 100))
        if volume != self._volume:
            self.emit(SIGNAL("volumeChanged(int)"), volume)
        self._volume = volume
        self._process.command("volume", (self._volume, 1))
    
    volume = pyqtProperty("int", getVolume, setVolume)
