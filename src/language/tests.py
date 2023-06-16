import unittest
from src.language.cls import Language


class TestLanguage(unittest.TestCase):
    def setUp(self):
        self.filename = 'test.yml'
        self.lang = Language(self.filename)

    def test_init_load_name(self):
        self.assertEqual(self.lang.name, 'Test')

    def test_init_load_vowels(self):
        self.assertEqual(len(self.lang.vowels), 5)

    def test_init_load_consonants(self):
        self.assertEqual(len(self.lang.consonants), 14)

    def test_init_load_clusters(self):
        self.assertEqual(len(self.lang.clusters), 13)

    def test_init_load_onset_incidence(self):
        self.assertEqual(self.lang.syllables['onset']['incidence'], 0.65)

    def test_init_load_onset_options(self):
        self.assertEqual(len(self.lang.syllables['onset']['options']), 21)

    def test_init_load_syllable_forbidden_patterns(self):
        self.assertEqual(len(self.lang.syllables['forbidden']), 1)

    def test_get_all_consonant_options(self):
        self.assertEqual(len(self.lang.get_all_consonant_options()), 27)

    def test_pick_random_sound(self):
        sounds = {'a': 1, 'b': 2}
        self.assertIn(Language.pick_random_sound(sounds), ['a', 'b'])
