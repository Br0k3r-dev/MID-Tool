# _____________________________________
# Sprachen laden aus JSON Dateien unter ../Languages
# _____________________________________

import json
from pathlib import Path


class Translator:
    def __init__(self, language_folder="Languages", start_language="en"):
        self.language_path = Path(language_folder)
        self.current_language = start_language
        self.texts = {}
        self.load_lang(start_language)

    # _____________________________________
    # Übersetzungs Mehtode, läd Übersetzungen aus den jeweiligen Übersetzungsdateien
    # _____________________________________

    def load_lang(self, lang: str):
        self.current_language = lang
        file_path = self.language_path / f"{lang}.json"
        if not self.language_path.exists():
            print("Keine Sprach-Json bei", self.language_path, "gefunden")
            return {"error": "File not found"}

        with open(file_path, "r", encoding="utf-8") as file:
            self.texts = json.load(file)
            print("Sprache:", self.current_language, "geladen")

    def t(self, key: str, **kwargs) -> str:
        text = self.texts.get(key, key)

        if kwargs:
            try:
                return text.format(**kwargs)
            except KeyError:
                return text
        return text

translator = Translator()