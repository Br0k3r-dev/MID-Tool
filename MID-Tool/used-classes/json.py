#_____________________________________
# JSON lesen / schreiben Klassen
#_____________________________________

import json
from pathlib import Path


class JsonStorage:
    def __init__(self, json_path: str | Path):
        self.json_path = Path(json_path)

    # _____________________________________
    # Speicher Methode, speichert Dictionary als JSON, erstellt ordner falls nicht vorhanden
    # _____________________________________

    def save(self, data: dict):
        tmp_path = self.json_path.with_suffix(".tmp")
        self.tmp_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.json_path, "w", encoding="utf-8") as file:
            print("Schreibe Datei:", file)
            json.dump(data, file, ensure_ascii=False, indent=4)
            tmp_path.replace(self.json_path)

    # _____________________________________
    # Lade Methode, läd Daten aus der Datei, leeres Dictionary falls keine vorhanden ist
    # _____________________________________

    def load(self) -> dict:
        if not self.json_path.exists():
            print("Keine Json bei", self.json_path, "gefunden")
            return {"error": "File not found"}

        with open(self.json_path, "r", encoding="utf-8") as file:
            return json.load(file)
