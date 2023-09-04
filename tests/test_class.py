import unittest
from cdp_parser import File, Folder, Client

class TestFile(unittest.TestCase):
    def setUp(self):
        # Set up a mock client for testing
        self.client = Client("https://example.com/")
        self.file = File('example_file', 'https://example.com/file.pdf', "(pdf, 02/07/2023, 729 ko)", [], self.client)

    def test_file_initialization(self):
        self.assertEqual(self.file.name, 'example_file')
        self.assertEqual(self.file.extension, 'pdf')
        self.assertEqual(str(self.file.date), '2023-07-02')
        self.assertEqual(self.file.size, 729 * 1000)

class TestFolder(unittest.TestCase):
    def setUp(self):
        # Set up a mock client for testing
        self.client = Client("https://example.com/")
        self.folder_files_subfolder = Folder('example_folder', 'https://example.com/folder', "(6 répertoires, 1 document)", [], self.client)

        self.folder_one_subfolder = Folder('example_folder', 'https://example.com/folder', "(1 répertoire)", [], self.client)

        self.folder_documents = Folder('example_folder', 'https://example.com/folder', "(8 documents)", [], self.client)

        self.empty_folder = Folder('example_folder', 'https://example.com/folder', "(vide)", [], self.client)

    def test_folder_files_subfolder_initialization(self):
        self.assertEqual(self.folder_files_subfolder.name, 'example_folder')
        self.assertEqual(self.folder_files_subfolder.nb_files, 1)
        self.assertEqual(self.folder_files_subfolder.nb_folders, 6)

    def test_folder_one_subfolder_initialization(self):
        self.assertEqual(self.folder_one_subfolder.name, 'example_folder')
        self.assertEqual(self.folder_one_subfolder.nb_files, 0)
        self.assertEqual(self.folder_one_subfolder.nb_folders, 1)

    def test_folder_documents_initialization(self):
        self.assertEqual(self.folder_documents.name, 'example_folder')
        self.assertEqual(self.folder_documents.nb_files, 8)
        self.assertEqual(self.folder_documents.nb_folders, 0)

    def test_empty_folder_initialization(self):
        self.assertEqual(self.empty_folder.name, 'example_folder')
        self.assertEqual(self.empty_folder.nb_files, 0)
        self.assertEqual(self.empty_folder.nb_folders, 0)

    def test_folder_get_content(self):
        # Implement test cases for getting folder content here
        pass

if __name__ == '__main__':
    unittest.main()
