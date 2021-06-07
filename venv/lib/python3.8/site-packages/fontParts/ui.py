from fontParts.world import _EnvironmentDispatcher


def AskString(message, value='', title='FontParts'):
    """
    An ask a string dialog, a `message` is required.
    Optionally a `value` and `title` can be provided.

    ::

        from fontParts.ui import AskString
        print(AskString("who are you?"))

    """
    return dispatcher["AskString"](message=message, value=value, title=title)


def AskYesNoCancel(message, title='FontParts', default=0, informativeText=""):
    """
    An ask yes, no or cancel dialog, a `message` is required.
    Optionally a `title`, `default` and `informativeText` can be provided.
    The `default` option is to indicate which button is the default button.

    ::

        from fontParts.ui import AskYesNoCancel
        print(AskYesNoCancel("who are you?"))

    """
    return dispatcher["AskYesNoCancel"](message=message, title=title,
                                        default=default, informativeText=informativeText)


def FindGlyph(aFont, message="Search for a glyph:", title='FontParts'):
    """
    A dialog to search a glyph for a provided  font.
    Optionally a `message`, `title` and `allFonts` can be provided.


        from fontParts.ui import FindGlyph
        from fontParts.world import CurrentFont
        glyph = FindGlyph(CurrentFont())
        print(glyph)

    """
    return dispatcher["FindGlyph"](aFont=aFont, message=message, title=title)


def GetFile(message=None, title=None, directory=None, fileName=None,
            allowsMultipleSelection=False, fileTypes=None):
    """
    An get file dialog.
    Optionally a `message`, `title`, `directory`, `fileName` and
    `allowsMultipleSelection` can be provided.

    ::

        from fontParts.ui import GetFile
        print(GetFile())

    """
    return dispatcher["GetFile"](message=message, title=title, directory=directory,
                                 fileName=fileName,
                                 allowsMultipleSelection=allowsMultipleSelection,
                                 fileTypes=fileTypes)


def GetFileOrFolder(message=None, title=None, directory=None, fileName=None,
                    allowsMultipleSelection=False, fileTypes=None):
    """
    An get file or folder dialog.
    Optionally a `message`, `title`, `directory`, `fileName`,
    `allowsMultipleSelection` and `fileTypes` can be provided.

    ::

        from fontParts.ui import GetFileOrFolder
        print(GetFileOrFolder())

    """
    return dispatcher["GetFileOrFolder"](message=message, title=title,
                                         directory=directory, fileName=fileName,
                                         allowsMultipleSelection=allowsMultipleSelection,
                                         fileTypes=fileTypes)


def Message(message, title='FontParts', informativeText=""):
    """
    An message dialog.
    Optionally a `message`, `title` and `informativeText` can be provided.

    ::

        from fontParts.ui import Message
        print(Message("This is a message"))

    """
    return dispatcher["Message"](message=message, title=title,
                                 informativeText=informativeText)


def PutFile(message=None, fileName=None):
    """
    An put file dialog.
    Optionally a `message` and `fileName` can be provided.

    ::

        from fontParts.ui import PutFile
        print(PutFile())

    """
    return dispatcher["PutFile"](message=message, fileName=fileName)


def SearchList(items, message="Select an item:", title='FontParts'):
    """
    A dialgo to search a given list.
    Optionally a `message`, `title` and `allFonts` can be provided.

    ::

        from fontParts.ui import SearchList
        result = SearchList(["a", "b", "c"])
        print(result)

    """
    return dispatcher["SearchList"](items=items, message=message, title=title)


def SelectFont(message="Select a font:", title='FontParts', allFonts=None):
    """
    Select a font from all open fonts.
    Optionally a `message`, `title` and `allFonts` can be provided.
    If `allFonts` is `None` it will list all open fonts.

    ::

        from fontParts.ui import SelectFont
        font = SelectFont()
        print(font)

    """
    return dispatcher["SelectFont"](message=message, title=title, allFonts=allFonts)


def SelectGlyph(aFont, message="Select a glyph:", title='FontParts'):
    """
    Select a glyph for a given font.
    Optionally a `message` and `title` can be provided.

    ::

        from fontParts.ui import SelectGlyph
        font = CurrentFont()
        glyph = SelectGlyph(font)
        print(glyph)

    """
    return dispatcher["SelectGlyph"](aFont=aFont, message=message, title=title)


def ProgressBar(title="RoboFab...", ticks=None, label=""):
    """
    A progess bar dialog.
    Optionally a `title`, `ticks` and `label` can be provided.

    ::

        from fontParts.ui import ProgressBar

        bar = ProgressBar()
        # do something
        bar.close()

    """
    return dispatcher["ProgressBar"](title=title, ticks=ticks, label=label)


# ----------
# Dispatcher
# ----------

dispatcher = _EnvironmentDispatcher([
    "AskString",
    "AskYesNoCancel",
    "FindGlyph",
    "GetFile",
    "GetFolder",
    "GetFileOrFolder",
    "Message",
    "OneList",
    "PutFile",
    "SearchList",
    "SelectFont",
    "SelectGlyph",
    "ProgressBar",
])
