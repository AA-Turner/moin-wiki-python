"""Extend I.D.L.E. with an Alias facility for the command shell.

This I.D.L.E. extension provides the following functionality enhancements:
* an Alias facility for I.D.L.E.'s command shell
* an 'alias' command for the Alias facility
* an 'unalias' command for the Alias facility

The Alias facility, implemented by the function runsource, enhances
the I.D.L.E. command shell by promoting all fully-qualified callable
objects and the string keys of all callable objects stored in the
module-global dictionary "GlobalAliases" into "commands", UNDER
SPECIFIC CIRCUMSTANCES.

At the command prompt ONLY [i.e., NOT in module source code!], before
a line is submitted to the normal I.D.L.E. execution machinery,
several checks are performed:

* The first 'word' is split from the rest of the string, and the two
  chunks are saved as Command and Args.
* Command is then looked up in the module-global dictionary
  GlobalAliases.
  If found, the corresponding value becomes the Command, else the
  command string is evaluated in the context of the module __main__,
  and the result of the execution becomes the Command.
* If the preceeding operation yeilds a callable, Args is also evaluated
  in the context of module __main__. If the evaluation succeeds, the
  result becomes the Args.
* If Args is not by now a tuple, it is wrapped in one.

  Up to this point, any errors are trapped and silently dealt with,
  diverting evaluation of the command to "normal" channels if unable
  to proceed.

## XXX TO DO: before handing a command off to the "normal" evaluator,
## attempt to import the presumed module named by the command, and, if
## successful, update the dictionary of defined Alises from a
## specially-named dictionary found there, or from the dictionary
## returned by a specially-named callable found there, then enter the
## module into the namespace of module __main__.

* The Command callable is then called, and the Args tuple is used to
  supply positional arguments.
  If an error occurs, a traceback is printed, else the result of the
  call, if non-None, is printed.
  In either case, a new command line is solicited.

If the fully-qualified callable is followed immediately by an open
paren and a space, IN THAT ORDER, the "normal" command processing
takes over. This is useful for situations when you want to prevent the
Alias mechanism from evaluating the result of a function that returns
a callable. Another method is to put a space BEFORE the open paren,
letting Alias evaluate the argstring as a parenthasis-grouped
expression to be passed to the callable. Examples:

 >>> type {}
 <type 'dict'>
 >>> type({})
 {}
 >>> type ({})
 <type 'dict'>
 >>> type( {})
 <type 'dict'>
 >>> 

The first three examples are evaluated by the Alias evaluator; the
fourth is evaluated by the "normal" evaluator. The second example is
likely a source for confusion: Note that <type 'dict'> is callable,
and that calling it without arguments yeilds an empty dictionary!

The alias command, implemented by the function alias, provides four
features:

* If called with no arguments, or with a first argument equal to an
  empty string, the current dictionary of defined GlobalAliases is
  displayed nicely formatted.
* If called with a first argument that is [a subclass of] a dictionary,
  the dictionary is used to update the dictionary of defined GlobalAliases.
* If called with a non-None second argument, the second argument is
  inserted into the dictionary of defined GlobalAliases using the first
  argument as the key.
* Otherwise, the first [and presumably only] argument is looked up in
  the dictionary of defined GlobalAliases, and the pair is displayed.

The unalias command, implemented by the function unalias, provides a
single feature: if the only argument matches a key in the
module-global dictionary GlobalAliases, the key:value pair is deleted, else
a simple error message is displayed.
"""

import UT, code, os, sys, types, __builtin__

class Alias:
 def __init__(Self, editwin):
  pass

def runsource(self, source, filename="<input>", symbol="single"):
 """Compile and run some source in the interpreter.

 Arguments are as for compile_command().

 One several things can happen:

 1) The input is empty. Nothing happens.

 2) The input matches a registered Alias. The matching callable is
 called with the supplied arguments, if any.

 3) The input evaluates to a callable. The callable is called with the
 supplied arguments, if any.

 4) The input matches an importable module. The module is imported,
 bound in the source context, and checked for any of several
 signatures:

 4a) The module defines a mapping named __Aliases__. The dictionary of
 registered Aliases is updated from this dictionary.

 4b) The module defines a callable named __Alias__. The callable
 becomes the command [and the module is NOT bound].

 Note: 4a and 4b are not mutually exclusive, but the dictionary update
 is performed _before_ the function call.

 5) The input is incorrect; compile_command() raised an exception
 (SyntaxError or OverflowError).  A syntax traceback will be printed
 by calling the showsyntaxerror() method.

 6) The input is incomplete, and more input is required;
 compile_command() returned None.  Nothing happens.

 7) The input is complete; compile_command() returned a code object.
 The code is executed by calling self.runcode() (which also handles
 run-time exceptions, except for SystemExit).

 The return value is True in case 6, False in the other cases (unless
 an exception is raised).  The return value can be used to decide
 whether to use sys.ps1 or sys.ps2 to prompt the next line.

 """
## from UT import ThisLine
## print >> sys.stderr, "Here goes!"
## print >> sys.stderr, '### %r %r' % (ThisLine(), source)
 if not source.strip(): source = 'pass' # Case 1: Empty line; do nothing.
## print >> sys.stderr, '### %r %r' % (ThisLine(), source.split())
## print >> sys.stderr, '### %r %r' % (ThisLine(), source.split()[0])
 Command, Args = (source.split(' ', 1) + [''])[:2]
## print >> sys.stderr, '### %r %r %r' % (ThisLine(), Command, Args)
 import __main__
 # Case 2: Is this a REGISTERED Alias?
 if Command in GlobalAliases.keys():
  Command = GlobalAliases[Command]
 else:
  # Case 3: Ok, it isn't registered, so try to evaluate it.
  try: Command = eval(Command, self.locals)
  except: pass
## print >> sys.stderr, '### %r %r %r' % (ThisLine(), Command, Args)
  
 # Case 4: It wasn't a callable, so try to import it as a module.
 if isinstance(Command, types.StringType): # and (Args == ''):
  try:    exec 'import %s as Command' % Command #; print "Import succeeded."
  except: pass
 if isinstance(Command, types.ModuleType):
##  print >> sys.stderr, '### %r import %r' % (ThisLine(), Command.__name__)

  # Case 4a: The module defines a mapping named __Aliases__.
  try:    GlobalAliases.update(Command.__Aliases__)
  except: pass

  # Case 4b: The module defines a callable named __Alias__.
  try:    Command = Command.__Alias__
  except: pass
##  print >> sys.stderr, '### %r %r %r' % (ThisLine(), Command, Args)
 if isinstance(Command, types.ModuleType):
  source = 'import %s;%s' % (source, source,)

 # If we have a callable, we're going to need to evaluate the
 # arguments, if any.
 if callable(Command):

  # I know, I know, the code below makes it awkward to pass a
  # single empty string to commands; use
  # >>> blah '',
  # [It's still easier than typing two parenthases.]
  if Args == '':
   Args = ()
  else:
   try:    Args = eval(Args, self.locals)
   except: pass
   if not isinstance(Args, types.TupleType):
    Args = (Args,)
##  print >> sys.stderr, '### %r %r %r' % (ThisLine(), Command, Args)
##  print >> sys.stderr, '### %r call %r%r' % (ThisLine(), Command, Args)
  __builtin__._AliasCommand = Command
  __builtin__._AliasArgs = Args
  source = '_AliasCommand(*_AliasArgs)'

 try:
  code = self.compile(source, filename, symbol)
 except (OverflowError, SyntaxError, ValueError):
  # Case 5
  self.showsyntaxerror(filename)
  return False

 if code is None:
  # Case 6
  return True

 # Case 7
 self.runcode(code)
 return False

##   if Args is not '':
##    # It's a module and we have Args; try to call its __init__ function.
##    print >> sys.stderr, '### 181 call %s.__init__%s' % (Command, Args)
##    try: Command.__init__(*Args)
##    except: self.showtraceback()
##    return 0
##
##   if 'Aliases' in Command.__dict__.keys() \
##      and isinstance(Command.Aliases, types.DictType):
##    # It's a module and we don't have args, but we DO have a dictionary
##    # named Aliases.
##    print >> sys.stderr, '### 190 bind', Command
##    if Module: self.locals[Module] = Command
##    GlobalAliases.update(Command.Aliases)
##    return 0
##
##   if 'MakeAliases' in Command.__dict__.keys() \
##      and isinstance(Command.MakeAliases, types.FunctionType):
##    # It's a module and we don't have args or an Aliases dictionry, but
##    # we DO have a function named MakeAliases...
##    Aliases = Command.MakeAliases()
##    if isinstance(Aliases, types.DictType):
##     # ...AND it returnes a dictionary.
##     print >> sys.stderr, '### 202 bind', Command
##     self.locals[Command] = Module
##     GlobalAliases.update(Aliases)
##     return 0
##
##  print >> sys.stderr, '### 207', `source`
##  return PyShell.InteractiveInterpreter.runsource(self, source, filename)
##  return oldrunsource(self, source)
## finally:
##  print >> sys.stderr, "How's that?"
##  self.tkconsole.endexecuting()
##  self.tkconsole.resetoutput()
##  if self.save_warnings_filters is not None:
##   PyShell.warnings.filters[:] = self.save_warnings_filters
##   self.save_warnings_filters = None

def _help(Topic=None):
 if Topic in GlobalAliases.keys():
  help(GlobalAliases[Topic])
 else:
  help(Topic)

_help.__doc__ = help.__doc__

def alias(Name='', Func=None):
 # Don't bother with sanity checks; runsource takes care of that.
 print `Name, Func`
 if Name == '':
  import UT
  try:
   UT.dump(dict(map(lambda (x, y): (x, '.'.join([y.__module__, y.__name__])),
                    GlobalAliases.items())))
  except:
   UT.dump(GlobalAliases)
 elif isinstance(Name, types.DictType):
  GlobalAliases.update(Name)
 elif Func is None:
  print ' %s: %s' % (Name, GlobalAliases.get(Name, "Undefined"))
 else:
  GlobalAliases[Name] = Func

def unalias(Name):
 try:
  del GlobalAliases[Name]
 except:
  print "Error: %s is not a defined alias." % `Name`

def usage(Topic):
 if Topic in GlobalAliases.keys():
  Topic = GlobalAliases[Topic]
 try:
  if Topic.__doc__: print Topic.__doc__
  else: print 'None.'
 except: print 'None'

__Aliases__ = {
 'alias':   alias,
 'help':    _help,
 'unalias': unalias,
 'usage':   usage,
 }

GlobalAliases = {}
code.InteractiveInterpreter.runsource = runsource
sys.modules['Alias'] = sys.modules['idlelib.Alias']
print "Alias installed."
