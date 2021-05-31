from argostranslate import package, translate
from os.path import (
    normpath,
    join,
    dirname,
    abspath
)

class Translator:
    def __init__(self, path=normpath(join(dirname(abspath(__file__)), '../data', 'translate-en_ru-1_1.argosmodel'))):
        self.langs = self.get_installed()
        if 'English' not in self.langs or 'Russian' not in self.langs:
            package.install_from_path(path)
            self.langs = self.get_installed()
        self.en_ru = self.langs['English'].get_translation(self.langs['Russian'])
        self.ru_en = self.langs['Russian'].get_translation(self.langs['English'])

    def get_installed(self):
        return {
            str(s): s
            for s in translate.get_installed_languages()
        }

    def translate_en_ru(self, text: str) -> str:
        return self.en_ru.translate(text)

    def translate_ru_en(self, text: str) -> str:
        return self.ru_en.translate(text)
