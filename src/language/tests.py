import unittest
from src.language.cls import Language


class TestLanguage(unittest.TestCase):
    def setUp(self):
        self.filename = 'test.yml'
        self.lang = Language(self.filename)

    def test_init_load(self):
        self.assertIsNotNone(self.lang.contents)
        self.assertEqual(self.lang.contents[1], 'name: Test\n')
