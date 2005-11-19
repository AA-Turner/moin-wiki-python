import inspect
import os
import sys
import UT

try:
  Geometry = UT.Load(os.path.join(
    os.path.dirname(__file__),
    'Geometry.Pickle'))
except:
  Geometry = {}

class Edit:
  ## 200412.12: New in v?.?:
  ## * Added function with matching menu entry to unset the current
  ##   file`s edit-window geometry.
  ## 200503.15: No longer needed:
  ##  a means of purging the Geometry of all entries for files that no
  ##  longer exist.
  ## 200510.11: changed the call of `sitecustomize.patch` to
  ## `sitecustomize.patchNames` to reflect the name change in
  ## `sitecustomize`.
  def __init__(Self, editwin):
    global flist
    flist = editwin.flist
    geometry = Geometry.get(editwin.io.filename, '+46+44')
    editwin.top.geometry(geometry)
    Self.editwin = editwin
  menudefs = [ ('options', [('_Save window size and position',
                             '<<save-size>>'),
                            ('Clear window size and position',
                             '<<clear-size>>'),
                            None,
                            ]), ]

  def clear_size_event(Self, Event):
    try:
      del Geometry[Self.editwin.io.filename]
    except:
      pass
    save()
    UT.dump(Geometry)
    print `Self.editwin.root`

  def save_size_event(Self, Event):
    Geometry[Self.editwin.io.filename] = '%sx%s+%s+%s' % tuple(Self.editwin.get_geometry())
    save()
    UT.dump(Geometry)
    print `Self.editwin.root`

def save():
  ## 200503.15: New in v?.?:
  ## * Added call to new purge() function.
  purge()
  UT.Save(os.path.join(os.path.dirname(__file__), 'Geometry.Pickle'), Geometry, True, 0)
  print >> sys.stderr, 'Geometry saved.'

def purge():
  ## 200503.15: Version 0.0:
  ## Called by save() prior to saving, this function purges the
  ## Geometry dictionary of entries for files that no longer exist.
  for Path in sorted(Geometry.keys()):
    if Path:
      try: os.stat(Path)
      except:
        del Geometry[Path]
        print >> sys.stderr, 'Purged:', Path

def edit(Thing='', ignoreCustomHook=False, *Args, **kwArgs):
  """Edit the source code of an object, if available

Edit.edit(Thing)

Version: 0.8

Arguments:
  Thing: The object whose source is to be edited.
  ignoreCustomHook: A flag to ignore the `__Edit__` hook.

Result:
  None (usually)

Notes:
  Object must evaluate to an object that satisfies one or more of the
  following criteria:
  * The object has a callable attribute named __Edit__.
  * The module where the object was defined is identifiable [by module
    `inspect`], and the module's source is available to be edited.
  * The object is a string value that identifies a file on the host OS.

  If the object has a callable attribute named __Edit__, it is called,
  and the result is the return value, else the I.D.L.E. editor is
  invoked, with the source positioned at the object's definition, if
  possible, and None is returned. Live-object editors should be
  prepared to accept an optional keyword argument named `__file__`
  containing the filesystem path of the file that object was loaded
  from. This will not be present if edit did not unpickle the object
  from a file.

  When `ignoreCustomHook` is True, `edit`, does NOT honor `__Edit__`
  attributes. This is useful for creating classes whose instances use
  a custom editor, without invoking the custom editor on the class
  itself.

Author:
  Lyster E. Wick Jr.
"""
  ## 200309.17: New in v0.5:
  ## * Support for I.D.L.E.'s internal editor added.
  ##   Old docstring:
  ##    An external editor is invoked on the source file,
  ##    and the module is reloaded when the editor returns.
  ## * Type-checking converted to use isinstance() instead of directly
  ##   comparing the result of type() with specific hard-coded types.
  ## 200310.23: New in v0.6:
  ## * Objects may define custom editors: Iff the `Thing` to be edited has a
  ##   callable attribute named `__Edit__`, `Thing.__Edit__(Thing)` is called
  ##   in place of the usual mechanism, and its return value is returned.
  ## 200311.03: New in v0.7: ???
  ## 200312.03: New in v0.8:
  ## * now uses module `inspect` to identify the source code of an
  ##   object, when possible
  ## 200312.03: New in v0.9:
  ## * added flag `ignoreCustomHook` to bypass the `__Edit__` custom editor hook.
  ## 200510.10: New in v0.10:
  ## * updated refrences to sitecustomize.patch to use the new name (.patchNames).
  ## 200511.06: New iv v0.11:
  ## * Added long-missing code to allow the editing of specified text files.
  ## * Removed references to the module a thing is defined in; since
  ##   module `inspect` deals with that, we don't have to.
  ## * Added the ability to extract a live object from a file containing a
  ##   pickle, and live-edit the resulting object.
  ## * Optimized module filename extension manipulation a tad,
  ##   tightening the test to trigger only when the whole extension
  ##   matches, instead of whenever the end of the name matches
  ##   without checking for the extension seperator.
  ## * Added an optional keyword `__file__` to the live-object editor
  ##   call when the object is extracted from a pickle.
  ## * Updated the docstring a tad.
  ## * Added comments to the code.
  ## * ??? Nothing else I can remember just a few miniutes later.
  global _LastEdited
  import sitecustomize, types
  if Thing=='':
    Thing = _LastEdited
  else:
    _LastEdited = Thing
  # We do this here, in case we have a live editable object without a
  # companion filesystem object.
  if not ignoreCustomHook \
    and hasattr(Thing, '__Edit__') \
    and callable(Thing.__Edit__):
    return Thing.__Edit__(Thing, *Args, **kwArgs)
  FileName  =None
  SourceLine=None
  try: FileName = inspect.getsourcefile(Thing)
  except: pass
  try: SourceLine = inspect.getsourcelines(Thing)[-1]
  except: pass
  # Do we have a file name instead of a live object?
  if isinstance(Thing, basestring) \
    and os.path.exists(Thing):
    FileName = sitecustomize._patch(Thing)
  if FileName is None:
    raise ValueError, "Can't identify source file of %r" % (Thing,)
  # Normalize the filespec case to match the filesystem.
  FileName = os.path.join(sitecustomize._patch(os.path.dirname(FileName)),os.path.basename(FileName))
  # If we have a module loaded from a bytecodefile, we need the sourcefile name.
  if FileName[-4:].lower() in (".pyc", "pyo"):   FileName=FileName[:-1]
  # Do we have a picklefile?
  try: Thing = UT.Load(FileName)
  except: pass
  # We do this again here, in case we found a pickled editable object
  # in the filesystem object.
  if not ignoreCustomHook \
    and hasattr(Thing, '__Edit__') \
    and callable(Thing.__Edit__):
    return Thing.__Edit__(Thing, __file__=FileName, *Args, **kwArgs)
  edit = flist.open(FileName)
  if SourceLine:
    edit.gotoline(SourceLine)

_LastEdited = None
__Aliases__ = {
  'edit': edit,
  'save': save,
  }
import sys
sys.modules['Edit']=sys.modules['idlelib.Edit']
