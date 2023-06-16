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
        self.assertEqual(self.lang.syllables['onset']['incidence'], 75)

    def test_init_load_onset_options(self):
        self.assertEqual(self.lang.syllables['onset']['options'], ['a', 'b'])

    def test_init_load_coda_incidence(self):
        self.assertEqual(self.lang.syllables['coda']['incidence'], 25)

    def test_init_load_coda_options(self):
        self.assertEqual(self.lang.syllables['coda']['options'], ['b', 'c'])

    def test_init_load_syllable_forbidden_patterns(self):
        self.assertEqual(self.lang.syllables['forbidden'], ['CCVCC'])

    def test_init_load_word_max_syllables(self):
        self.assertEqual(self.lang.words['syllables']['max'], 5)

    def test_init_load_word_min_syllables(self):
        self.assertEqual(self.lang.words['syllables']['min'], 1)

    def test_init_load_word_syllables_rerolls(self):
        self.assertEqual(self.lang.words['syllables']['tries'], 3)

    def test_init_load_word_forbidden_patterns(self):
        self.assertEqual(self.lang.words['forbidden'], ['bbc'])

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

    def test_test_syllable_pattern_matches_explicit(self):
        self.assertTrue(self.lang.test_syllable_pattern('abc', 'abc'))

    def test_test_syllable_pattern_fails_wrong_explicit(self):
        self.assertFalse(self.lang.test_syllable_pattern('abc', 'xyz'))

    def test_test_syllable_pattern_matches_consonants(self):
        self.assertTrue(self.lang.test_syllable_pattern('abc', 'aCc'))

    def test_test_syllable_pattern_fails_wrong_consonants(self):
        self.assertFalse(self.lang.test_syllable_pattern('abc', 'Cbc'))

    def test_test_syllable_pattern_matches_vowels(self):
        self.assertTrue(self.lang.test_syllable_pattern('abc', 'Vbc'))

    def test_test_syllable_pattern_fails_wrong_vowels(self):
        self.assertFalse(self.lang.test_syllable_pattern('abc', 'aVc'))

    def test_test_syllable_pattern_all_consonants_and_vowels(self):
        self.assertTrue(self.lang.test_syllable_pattern('abc', 'VCC'))

    def test_test_syllable_pattern_fails_all_consonants_and_vowels(self):
        self.assertFalse(self.lang.test_syllable_pattern('abc', 'CVC'))

    def test_test_syllable_pattern_fails_incomplete_pattern(self):
        self.assertFalse(self.lang.test_syllable_pattern('abc', 'VCCC'))

    def test_pick_onset_certainty(self):
        self.lang.syllables['onset']['incidence'] = 100
        self.assertIn(self.lang.pick_onset(), ['a', 'b'])

    def test_pick_onset_certainly_not(self):
        self.lang.syllables['onset']['incidence'] = 0
        self.assertEqual(self.lang.pick_onset(), '')

    def test_pick_coda_certainty(self):
        self.lang.syllables['coda']['incidence'] = 100
        self.assertIn(self.lang.pick_coda(), ['b', 'c'])

    def test_pick_coda_certainly_not(self):
        self.lang.syllables['coda']['incidence'] = 0
        self.assertEqual(self.lang.pick_coda(), '')

    def test_pick_syllable_element_onset_certainty(self):
        self.lang.syllables['onset']['incidence'] = 100
        self.assertIn(self.lang.pick_syllable_element('onset'), ['a', 'b'])

    def test_pick_syllable_element_onset_certainly_not(self):
        self.lang.syllables['onset']['incidence'] = 0
        self.assertEqual(self.lang.pick_syllable_element('onset'), '')

    def test_pick_syllable_element_coda_certainty(self):
        self.lang.syllables['coda']['incidence'] = 100
        self.assertIn(self.lang.pick_syllable_element('coda'), ['b', 'c'])

    def test_pick_syllable_element_coda_certainly_not(self):
        self.lang.syllables['coda']['incidence'] = 0
        self.assertEqual(self.lang.pick_syllable_element('coda'), '')

    def test_generate_syllable_core(self):
        self.lang.syllables['onset']['incidence'] = 0
        self.lang.syllables['coda']['incidence'] = 0
        self.assertIn(self.lang.generate_syllable(), ['a'])

    def test_generate_syllable_onset_core(self):
        self.lang.syllables['onset']['incidence'] = 100
        self.lang.syllables['coda']['incidence'] = 0
        self.assertIn(self.lang.generate_syllable(), ['aa', 'ba'])

    def test_generate_syllable_core_coda(self):
        self.lang.syllables['onset']['incidence'] = 0
        self.lang.syllables['coda']['incidence'] = 100
        self.assertIn(self.lang.generate_syllable(), ['ab', 'ac'])

    def test_generate_syllable_onset_core_coda(self):
        self.lang.syllables['onset']['incidence'] = 100
        self.lang.syllables['coda']['incidence'] = 100
        self.assertIn(self.lang.generate_syllable(), ['aab', 'aac', 'bab', 'bac'])

    def test_pick_number_syllables_min_max(self):
        syllables = self.lang.pick_number_syllables()
        self.assertGreaterEqual(syllables, self.lang.words['syllables']['min'])
        self.assertLessEqual(syllables, self.lang.words['syllables']['max'])

    def test_generate_word_returns_monosyllabic(self):
        self.lang.syllables['onset']['incidence'] = 100
        self.lang.syllables['onset']['options'] = ['b']
        self.lang.syllables['coda']['incidence'] = 0
        self.lang.words['syllables']['min'] = 1
        self.lang.words['syllables']['max'] = 1
        self.assertEqual(self.lang.generate_word(), 'ba')

    def test_generate_word_returns_multisyllabic(self):
        self.lang.syllables['onset']['incidence'] = 100
        self.lang.syllables['onset']['options'] = ['b']
        self.lang.syllables['coda']['incidence'] = 0
        self.lang.words['syllables']['min'] = 2
        self.lang.words['syllables']['max'] = 2
        self.assertEqual(self.lang.generate_word(), 'baba')

    def test_test_acceptable_syllable_fail(self):
        self.assertFalse(self.lang.test_acceptable_syllable('bbabb'))

    def test_test_acceptable_syllable_pass(self):
        self.assertTrue(self.lang.test_acceptable_syllable('bbab'))