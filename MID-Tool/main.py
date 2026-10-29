import os
import sys
import subprocess
import requests

CURRENT_VERSION = "1.0.0"


def check_and_update():
    # 1. GitHub Release abfragen
    api_url = "https://api.github.com/repos/DEIN_NAME/DEIN_REPO/releases/latest"
    try:
        response = requests.get(api_url, timeout=5)
        if response.status_code != 200:
            return

        data = response.json()
        latest_tag = data.get("tag_name")  # z.B. "v1.1.0"

        if latest_tag and latest_tag != f"v{CURRENT_VERSION}":
            print(f"Update gefunden: {latest_tag}")

            # Suche in den Assets des Releases nach unserer neuen .exe
            download_url = None
            for asset in data.get("assets", []):
                if asset["name"] == "meine_app.exe":
                    download_url = asset["browser_download_url"]
                    break

            if download_url:
                perform_update(download_url)

    except Exception as e:
        print("Update-Fehler:", e)


def perform_update(download_url):
    print("Lade Update herunter...")

    # 2. Neue .exe in den temporären Ordner oder aktuellen Ordner laden
    # (Wir nennen sie vorerst 'update_new.exe')
    new_exe_path = "update_new.exe"

    r = requests.get(download_url, stream=True)
    with open(new_exe_path, "wb") as f:
        for chunk in r.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)

    print("Update heruntergeladen. Starte Updater...")

    current_exe = sys.executable

    batch_content = f"""
        @echo off
        timeout /t 2 /nobreak > nul
        del "{current_exe}"
        move "{new_exe_path}" "{current_exe}"
        start "" "{current_exe}"
        del "%~f0"
        """

    bat_path = "update.bat"
    with open(bat_path, "w") as bat_file:
        bat_file.write(batch_content)

    subprocess.Popen(bat_path, shell=True)
    sys.exit(0)

