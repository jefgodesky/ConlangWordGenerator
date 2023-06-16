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

    def test_pattern(self, sample, pattern):
        zipped = zip([*sample], [*pattern])
        for comparison in zipped:
            seeking_consonants = comparison[1] == 'C'
            seeking_vowels = comparison[1] == 'V'
            in_consonants = comparison[0] in self.consonants
            in_vowels = comparison[0] in self.vowels
            match_consonant = seeking_consonants and in_consonants
            match_vowel = seeking_vowels and in_vowels
            match_explicit = comparison[0] == comparison[1]
            if not (match_consonant or match_vowel or match_explicit):
                return False
        return True

    @staticmethod
    def pick_random_sound(sounds):
        return random.choice(list(sounds.keys()))
