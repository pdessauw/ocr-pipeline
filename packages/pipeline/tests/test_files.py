import unittest
from os.path import exists, join, dirname, realpath
from mongoengine.errors import DoesNotExist
from os import remove
from pipeline.files import FileManager
from nose.tools import raises, nottest

TEST_DIR = dirname(realpath(__file__))
RESOURCES_DIR = join(TEST_DIR, 'resources')  # FIXME use the tmp folder instead

TEST_FILE_CONTENT = "Lorem ipsum dolor sit amet"

@nottest
def write_test_file(filename):
    pass

class FileManagerUploadDownloadTestCase(unittest.TestCase):
    def setUp(self):
        def cleanup():
            if exists(self.test_filename):
                remove(self.test_filename)

            self.file_manager.empty()
            self.file_manager.close()

        self.addCleanup(cleanup)

        self.file_manager = FileManager()
        self.test_filename = join(RESOURCES_DIR, "test.txt")

        # TODO Remove this part and insert it into every test
        if not exists(self.test_filename):
            with open(self.test_filename, "wb") as test_file:
                test_file.write(TEST_FILE_CONTENT)

    def test_upload_db_creation(self):
        self.file_manager.store_file(self.test_filename)

        try:
            self.file_manager.retrieve_file(self.test_filename)
        except DoesNotExist:
            self.fail("File has not been stored in DB")

    def test_upload_fs_deletion(self):
        self.file_manager.store_file(self.test_filename)

        self.assertFalse(exists(self.test_filename), "Uploaded file is still present on the filesystem")

    @raises(DoesNotExist)
    def test_download_db_deletion(self):
        self.file_manager.store_file(self.test_filename)
        self.file_manager.retrieve_file(self.test_filename)

        self.file_manager.retrieve_file(self.test_filename)

    def test_download_fs_creation(self):
        self.file_manager.store_file(self.test_filename)
        self.file_manager.retrieve_file(self.test_filename)

        self.assertTrue(exists(self.test_filename), "Retrieved file is not present on the filesystem")

    @raises(DoesNotExist)
    def test_deletion(self):
        self.file_manager.store_file(self.test_filename)
        self.file_manager.delete_file(self.test_filename)

        self.file_manager.retrieve_file(self.test_filename)

    def test_multiple_keys_retrieval(self):
        self.file_manager.store_file(self.test_filename)

        # TODO Simplify file creation with the helper
        with open(self.test_filename, "wb") as test_file:
            test_file.write(TEST_FILE_CONTENT)

        self.file_manager.store_file(self.test_filename)

        self.file_manager.retrieve_file(self.test_filename)


    @raises(DoesNotExist)
    def test_unexisting_file_retrieval(self):
        self.file_manager.retrieve_file(self.test_filename)


if __name__ == '__main__':
    unittest.main()

