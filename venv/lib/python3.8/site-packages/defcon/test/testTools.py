from __future__ import print_function
import os
import shutil
from pkg_resources import resource_filename
import zipfile
import fs.osfs
import fs.tempfs
import fs.zipfs
import fs.copy

TESTDATA_DIR = resource_filename("defcon.test", 'testdata')


def getTestFontPath(fileName='TestFont.ufo'):
    return os.path.join(TESTDATA_DIR, fileName)


def getTestFontCopyPath(testFontPath=None):
    if testFontPath is None:
        testFontPath = getTestFontPath()
    dirName, fileName = os.path.split(testFontPath)
    fileName, ext = os.path.splitext(fileName)
    return os.path.join(dirName, fileName + 'Copy' + ext)


def makeTestFontCopy(testFontPath=None):
    if testFontPath is None:
        testFontPath = getTestFontPath()
    copyPath = getTestFontCopyPath(testFontPath)
    if os.path.isdir(testFontPath):
        shutil.copytree(testFontPath, copyPath)
    else:
        shutil.copyfile(testFontPath, copyPath)
    return copyPath


def tearDownTestFontCopy(testFontPath=None):
    if testFontPath is None:
        testFontPath = getTestFontCopyPath()
    if os.path.isdir(testFontPath):
        shutil.rmtree(testFontPath)
    else:
        os.remove(testFontPath)


def openTestFontAsFileSystem(testFontPath=None):
    if testFontPath is None:
        testFontPath = getTestFontPath()
    if zipfile.is_zipfile(testFontPath):
        parentFS = fs.tempfs.TempFS()
        with fs.zipfs.ZipFS(testFontPath, encoding="utf-8") as origFS:
            fs.copy.copy_fs(origFS, parentFS)
            rootDirs = [
                p.name for p in parentFS.scandir(u"/")
                if p.is_dir and p.name != "__MACOSX"
            ]
            fileSystem = parentFS.opendir(
                rootDirs[0], factory=fs.subfs.ClosingSubFS
            )
    else:
        fileSystem = fs.osfs.OSFS(testFontPath)
    return fileSystem


def closeTestFontAsFileSystem(fileSystem, testFontPath=None):
    if testFontPath is None:
        testFontPath = getTestFontPath()
    if not zipfile.is_zipfile(testFontPath):
        return
    rootDir = os.path.splitext(os.path.basename(testFontPath))[0] + ".ufo"
    with fs.zipfs.ZipFS(testFontPath, write=True, encoding="utf-8") as destFS:
        fs.copy.copy_fs(fileSystem, destFS.makedir(rootDir))


class NotificationTestObserver(object):

    def __init__(self, name=None):
        self.name = name
        self.stack = []

    def __repr__(self):
        return "<_TestObservable {name} {id}>".format(name=self.name, id=id(self))

    def notificationCallback(self, notification):
        print(notification.name, notification.object.name)
        self.stack.append((notification.name, notification.object.name))

    def testCallback(self, notification):
        print(notification.name, notification.data)
