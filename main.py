import os
import inquirer

from src.language.cls import Language


def load_languages(lang_dir):
    lang_list = []
    for filepath in os.listdir(lang_dir):
        if os.path.isfile(os.path.join(lang_dir, filepath)) and filepath.endswith('.yml') and filepath != 'test.yml':
            lang = Language(f'{lang_dir}/{filepath}')
            lang_list.append(lang)
    return lang_list


def get_language(choice, lang_list):
    for lang in lang_list:
        if choice == lang.name:
            return lang
    return None



if __name__ == '__main__':
    languages = load_languages('languages')
    options = [
        inquirer.List('language',
                      message='Pick a language:',
                      choices=list(map(lambda language: language.name, languages))
                      ),
        inquirer.Text('words',
                      message='Words to generate: ',
                      validate=lambda _, x: x.isdigit())
    ]
    answers = inquirer.prompt(options)

    language = get_language(answers['language'], languages)
    words = language.generate_words(int(answers['words']))
    csv = language.create_csv(words)
