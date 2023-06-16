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

    @staticmethod
    def pick_random_sound(sounds):
        return random.choice(list(sounds.keys()))
