class Language:
    def __init__(self, filename):
        with open(filename) as file:
            self.contents = file.readlines()
