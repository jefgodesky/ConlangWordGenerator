import unittest
from src.language.cls import Language


class TestLanguage(unittest.TestCase):
    def setUp(self):
        self.filename = 'test.yml'
        self.lang = Language(self.filename)

    def test_init_load_name(self):
        self.assertEqual(self.lang.name, 'Test')

    def test_init_load_vowels(self):
        self.assertEqual(len(self.lang.vowels), 1)

    def test_init_load_consonants(self):
        self.assertEqual(len(self.lang.consonants), 2)

    def test_init_load_clusters(self):
        self.assertEqual(len(self.lang.clusters), 1)

    def test_init_load_onset_incidence(self):
        self.assertEqual(self.lang.syllables['onset']['incidence'], 0.5)

    def test_init_load_onset_options(self):
        self.assertEqual(len(self.lang.syllables['onset']['options']), 3)

    def test_init_load_syllable_forbidden_patterns(self):
        self.assertEqual(len(self.lang.syllables['forbidden']), 1)

    def test_get_all_consonant_options(self):
        self.assertEqual(len(self.lang.get_all_consonant_options()), 3)

    def test_pick_random_sound(self):
        sounds = {'a': 1, 'b': 2}
        self.assertIn(Language.pick_random_sound(sounds), ['a', 'b'])
