# Chuck Fox  cfox04 at gmail dot com
# Date: 23/03/2005 PyCon code sample
#
# Description:
#    This module contains code for a very simple IPC mechanism that allows for pickled Python
# objects to be passed between different processes using UNIX domain sockets.  The intent of
# this file is to have the ability to send status information objects from a child process
# up to its parent which is listening for updates.  However, this mechanism should be 
# generic enough to allow for passing of objects between any 2 programs as long as they
# can connect on a UNIX socket.  We are keeping the interface limited to UNIX sockets
# on purpose for security purposes here, this is generally not a safe method of network
# communication.

# Update: Improve the socket-level performanance by moving the depickling code to the actual
# poll method.  This requires shorter lock holds and means the socket code needs to do less... a good thing

import os, socket, sys, string, time, cPickle, threading

class ObjectSender:
  """ This class is responsible for pickling and sending (via a socket) an object to another process
  listening on a UNIX socket. Once instantiated this object can be used to send multiple objects across.
  Internally the object uses a UNIX domain socket that will establish a new connection with the server
  for each object we send across.  This class is the "client" side of the equation; please see RecvObject
  for the "server" side """ 
  
  def __init__ (self, sockName, sockTimeout = 30):
    """ Args:
         sockName: Name of the UNIX socket to connect to (this is a string and the socket should be open)
         sockTimeout: Timeout in seconds on socket operations, prevents us from blocking forever... """
    self.sockName = sockName
    self.sockTimeout = sockTimeout
  
  def sendObj (self, object, retries = 10):
    # This is where we actually pickle and ship out 'object' across the socket:
    # Returns: codes based on success/failure
    pickledObj = cPickle.dumps (object, cPickle.HIGHEST_PROTOCOL)
    
    # now send it across a newly opened socket:
    for II in range (0, retries):
      try:
        sock = socket.socket (socket.AF_UNIX)
        sock.settimeout (self.sockTimeout)
        sock.connect (self.sockName)
        sock.sendall (pickledObj)
        sock.shutdown (2) # REALLY shutdown mr. connection here 
        sock.close ()
        return ()
      except Exception, err:
       print "Error received: ", err
       # if we have exceeded max retries OR if the error code is not 146 (meaning "Connection Refused") we pass this error up the line
       if II == retries - 1 or (err [0] != 146):
         raise
       else:
         time.sleep (float (II + 1) / 10)  # a linearly increasing backoff delay for retries on the socket
    
class ObjectReceiver (threading.Thread):
  """ ObjectReceiver is the 'server' counterpart to ObjectSender.  It binds to a named UNIX socket and listens for incoming
  connections from ObjectSender.  Once a connection is completed it takes all the data send and attempts to depickle it to a Python
  object.  If this succeeds ObjectReceiver then places the object in an internal list that may be grabbed by the calling program.  Once
  the calling program has grabbed the list, it is cleared out and we wait for more objects to come in from other processes. 
    With the optional maxCachedObjects constructor arg, the internal object cache can be setup to only hold a certain number of objects
  In the event of too many objects in the queue, additional objects sent across the wire will not be added to the queue. """
  def __init__ (self, sockName, socketTimeout = 30, sockBuffSize = 4096, maxCachedObjects = None):
    """ New ObjectReceivers are setup to bind to a sockName and wait for incoming 
    connections from other processes.
    Args:
      sockName: string name of the socket to bind to, must be available and clients will use the same name
      socketTimeout: This is the timeout for all socket operations to prevent hanging 
      sockBuffSize: Size of the receive buffer in bytes of the listening socket
      maxCachedObjects: The max number of objects we keep on hand between poll requests that grab the buffer, None means no limit to the list size """
    threading.Thread.__init__ (self)
    self.sockName = sockName
    self.sockBuffSize = sockBuffSize
    self.sock = socket.socket (socket.AF_UNIX)
    self.socketTimeout  = socketTimeout
    self.maxCachedObjects  = maxCachedObjects
    self.objCache = [] 
    self.pollLock = threading.Lock ()
    self.objEvent = threading.Event () # we use this event to allow for blocking when objCache is empty
    self.setDaemon (True)  # this is a daemon thread that will close with the rest of the process
 
  def run (self):
    # Bind and the socket and start listening
    self.sock.bind (self.sockName)
    self.sock.listen (5)
    while True:
      conn, addr = self.sock.accept ()
     
      # set conn's timeout to prevent hanging on bad behaviour
      conn.settimeout (self.socketTimeout)
   
      # now receive data & depickle it, we rely on the client to close out its
      # connection to get out of the following loop.  If that does not occur our conn socket
      # will timeout as well
      data = ""
      try:
        while True:
          next_data = conn.recv (self.sockBuffSize)
          if not next_data:
            conn.shutdown (2)
            conn.close ()
            break
          data += next_data
      except Exception, err:
        # most likely a timeout exception, ignore any data that came in
        continue 
 
      # if the existing objCache is allowed to have another member, try adding one:
      if (not self.maxCachedObjects) or (len (self.objCache) < self.maxCachedObjects):
        self.pollLock.acquire ()
        self.objCache.append (data)
        self.objEvent.set ()  # we have at least 1 item in the queue anybody waiting for a new object may fire 
        self.pollLock.release ()
 
  def poll (self): 
    """ This method is designed to return the contents of the objCache to the calling process. It is a (mostly) non-blocking poll, the
    only block is on the lock that keeps the contents of objCache trhead-safe.  The returned list consists of python objects that the
    calling process may use as it sees fit.  UPDATE: In the new version the actual depickling takes place in this method now """ 
    self.pollLock.acquire ()
    dataList = self.objCache
    self.objCache = []
    self.objEvent.clear () # no objects left in the queue, wait for more
    self.pollLock.release ()
    for II in range (0, len (dataList)):
      dataList [II] = cPickle.loads (dataList [II])
    return (dataList)
    

  def wait (self, timeout = None):
    self.objEvent.wait (timeout)
    # fell through timeout or got woken up, attempt a poll
    return (self.poll ())
