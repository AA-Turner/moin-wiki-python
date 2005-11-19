"""Module UT exports the following functions,
which have their own help-strings:

UT.dump: dump an object with pprint, or dump a class, instance, or module,
 using pprint to print the members.
UT.Load: A convenient wrapper to unpickle a single object from a file.
UT.Save: A convenient wrapper to pickle a single object into a file.
UT.ThisLine: Return the number of the line where this function was called.
UT.smartreload: a drop-in replacement for __builtins__.reload, only
 smarter, exported directly into __builtins__.
"""##"""Module UT *used to* export the following functions,
##which are now obsolete or irrelavent:
##UT.AppendDictionary: copy possibly multiple dictionaries into a new empty
## dictionary and return the resultant dictionary.
##UT.Call, UT.__Call__: an extension to apply() that allows the 'Function' to
## include optional positional and keyword arguments, to be suplimented by
## additional arguments to Call, and to allow 'Function' to be supplied in
## the more-portably-pickleable format of [[Instance, 'Method']...].
##UT.edit: edit and reload a module's source.
##UT.Quote: preprocess strings to try to convince DOS.readargs() to retrieve
## the original string.
##
##Module UT also exports one function directly
##into module ARexx, which is only visible there:
##
##ARexx.CallArexxFunc: call an ARexx function, returning the result
##"""

##import ARexx
import cPickle
import os
import pprint
import sys
import types
import idlelib.PyShell as PyShell
from inspect import getmodule
from types import ClassType, DictionaryType, FloatType, FrameType, InstanceType
from types import IntType, ListType, LongType, ModuleType, StringType, TupleType
from types import TracebackType
NumericTypes=[FloatType, IntType, LongType]
SequenceTypes=[ListType, TupleType]

##def AppendDictionary(*Args):
## """
##UT.AppendDictionary(*Args):
##
##Version: 1.0
##
##Argument(s):
## one or more dictionaries to be concatenated.
##
##Result:
## A single dictionary containing entries for each item in each dictionary
## supplied in *Args, with duplicate entries represented by the entry in the
## right-most dictionary.
##
##Notes:
## None
##
##Author:
## Lyster E. Wick Jr.
##"""
## Dictionary={}
## for Arg in Args:
##  for Key in Arg.keys():
##   if not Dictionary.has_key(Key):
##    Dictionary[Key]=Arg[Key]
## return Dictionary

##def Call(Function, *Args, **KWArgs):
## """
##UT.Call(Function, *Args, **KWArgs)
##
##Version: 1.0
##
##Arguments:
## Function: an object representing the object to be called.
## Args: Optional positional arguments to be supplied to Function.
## KWArgs: Optional keyword arguments to be supplied to Function.
##
##Result:
## The result, if any, of the called function.
##
##Notes:
## UT.Call() is a wrapper for UT.__Call__(), see its docstring for further notes.
##
##Author:
## Lyster E. Wick Jr.
##"""
## return __Call__(Function, Args, KWArgs)

##def __Call__(Function, Args, KWArgs):
## """
##UT.__Call__(Function, Args, KWArgs)
##
##Version: 1.0
##
##Arguments:
## Function: an object representing the object to be called.
## Args: Optional positional arguments to be supplied to Function.
## KWArgs: Optional keyword arguments to be supplied to Function.
##
##Result:
## The result, if any, of the called function.
##
##Notes:
## Functionaly equivalent to built-in function apply(), __Call__() additionaly
## handles "Function"s other than natively callable objects, ie. lists/tuples
## of the following forms:
##
## - [[Object, 'Method']]
## - [[Object, 'Method'], [Args]]
## - [[Object, 'Method'], {KWArgs}]
## - [[Object, 'Method'], [Args], {KWArgs}]
## - [Callable]
## - [Callable, [Args]]
## - [Callable, {KWArgs}]
## - [Callable, [Args], {KWArgs}]
##
## The Args and KWArgs passed explicitly to __Call__ will be appended to those
## supplied by "Function", with any duplicate KWArgs taking on the value
## supplied explicitly.
##
## Forms that mimic the listed forms but substitute tuples for lists are
## accepted.
##
## Note that [Instance, 'Method'] and [Class, 'Method'] are pickleable,
## whilst the equivalent [to __Call__()] Instance.Method and Class.Method are
## not, unless copy_reg is used to extend Pickle/cPickle [my extension to
## copy_reg handles Methods].
##
##Author:
## Lyster E. Wick Jr.
##"""
## if type(Function) in SequenceTypes:
##  if len(Function)==0: raise TypeError, 'Empty sequence for "Function" is illegal'
##  if type(Function[0]) in SequenceTypes:
##   Callable=getattr(Function[0][0], Function[0][1])
##  else:
##   Callable=Function[0]
##  if len(Function)==2:
##   if not type(Function[1]) in (DictionaryType, ListType, TupleType):
##    raise TypeError, 'Single argument in "Function" must be either sequence or dictionary'
##   if type(Function[1]) in SequenceTypes:
##    Args=list(Function[1])+list(Args)
##   else:
##    KWArgs=AppendDictionary(KWArgs, Function[1])
##  if len(Function)==3:
##   if not type(Function[1]) in SequenceTypes:
##    raise TypeError, 'Non-sequence positional arguments in "Function"'
##   if not type(Function[2]) is DictionaryType:
##    raise TypeError, 'Non-dictionary keyword arguments in "Function"'
##   Args=List(Function[1])+list(Args)
##   KWArgs=AppendDictionary(KWArgs, Function[2])
##  if len(Function)>3: raise TypeError, 'Sequence for "Function" too long'
##  Function=Callable
## return apply(Function, Args, KWArgs)

##def CallARexxFunc(Func, *Args):
## # Irmen de Jong copied this into Arexx.py without crediting me,
## # but he did improve it in the process. This version, however,
## # also by me, is even better than his version.
## """
##UT.CallARexxFunc(Func, *Args)
##
##Version: 0.3
##
##Arguments:
## Func:  The name of the ARexx function to be called.
## *Args: The arguments to be passed to the ARexx function.
##
##Result:
## Whatever the ARexx function returns, as a String.
##
##Notes:
## CallARexxFunc can call any ARexx function, including functions defined by
## the ARexx interpreter, functions defined in libraries on the ARexx
## function library list, and functions defined by external ARexx scripts,
## but NOT "internal" functions defined by labels inside of ARexx scripts.
##
## Irmen de Jong improved on the original version by Lyster E. Wick Jr., and
## this is an improvement by the original author over Irmen's version.
##
##Author:
## Lyster E. Wick Jr.
##"""
## return ARexx.SendARexxMsg('REXX', 'Return '+Func+`Args`)
##
### Export this function into module ARexx in place of the version defined there.
##ARexx.CallARexxFunc=CallARexxFunc
##del CallARexxFunc

def dump(Object):
 """Prety-print objects, including some types not supported by `pprint`.

UT.dump(Object)

Version: 0.3

Argument:
 Object: The object to be pretty-printed.

Author:
 Lyster E. Wick Jr.
"""
 ## 
 ## improved the type-detection code somewhat (now catches new-style
 ## subclasses, too)
 ## 200307.26: New in v0.3:
 ## restricted output to items in the Object's __dict__ when the
 ## object has one (most classes and modules do)
 if isinstance(Object, (
   ClassType,
   FrameType,
   InstanceType,
   ModuleType,
   TracebackType,
   )):
  try:
   PropertyList = Object.__dict__.keys()
   PropertyList.sort()
  except AttributeError:
   PropertyList = dir(Object)
  for Property in PropertyList:
   print Property+': ',
   pprint.pprint( getattr( Object, Property ))
 else:
  pprint.pprint( Object )

#
# The functionality of the following function was transfered into its
# own module, where it is configured as an I.D.L.E. extension module.
#

##def edit(Object):
## """
##UT.edit(Object)
##
##Version: 0.5
##
##Argument:
## Object: The object whose source is to be edited.
##
##Result:
## None
##
##Notes:
## Module must evaluate to a module whose source is available to be
## edited.
##
## The I.D.L.E. editor is invoked, with the source positioned at the
## object's definition, if possible.
##
##Author:
## Lyster E. Wick Jr.
##"""
## ## 200309.17: New in v0.5:
## ## * Support for I.D.L.E.'s internal editor added.
## ##   Old docstring:
## ##    An external editor is invoked on the source file,
## ##    and the module is reloaded when the editor returns.
## ## * Type-checking converted to use isinstance() instead of directly
## ##   comparing the result of type() with specific hard-coded types.
## global _LastEdited
## if Object=='':
####  import Browse
####  Object=Browse.Browse()
##  Object = _LastEdited
## FileName  =None
## Module    =None
## SourceLine=None
#### ObjectType=type(Object)
## if   isinstance(Object, types.ClassType):
##  Module    =sys.modules[Object.__module__]
##  FileName  =Module.__file__
####  SourceLine="Find (class %s)\n" % (Object.__name__,)
## elif isinstance(Object,  types.FunctionType):
##  FileName  =Object.func_code.co_filename
##  SourceLine=Object.func_code.co_firstlineno
## elif isinstance(Object,  types.InstanceType):
##  Module    =Object.__dict__.get('__module__') or Object.__class__.__module__
##  if isinstance(Module, basestring): Module=sys.modules[Module]
##  FileName  =Object.__dict__.get('__file__') or Module.__file__
####  SourceLine=Object.__dict__.get('__DME_FindMe__') or "Find (class %s)\n" % (Object.__class__.__name__,)
## elif isinstance(Object,  types.MethodType):
##  Module    =sys.modules[Object.im_class.__module__]
##  FileName  =Module.__file__
##  SourceLine=Object.im_func.func_code.co_firstlineno
## elif isinstance(Object,  types.ModuleType):
##  Module    =Object
##  FileName  =Object.__dict__.get('__file__')
##  SourceLine=1
## else:
####  dump(locals())
##  raise TypeError, "Can't identify source file of %s objects" % (type(Object).__name__,)
## if FileName is None:
####  dump(locals())
##  raise ValueError, "Can't identify source file of %s" % (`Object`,)
## if FileName[-1]=='c': FileName=FileName[:-1]
## if FileName[-1]=='o': FileName=FileName[:-1]
#### SourcePath=os.path.join('Ram:T', os.path.basename(FileName))
#### if SourceLine: open(SourcePath, 'w').write(SourceLine+'Block Block ScreenTop While !cb ScrollDown UnBlock\n')
## edit = PyShell.flist.open(FileName)
## if SourceLine:
##  edit.gotoline(SourceLine)
#### os.system('DME '+FileName)
#### if not Module:
####  if FileName[-3:]=='.py':        FileName=FileName[:-3]
####  if FileName[-9:]=='/__init__':  FileName=FileName[:-9]
####  FileName=FileName.replace('/', '.')
####  Modules=sys.modules.keys()
####  Modules.sort(lambda x,y: -cmp(len(x), len(y)))
####  for Module in Modules:
####   if FileName[-len(Module):]==Module:
####    Module=sys.modules[Module]
####    break
#### reload(Module)
####  if not os.path.exists(self.file):
####   return
##### if 'RawPython' in sys.modules.keys():
#####  try:
#####   Module.RawPythonInit
#####  except:
#####   pass
#####  else:
#####   if callable(Module.RawPythonInit):
#####    Module.RawPythonInit()
#####  try:
#####   Module.RawPythonCommands.keys
#####  except AttributeError:
#####   pass
#####  else:
#####   if callable(Module.RawPythonCommands.keys):
#####    from RawPython import RawPythonInternalCommands
#####    for Command in Module.RawPythonCommands.keys():
#####     RawPythonInternalCommands[Command]=Module.RawPythonCommands[Command]
#### if os.path.exists(SourcePath): os.unlink(SourcePath)
#### import linecache
#### linecache.checkcache()
##_LastEdited = None
#
# Octal was created as an exercize, and was obsolete before it was written.
#
#def Octal(I, Width=7):
# MyI=I+0
# OctString=''
# for Octit in range(0, Width):
#  OctString=`MyI - (MyI/8)*8`+OctString
#  MyI=(MyI/8)
# return OctString
#

class Load:
 """Load a pickled object from a named file, and unpickle it.

UT.Load(File)

Version: 0.1

Argument:
 File: The name of the file whose pickled object is to be retrieved.

Result:
 The pickled object in the file, unpickled.

Notes:
 Implemented as a class to allow use of Load.Name and Load['Name'] as
 well as the usual Load('Name'), Load retrieves a single pickled object
 from the beginning of a named named file, such as is created by UT.Save().

Author:
 Lyster E. Wick Jr.
"""
 def Load(
  Load,
  File,
  ):
  return cPickle.load(open(File))
 def __call__(
  Load,
  File,
  ):
  return Load.Load(File)
 def __getattr__(
  Load,
  File,
  ):
  return Load.Load(File)
 def __getitem__(
  Load,
  File,
  ):
  return Load.Load(File)

Load=Load()

##def ProtectBitsToText(Bits):
## """UT.ProtectBitsToText(Bits)
##
##Version: 1.0
##
##Argument:
## A file's protection bits as an integer.
##
##Result:
## The same protection bits as a text string.
##
##Notes:
## None
##
##Author:
## Lyster E. Wick Jr.
##"""
## Text=['dewr-------------', '----apshdewrdewru']
## BitNum=0
## TextOut=''
## for I in range(17):
##  Bits, Bit=divmod(Bits, 2)
##  TextOut=Text[Bit][BitNum]+TextOut
##  BitNum=BitNum+1
## return TextOut[0]+TextOut[-8:]+' '+TextOut[1:5]+' '+TextOut[5:9]

def Save(
 File,
 Object,
 Backup=True,
 Protocol=-1,
 ):
 """Pickle an object and write it to a named file.

UT.Save(File, Object[, Backup[, Protocol]])

Version: 0.3

Arguments:
 File:   The name of the file into which the object is to be pickled.
 Object: The object which is to be pickled into the file.
 Backup: A flag specifying that a back-up copy of the file is to be saved,
         or a string specifying where to save the back-up copy of the file.

Result:
 None. The object is written into the file, pickled in the best available
 format.

Notes:
 A convenient wrapper for cPickle's dump function, Save writes a single pickled
 object to a file, replacing the entire previous contents of the file, if any,
 with a data value suitable for processing by UT.Load() or any similar code.

 Any true value of Backup [which defaults to a true value] causes Save to
 attempt to make a back-up copy of the old object file before creating the
 new file. If the value of Backup is a string value, it is used as the name
 of the back-up file, else the name is constructed by appending ".bak" to
 the name contained in File.

 Any errors encountered whilst making the back-up file are silently ignored.

Author:
 Lyster E. Wick Jr.
"""
 ## 200308.20: New in v0.2:
 ## Changed the documentation to represent the pickle format as "the best
 ## available" format instead of "binary" format.
 ## Changed the code to use the best available format instead of TEXT FORMAT!
 ## The code and documentation actually *agree* on this now.
 ## Changed the code to detect the type of the Backup flag using isinstance()
 ## instead of direct type comparison.
 ## 200310.07: New in v0.3:
 ## Added an optional fourth parameter to specify the desired pickle protocol,
 ## which defaults to "best available".
 if Backup:
  if not isinstance(Backup, basestring):
   Backup=File+'.bak'
  try:    os.system('Copy "'+File+'" "'+Backup+'"')
  except: pass
 f=file(File, 'wb') 
 cPickle.dump(Object, f, Protocol)
 f.close()

##def Quote(String):
## """UT.Quote(String)
##
##Version: 0.4
##
##Argument:
## String: The string to process.
##
##Result:
## The processed string.
##
##Notes:
## None
##
##Author:
## Lyster E. Wick Jr.
##"""
## if type(String) in NumericTypes: return `String`
## import string
## String=string.join(string.split(String, '*'), '**')
## String=string.join(string.split(String, '"'), '*"')
## String=string.join(string.split(String, '\012'), '*n')
## return '"'+String+'"'

def ThisLine(depth=0):
  """Return the number of the line where this function was called.

UT.ThisLine()

Version: 0.4

Optional Argument:
 The depth of the frame to interogate for line number and function
 name.

Result:
 The number of the line where the function was called from, and the
 name of the calling function.

Author:
 Lyster E. Wick Jr.
"""
  ## 200402.20: New in v0.2:
  ## * now also extracts and returns the name of the calling function.
  ## 200402.21: New in v0.3:
  ## * now uses sys._getframe() instead of raising an error and
  ##   extracting the frame.
  ## * removed from the docstring the note about using a deliberate
  ##   error to achieve access to the required frame.
  ## 200410.01: New in v0.4:
  ## * added an optional parameter `depth`, specifying how deep in the
  ##   call stack to peek.
  f = sys._getframe(depth + 1)
  return [f.f_code.co_name, f.f_lineno]

def smartreload(Module):
 """A 'smart' reload that auto-reloads modules listed in dependancy lists.

UT.smartreload()

Version: 0.3

Argument:
 Module: The module to be reloaded.

Result:
 The module whose reload was requested.

Side effects:
 The module is reloaded, as are any modules listed in
 Module.__reload_before__ and __reload_after__.

Notes:
 The intended use of smartreload, setReloadBefore, and setReloadAfter
 is as a set of development tools:

 When one module depends upon another module in such a way that the
 dependant module breaks when the other module is reloaded, the
 dependant module can call UT.setReloadAfter(Other, Self) to ensure
 that it gets reloaded every time the other module is reloaded.

 When one module depends upon another module in such a way that the
 dependant module breaks when reloaded unless another module is
 re-initialized first, the dependant module can call
 UT.setReloadBefore(Self, Other) to ensure that the other module gets
 reloaded and re-initialized first every time the dependant module is
 reloaded.

Author: Lyster E. Wick Jr.
"""
 # 200311.28: initial version.
 # 200312.02: New in v0.1:
 # * cache `__builtins__.reload` as `_reload`
 # * call the cached _reload instead of the built-in `reload`
 # * replace the built-in `reload` with `smartreload`
 # 200402.19: New in v0.2:
 # * use `inspect.getmodule` to allow reloading a module when given a
 #   non-module object defined there.
 # 200507.03: New in v0.3:
 # * Now returns the original module, for consistancy with the
 #   standard implimentation.
 # * ***FIXED***: a small bug with *MAJOR* bad-mojo side-effects:
 #   Attempting to smartreload a module with __reload_before__ defined
 #   would trigger a recursive infinite loop of trying to smartreload
 #   the original module, terminating only when the depth of the call
 #   stack caused problems.
 # * The documentation was extended with better[?] explanations.
 ArgModule = Module
 Module = getmodule(Module)
 assert Module, "Can't find module for object %r." % (ArgModule)
 if hasattr(Module, '__reload_before__'):
  for m in Module.__reload_before__:
   smartreload(m)
 print _reload(Module)
 if hasattr(Module, '__reload_after__'):
  for m in Module.__reload_after__:
   smartreload(m)
 return Module

## 200510.23 New:
## * now uses the new sitecustomize.patch(Where, What) function,
##   with checks that we don`t cache a previous version of
##   smartreload().
import sitecustomize
while (sitecustomize.isPatched(reload)
       and __file__ in (
         reload.__previous_function__.func_code.co_filename,
         reload.__previous_function__.func_code.co_filename+"w",
         reload.__previous_function__.func_code.co_filename+"c",
         reload.__previous_function__.func_code.co_filename+"o")
       and reload.__name__ == "smartreload"):
  sitecustomize.unpatch(sys.modules["__builtin__"], "reload")
try: _reload
except: _reload = __builtins__['reload']
sitecustomize.patch(sys.modules["__builtin__"], "reload", smartreload)
del sitecustomize
##__builtins__['reload'] = smartreload

def setReloadBefore(Mod1, Mod2, Cancel=False):
  """Set Mod2 to [not] be smartreloaded before Mod1.

UT.setReloadBefore(Mod1, Mod2, Cancel)

Version: 0.2

Arguments:
 Mod1: The module whose __reload_before__ list is to be updated.
 Mod2: The module to be inserted in that list.
 Cancel: Flag to cause Mod2 to be removed from the list instead of
         added.

Result:
 None. Mod2 is inserted into Mod1's __reload_before__ list.

Notes:
 See smartreload`s notes.

Author: Lyster E. Wick Jr.
"""
  # 200311.28: initial version.
  # 200507.03: New in v0.1:
  # * optional Cancel flag to cause removal of Mod2 from Mod1`s
  #   __reload_before__ list.
  # 200510.23: New in v0.2:
  # * documentation updated to include new Cancel flag.
  if Cancel:
    try: Mod1.__reload_before__.remove(Mod2)
    except: pass
  else:
    try: Mod1.__reload_before__
    except: Mod1.__reload_before__ = []
    if Mod2 not in Mod1.__reload_before__:
      Mod1.__reload_before__.append(Mod2)

def setReloadAfter(Mod1, Mod2, Cancel=False):
  """Set Mod2 to be smartreloaded after Mod1.

UT.setReloadAfter(Mod1, Mod2, Cancel=False)

Version: 0.2

Arguments:
 Mod1: The module whose __reload_after__ list is to be updated.
 Mod2: The module to be inserted in that list.
 Cancel: Flag to cause Mod2 to be removed from the list instead of
         added.

Result:
 None. Mod2 is inserted into Mod1's __reload_after__ list.

Notes:
 See smartreload`s notes.

Author: Lyster E. Wick Jr.
"""
  # 200311.28: initial version.
  # 200507.03: New in v0.1:
  # * optional Cancel flag to cause removal of Mod2 from Mod1`s
  #   __reload_after__ list.
  # 200510.23: New in v0.2:
  # * documentation updated to include new Cancel flag.
  # * bug fix: added Cancel flag to the formal argument list.
  if Cancel:
    try: Mod1.__reload_after__.remove(Mod2)
    except: pass
  else:
    try: Mod1.__reload_after__
    except: Mod1.__reload_after__ = []
    if Mod2 not in Mod1.__reload_after__:
      Mod1.__reload_after__.append(Mod2)

__Aliases__ = {
 'dump': dump,
## 'edit':         edit,
 'reload':         smartreload,
 'setReloadAfter': setReloadAfter,
 'setReloadBefore':setReloadBefore,
 'Save':           Save,
 }
