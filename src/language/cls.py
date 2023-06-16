import random
import yaml


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

    def generate_syllable(self):
        return self.pick_onset() + Language.pick_random_sound(self.vowels) + self.pick_coda()

    def pick_number_syllables(self):
        minimum = self.words['syllables']['min']
        maximum = self.words['syllables']['max'] + 1
        return random.choice(range(minimum, maximum))

    def test_syllable_pattern(self, sample, pattern):
        if len(sample) != len(pattern):
            return False

        zipped = zip([*sample], [*pattern])
        for (letter, measure) in zipped:
            options = self.consonants if measure == 'C' else self.vowels if measure == 'V' else measure
            if not (letter in options):
                return False

        return True

    @staticmethod
    def pick_random_sound(sounds):
        return random.choice(list(sounds.keys()))
