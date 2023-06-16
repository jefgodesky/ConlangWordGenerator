import random
import yaml

MAX_ATTEMPTS = 50


class Language:
    def __init__(self, filename):
        with open(filename) as file:
            contents = yaml.safe_load(file)
        self.name = contents['name']
        self.vowels = contents['vowels']
        self.consonants = contents['consonants']
        self.clusters = contents['clusters']
        self.syllables = contents['syllables']
        self.words = contents['words']

    def get_all_consonant_options(self):
        return dict(self.consonants, **self.clusters)

    def get_sound_inventory(self):
        inventory = dict(self.vowels, **self.consonants, **self.clusters)
        inventory_list = sorted(list(inventory.items()), key=lambda key: len(key[0]), reverse=True)
        return {sound[0]: sound[1] for sound in inventory_list}

    def pick_random_vowel(self):
        return Language.pick_random_sound(self.vowels)

    def pick_random_consonant_option(self):
        return Language.pick_random_sound(self.get_all_consonant_options())

    def pick_onset(self):
        return self.pick_syllable_element('onset')

    def pick_coda(self):
        return self.pick_syllable_element('coda')

    def pick_syllable_element(self, element):
        if random.choice(range(1, 101)) <= self.syllables[element]['incidence']:
            return random.choice(self.syllables[element]['options'])
        return ''

    def pick_number_syllables(self):
        minimum = self.words['syllables']['min']
        maximum = self.words['syllables']['max'] + 1
        return random.choice(range(minimum, maximum))

    def generate_syllable(self):
        return self.pick_onset() + Language.pick_random_sound(self.vowels) + self.pick_coda()

    def generate_word(self):
        number_syllables = self.pick_number_syllables()
        syllables = []
        attempts = 0
        while len(syllables) < number_syllables:
            syllable = self.generate_syllable()
            attempts += 1
            if self.test_acceptable_syllable(syllable) or attempts >= MAX_ATTEMPTS:
                syllables.append(syllable)
        return f"/{'.'.join(syllables)}/"

    def generate_words(self, number):
        words = []
        while len(words) < number:
            word = self.generate_word()
            words.append(word)
        return words

    def transcribe(self, ipa):
        transcription = ipa
        inventory = self.get_sound_inventory()
        for (ipa, orthography) in inventory.items():
            transcription = transcription.replace(ipa, orthography)
        return transcription.replace('/', '').replace('.', '')

    def test_syllable_pattern(self, sample, pattern):
        if len(sample) != len(pattern):
            return False

        zipped = zip([*sample], [*pattern])
        for (letter, measure) in zipped:
            options = self.consonants if measure == 'C' else self.vowels if measure == 'V' else measure
            if not (letter in options):
                return False

        return True

    def test_acceptable_syllable(self, syllable):
        for pattern in self.syllables['forbidden']:
            if self.test_syllable_pattern(syllable, pattern):
                return False
        return True

    def test_acceptable_word(self, word):
        for pattern in self.words['forbidden']:
            if pattern in word.replace('/', '').replace('.', ''):
                return False
        return True

    @staticmethod
    def pick_random_sound(sounds):
        return random.choice(list(sounds.keys()))
