import os
import json

# Durchlaufe alle Dateien im aktuellen Ordner
for filename in os.listdir():
    # Überprüfe, ob die Datei eine .json-Datei ist
    if filename.endswith('.json'):
        print(f"Verarbeite Datei: {filename}")
        try:
            # Versuche, die JSON-Datei zu laden
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
                # Überprüfe, ob das "snapshot"-Schlüsselwort im JSON-Dateninhalt existiert
                if 'snapshot' in data:
                    # Überprüfe, ob das "version"-Feld existiert
                    if 'version' in data:
                        version = data['version']
                        print(f"Version gefunden: {version} in {filename}")
                        
                        # Erstelle den neuen Dateinamen
                        base_name = filename[:-5]  # Entfernt '.json' vom Dateinamen
                        new_filename = f"{base_name}|{version}.json"
                        
                        # Benenne die Datei um
                        os.rename(filename, new_filename)
                        print(f"Datei umbenannt: {filename} -> {new_filename}")
                    else:
                        print(f"Keine Version gefunden in {filename}. Überspringe die Datei.")
                else:
                    print(f"Kein 'snapshot' gefunden in {filename}. Überspringe die Datei.")
        except json.JSONDecodeError:
            print(f"Fehler: {filename} ist keine gültige JSON-Datei.")
        except Exception as e:
            print(f"Unbekannter Fehler bei der Datei {filename}: {e}")
    else:
        print(f"Überspringe Datei: {filename} (nicht .json)")