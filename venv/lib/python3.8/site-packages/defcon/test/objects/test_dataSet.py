import unittest
import os
import shutil
import fs
import fs.copy
import fs.path
from defcon import Font
from defcon.test.testTools import (
    getTestFontPath, getTestFontCopyPath, makeTestFontCopy,
    openTestFontAsFileSystem, closeTestFontAsFileSystem,
    tearDownTestFontCopy)
from fontTools.ufoLib import UFOReader


class DataSetTest(unittest.TestCase):

    def __init__(self, methodName):
        unittest.TestCase.__init__(self, methodName)

    def tearDown(self):
        path = getTestFontCopyPath()
        if os.path.exists(path):
            shutil.rmtree(path)

    def test_read(self):
        path = getTestFontPath()
        font = Font(path)
        fileNames = [
            "com.typesupply.defcon.test.directory/file 1.txt",
            "com.typesupply.defcon.test.directory/sub directory/file 2.txt",
            "com.typesupply.defcon.test.file"]
        for i, fileName in enumerate(sorted(font.data.fileNames)):
            if True in [j.startswith(".") for j in fileName.split(os.sep)]:
                continue
            self.assertEqual(fileName, fileNames[i])
        self.assertEqual(
            font.data["com.typesupply.defcon.test.directory/file 1.txt"],
            b"This is file 1.")
        self.assertEqual(
            font.data["com.typesupply.defcon.test.directory/sub directory/file 2.txt"],
            b"This is file 2.")
        self.assertEqual(
            font.data["com.typesupply.defcon.test.file"],
            b"This is a top level test file.")

    def test_write(self):
        path = makeTestFontCopy()
        with Font(path) as font:
            font.data["com.typesupply.defcon.test.newdirectory/file.txt"] = b"hello."
            del font.data["com.typesupply.defcon.test.directory/sub directory/file 2.txt"]
            font.save()
            p = os.path.join(path, "data",
                             "com.typesupply.defcon.test.newdirectory", "file.txt")
            self.assertTrue(os.path.exists(p))
            with open(p, "r") as f:
                t = f.read()
            self.assertEqual(t, "hello.")
            p = os.path.join(path, "data",
                             "com.typesupply.defcon.test.directory",
                             "sub directory", "file 2.txt")
            self.assertFalse(os.path.exists(p))
        tearDownTestFontCopy()

    def test_save_as(self):
        path = getTestFontPath()
        with Font(path) as font:
            saveAsPath = getTestFontCopyPath(path)
            font.save(saveAsPath)
            dataDirectory = os.path.join(saveAsPath, "data")
            self.assertTrue(os.path.exists(dataDirectory))
            self.assertTrue(os.path.exists(os.path.join(
                dataDirectory,
                os.path.join("com.typesupply.defcon.test.directory",
                             "file 1.txt"))))
            self.assertTrue(os.path.exists(os.path.join(
                dataDirectory,
                os.path.join("com.typesupply.defcon.test.directory",
                             "sub directory", "file 2.txt"))))
            self.assertTrue(os.path.exists(os.path.join(
                dataDirectory,
                "com.typesupply.defcon.test.file")))
        tearDownTestFontCopy(saveAsPath)

    def test_testForExternalChanges_remove_in_memory_and_scan(self):
        for ufo in (u"TestExternalEditing.ufo", u"TestExternalEditing.ufoz"):
            path = getTestFontPath(ufo)
            path = makeTestFontCopy(path)
            with Font(path) as font:
                del font.data["com.typesupply.defcon.test.file"]
                with UFOReader(path) as reader:
                    self.assertEqual(font.data.testForExternalChanges(reader),
                                 ([], [], []))
            tearDownTestFontCopy(font.path)

    def test_testForExternalChanges_add_in_memory_and_scan(self):
        for ufo in (u"TestExternalEditing.ufo", u"TestExternalEditing.ufoz"):
            path = getTestFontPath(ufo)
            path = makeTestFontCopy(path)
            with Font(path) as font:
                font.data["com.typesupply.defcon.test.file2"] = "blah"
                with UFOReader(path) as reader:
                    self.assertEqual(font.data.testForExternalChanges(reader),
                                 ([], [], []))
            tearDownTestFontCopy(font.path)

    def test_testForExternalChanges_modify_in_memory_and_scan(self):
        for ufo in (u"TestExternalEditing.ufo", u"TestExternalEditing.ufoz"):
            path = getTestFontPath(ufo)
            path = makeTestFontCopy(path)
            with Font(path) as font:
                with UFOReader(path) as reader:
                    font.data["com.typesupply.defcon.test.file"] = "blah"
                    self.assertEqual(font.data.testForExternalChanges(reader),
                                 ([], [], []))
            tearDownTestFontCopy(font.path)

    def test_testForExternalChanges_remove_on_disk_and_scan(self):
        for ufo in (u"TestExternalEditing.ufo", u"TestExternalEditing.ufoz"):
            path = getTestFontPath(ufo)
            path = makeTestFontCopy(path)
            with Font(path) as font:
                # image = font.data["com.typesupply.defcon.test.file"]
                font.data["com.typesupply.defcon.test.file"]
                fileSystem = openTestFontAsFileSystem(font.path)
                fileSystem.remove(fs.path.join("data",
                                       "com.typesupply.defcon.test.file"))
                closeTestFontAsFileSystem(fileSystem, font.path)
                with UFOReader(path) as reader:
                    self.assertEqual(font.data.testForExternalChanges(reader),
                                 ([], [], ["com.typesupply.defcon.test.file"]))
            tearDownTestFontCopy(font.path)

    def test_testForExternalChanges_add_on_disk_and_scan(self):
        for ufo in (u"TestExternalEditing.ufo", u"TestExternalEditing.ufoz"):
            path = getTestFontPath(ufo)
            path = makeTestFontCopy(path)
            with Font(path) as font:
                fileSystem = openTestFontAsFileSystem(font.path)
                source = fs.path.join("data", "com.typesupply.defcon.test.file")
                dest = fs.path.join("data", "com.typesupply.defcon.test.file2")
                fileSystem.copy(source, dest)
                closeTestFontAsFileSystem(fileSystem, font.path)
                with UFOReader(path) as reader:
                    self.assertEqual(font.data.testForExternalChanges(reader),
                                 ([], ["com.typesupply.defcon.test.file2"], []))
            tearDownTestFontCopy(font.path)

    def test_testForExternalChanges_modify_on_disk_and_scan(self):
        for ufo in (u"TestExternalEditing.ufo", u"TestExternalEditing.ufoz"):
            path = getTestFontPath(ufo)
            path = makeTestFontCopy(path)
            with Font(path) as font:
                # d = font.data["com.typesupply.defcon.test.file"]
                font.data["com.typesupply.defcon.test.file"]
                fileSystem = openTestFontAsFileSystem(font.path)
                filePath = fs.path.join("data",
                                        "com.typesupply.defcon.test.file")
                fileSystem.writebytes(filePath, b"blah")
                closeTestFontAsFileSystem(fileSystem, font.path)
                with UFOReader(path) as reader:
                    self.assertEqual(font.data.testForExternalChanges(reader),
                                 (["com.typesupply.defcon.test.file"], [], []))
            tearDownTestFontCopy(font.path)

    def test_reload_data(self):
        path = makeTestFontCopy()
        with Font(path) as font:
            # d = font.data["com.typesupply.defcon.test.file"]
            font.data["com.typesupply.defcon.test.file"]
            filePath = os.path.join(path, "data",
                                    "com.typesupply.defcon.test.file")
            newData = b"blah"
            f = open(filePath, "wb")
            f.write(newData)
            f.close()
            font.data.reloadData(["com.typesupply.defcon.test.file"])
            data = font.data["com.typesupply.defcon.test.file"]
            self.assertEqual(data, newData)
        tearDownTestFontCopy()


if __name__ == "__main__":
    unittest.main()
