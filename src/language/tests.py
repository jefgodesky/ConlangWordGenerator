import unittest
from src.language.cls import Language


class TestLanguage(unittest.TestCase):
    def setUp(self):
        self.filename = 'test.yml'
        self.lang = Language(self.filename)

    def test_init_load_name(self):
        self.assertEqual(self.lang.name, 'Test')

    def test_init_load_vowels(self):
        self.assertEqual(self.lang.vowels, {'a': 'a'})

    def test_init_load_consonants(self):
        self.assertEqual(self.lang.consonants, {'b': 'b', 'c': 'c'})

    def test_init_load_clusters(self):
        self.assertEqual(self.lang.clusters, {'bc': 'bc'})

    def test_init_load_onset_incidence(self):
        self.assertEqual(self.lang.syllables['onset']['incidence'], 0.5)

    def test_init_load_onset_options(self):
        self.assertEqual(self.lang.syllables['onset']['options'], ['a', 'b'])

    def test_init_load_syllable_forbidden_patterns(self):
        self.assertEqual(self.lang.syllables['forbidden'], ['CCVCC'])

    def test_get_all_consonant_options(self):
        self.assertEqual(self.lang.get_all_consonant_options(), {'b': 'b', 'c': 'c', 'bc': 'bc'})

    def test_pick_random_sound(self):
        sounds = {'a': 1, 'b': 2}
        self.assertIn(Language.pick_random_sound(sounds), ['a', 'b'])

    def test_pick_random_consonant_option(self):
        options = self.lang.get_all_consonant_options().keys()
        self.assertIn(self.lang.pick_random_consonant_option(), options)

    def test_pick_random_vowel(self):
        vowels = self.lang.vowels.keys()
        self.assertIn(self.lang.pick_random_vowel(), vowels)

    def test_test_pattern_matches_explicit(self):
        self.assertTrue(self.lang.test_pattern('abc', 'abc'))

    def test_test_pattern_fails_wrong_explicit(self):
        self.assertFalse(self.lang.test_pattern('abc', 'xyz'))

    def test_test_pattern_matches_consonants(self):
        self.assertTrue(self.lang.test_pattern('abc', 'aCc'))

    def test_test_pattern_fails_wrong_consonants(self):
        self.assertFalse(self.lang.test_pattern('abc', 'Cbc'))
