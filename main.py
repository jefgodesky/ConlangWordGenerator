import os
import datetime
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


def create_csv_file(name, content):
    now = datetime.datetime.now()
    timestamp = now.strftime('%Y-%m-%d-%H-%M-%S')
    filename = f'generated/{name.lower()}-{timestamp}.csv'
    with open(filename, 'w') as file:
        file.write(content)


if __name__ == '__main__':
    languages = load_languages('languages')
    options = [
        inquirer.List('language',
                      message='Language',
                      choices=list(map(lambda language: language.name, languages))
                      ),
        inquirer.Text('words',
                      message='Number of words to generate',
                      validate=lambda _, x: x.isdigit())
    ]
    answers = inquirer.prompt(options)

    language = get_language(answers['language'], languages)
    words = language.generate_words(int(answers['words']))
    csv = language.create_csv(words)

    create_csv_file(language.name, csv)
