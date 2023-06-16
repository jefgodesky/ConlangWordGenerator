import unittest
from src.language.cls import Language


class TestLanguage(unittest.TestCase):
    def setUp(self):
        self.filename = 'languages/test.yml'
        self.lang = Language(self.filename)

    def set_deterministic_lang(self, number_syllables):
        self.lang.syllables['onset']['incidence'] = 100
        self.lang.syllables['onset']['options'] = ['b']
        self.lang.syllables['coda']['incidence'] = 0
        self.lang.words['syllables']['min'] = number_syllables
        self.lang.words['syllables']['max'] = number_syllables

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

    def test_repr_displays_name(self):
        self.assertEqual(self.lang.__repr__(), '<Language Test>')

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
        self.set_deterministic_lang(1)
        self.assertEqual(self.lang.generate_word(), '/ba/')

    def test_generate_word_returns_multisyllabic(self):
        self.set_deterministic_lang(2)
        self.assertEqual(self.lang.generate_word(), '/ba.ba/')

    def test_test_acceptable_syllable_fail(self):
        self.assertFalse(self.lang.test_acceptable_syllable('bbabb'))

    def test_test_acceptable_syllable_pass(self):
        self.assertTrue(self.lang.test_acceptable_syllable('bbab'))

    def test_generate_word_avoids_forbidden_syllables(self):
        self.set_deterministic_lang(10)
        self.lang.syllables['onset']['options'] = ['b', 'c']
        self.lang.syllables['forbidden'] = ['ca']
        self.assertEqual(self.lang.generate_word(), '/ba.ba.ba.ba.ba.ba.ba.ba.ba.ba/')

    def test_generate_word_avoids_infinite_loop(self):
        self.set_deterministic_lang(2)
        self.lang.syllables['forbidden'] = ['ba']
        self.assertEqual(self.lang.generate_word(), '/ba.ba/')

    def test_transcribe_removes_ipa_symbols(self):
        self.assertEqual(self.lang.transcribe('/ba.ba/'), 'baba')

    def test_get_sound_inventory_returns_all_sounds(self):
        expected = {'bc': 'bc', 'a': 'a', 'b': 'b', 'c': 'c'}
        self.assertEqual(self.lang.get_sound_inventory(), expected)

    def test_get_sound_inventory_sorted(self):
        expected = 'bcabc'
        actual = ''.join(self.lang.get_sound_inventory().keys())
        self.assertEqual(expected, actual)

    def test_transcribe_handles_ipa_symbols(self):
        self.lang.consonants = {'ʃ': 'sh'}
        self.assertEqual(self.lang.transcribe('/ʃa/'), 'sha')

    def test_transcribe_handles_ipa_clusters(self):
        self.lang.consonants = {'ʃ': 'sh', 't': 't'}
        self.lang.clusters = {'tʃ': 'ch'}
        self.assertEqual(self.lang.transcribe('/ʃa.ta.tʃa/'), 'shatacha')

    def test_test_acceptable_words_fail(self):
        self.assertFalse(self.lang.test_acceptable_word('abbca'))

    def test_test_acceptable_words_pass(self):
        self.assertTrue(self.lang.test_acceptable_word('abba'))

    def test_generate_words_returns_list_with_one_word(self):
        self.set_deterministic_lang(2)
        self.assertEqual(self.lang.generate_words(1), ['/ba.ba/'])

    def test_test_acceptable_words_ignore_ipa_markers(self):
        self.assertFalse(self.lang.test_acceptable_word('/ab.bca/'))

    def test_generate_words_does_not_generate_unacceptable_words(self):
        self.set_deterministic_lang(2)
        self.lang.words['forbidden'] = ['bab']
        self.assertEqual(self.lang.generate_words(1), [])

    def test_create_csv_returns_csv(self):
        self.lang.consonants = {'ʃ': 'sh', 't': 't'}
        self.lang.clusters = {'tʃ': 'ch'}
        expected = '"IPA","Orthography"\n"/ba.ba/","baba"\n"/tʃa.tʃa/","chacha"'
        actual = self.lang.create_csv(['/ba.ba/', '/tʃa.tʃa/'])
        self.assertEqual(expected, actual)
