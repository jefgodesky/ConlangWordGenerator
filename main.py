import os

from src.language.cls import Language


def load_languages(lang_dir):
    lang_list = []
    for filepath in os.listdir(lang_dir):
        if os.path.isfile(os.path.join(lang_dir, filepath)) and filepath.endswith('.yml') and filepath != 'test.yml':
            lang = Language(f'{lang_dir}/{filepath}')
            lang_list.append(lang)
    return lang_list


if __name__ == '__main__':
    languages = load_languages('languages')
    for lang in languages:
        print(lang.name)
