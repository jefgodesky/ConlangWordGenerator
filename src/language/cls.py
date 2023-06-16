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

    def get_all_consonant_options(self):
        return dict(self.consonants, **self.clusters)

    def pick_random_vowel(self):
        return Language.pick_random_sound(self.vowels)

    def pick_random_consonant_option(self):
        return Language.pick_random_sound(self.get_all_consonant_options())

    def pick_onset(self):
        if random.choice(range(1, 101)) <= self.syllables['onset']['incidence']:
            return random.choice(self.syllables['onset']['options'])
        return ''

    def pick_coda(self):
        return random.choice(self.syllables['coda']['options'])

    def test_pattern(self, sample, pattern):
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
