import os
import json
import uuid
from collections import defaultdict

# Variablen zur Steuerung des Skripts
data_dir = "data"  # Pfad zu 'data'
html_output_dir = "docs"
mapping_output_file = "mapping.json"
manual_entries_file = "manual_entries.yaml"
show_remarks = True
show_warnings = False

# Funktion zum Erstellen einer UUID
def generate_uuid():
    return str(uuid.uuid4())

# Funktion zum Erstellen der Config
def create_config():
    profiles_to_compare = []
    file_dict = defaultdict(list)
    
    print("Durchsuche das 'data' Verzeichnis nach JSON-Dateien...")

    # Durchlaufe alle Unterordner im 'data' Verzeichnis
    for subdir, _, files in os.walk(data_dir):
        print(f"Verarbeite Unterordner: {subdir}")
        
        # Sammle die JSON-Dateien für die jeweilige Version
        for file in files:
            if file.endswith('.json') and "|" in file:  # Nur Dateien mit einer Version
                base_name, version = file.rsplit('|', 1)
                # Logge den Basisnamen und die Version, um sicherzustellen, dass sie korrekt extrahiert werden
                print(f"Gefundene Datei: {file} (Basisname: {base_name}, Version: {version})")
                file_dict[base_name].append((version, os.path.join(subdir, file)))

    # Jetzt, nachdem alle Dateien gesammelt wurden, die Versionen vergleichen
    for base_name, file_versions in file_dict.items():
        print(f"Überprüfe Basisname: {base_name} mit {len(file_versions)} Versionen.")
        
        # Wenn es mehr als eine Version gibt, dann vergleichen und Paare erstellen
        if len(file_versions) >= 2:
            file_versions.sort(key=lambda x: x[0])  # Sortiere nach Version

            # Erstelle Mappings für alle Paare von Versionen
            for i in range(len(file_versions) - 1):
                source_file = file_versions[i][1]
                source_version = file_versions[i][0]
                target_file = file_versions[i+1][1]
                target_version = file_versions[i+1][0]

                # Entferne 'data/' aus dem Pfad, wenn es zweimal vorkommt
                source_file = source_file.replace(f'{data_dir}/', '')
                target_file = target_file.replace(f'{data_dir}/', '')

                print(f"Erstelle Mapping: {base_name} {source_version} -> {target_version}")
                
                # Erstelle das Mapping
                profile = {
                    "id": generate_uuid(),
                    "version": "1.0.0",
                    "status": "draft",
                    "mappings": {
                        "sourceprofiles": [
                            {
                                "file": source_file,
                                "version": source_version,
                                "simplifier_url": f"https://simplifier.net/packages/{base_name}/{source_version}/files",
                                "file_download_url": f"https://simplifier.net/ui/packagefile/downloadas?packageFileId=xxxx&format=json"
                            }
                        ],
                        "targetprofile": {
                            "file": target_file,
                            "version": target_version,
                            "simplifier_url": f"https://simplifier.net/{base_name}/{target_version}",
                            "file_download_url": f"https://simplifier.net/{base_name}/{target_version}/$downloadsnapshot?format=json"
                        }
                    }
                }
                profiles_to_compare.append(profile)
        else:
            print(f"Nicht genügend Versionen für {base_name}. Dateien vorhanden: {len(file_versions)}")

    # Zeige die Anzahl der gefundenen Profile
    print(f"Gesamtzahl der gefundenen Profile: {len(profiles_to_compare)}")

    # Erstelle das config.json
    if profiles_to_compare:
        config_data = {
            "manual_entries_file": manual_entries_file,
            "data_dir": data_dir,
            "html_output_dir": html_output_dir,
            "mapping_output_file": mapping_output_file,
            "show_remarks": show_remarks,
            "show_warnings": show_warnings,
            "profiles_to_compare": profiles_to_compare
        }

        # Schreibe die Konfiguration in eine Datei
        with open('config.json', 'w', encoding='utf-8') as f:
            json.dump(config_data, f, indent=4)
        print("config.json wurde erfolgreich erstellt.")
    else:
        print("Keine Profile zum Vergleichen gefunden. config.json wurde nicht erstellt.")

# Starte das Skript
if __name__ == "__main__":
    create_config()