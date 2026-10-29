#_____________________________________
# SQL lesen / schreiben Klassen
#_____________________________________

import os
from pathlib import Path

#_____________________________________
# erst SQL-Cipher laden, falls nicht, dann SQL
#_____________________________________

try:
    from sqlcipher3 import dbapi2 as sqlite3
    print("SQL Cipher wurde geladen")
except ImportError:
    print("SQL Cipher nicht geladen, lade SQL")
    import sqlite3
    print("SQL wurde geladen")


class SQLStorage:
    def __init__(self, db_path: str | Path):
        self.db_path = Path(db_path)
        self.password = password

        # _____________________________________
        # erstelle Ordner falls nicht vorhanden
        # _____________________________________

        self.db_path.parent.mkdir(parents=True, exist_ok=True)

    # _____________________________________
    # Verbindungs Mothode, verbindet und loggt sich ein
    # _____________________________________

    def connect(self):
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()

        if self.password:
            cursor.execute(f"PRAGMA key = '{self.password}';")

        return connection, cursor

    # _____________________________________
    # Ausführungs Methode, schreibt in die SQL
    # _____________________________________

    def execute(self, sql_command: str, parameter: tuple = ()):
        connection, cursor = self.connect()
        try:
            cursor.execute(sql_command, parameter)
            connection.commit()
        finally:
            connection.close()

    # _____________________________________
    # Anfrage Methode, liest aus der SQL
    # _____________________________________

    def query(self, sql_command: str, parameter: tuple = ()) -> list:
        connection, cursor = self.connect()
        try:
            cursor.execute(sql_command, parameter)
            return cursor.fetchall()
        finally:
            connection.close()
