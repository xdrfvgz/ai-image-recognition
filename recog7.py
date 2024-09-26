import base64
import requests
import os
import sys
import subprocess
import time

# Funktion zur Protokollierung des Ergebnisses
def protokolliere_ergebnis(original_image_path, search_term, ergebnis, full_prompt):
    log_message = f"{original_image_path}: Suchbegriff -> {search_term}, Ergebnis -> {ergebnis}, Prompt -> {full_prompt}\n"
    with open("log.txt", "a") as logfile:
        logfile.write(log_message)
    print(f"Log geschrieben: {log_message}")

# Funktion zum Kodieren des Bildes
def encode_image(image_path):
    try:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    except FileNotFoundError:
        print(f"Fehler: Datei {image_path} nicht gefunden.")
        sys.exit(1)

# API-Schlüssel prüfen
def get_api_key():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("Bitte setzen Sie die Umgebungsvariable 'OPENAI_API_KEY' mit Ihrem API-Schlüssel.")
        sys.exit(1)
    return api_key

# API-Anfrage senden
def send_request(api_key, base64_image, full_prompt):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    
    payload = {
        "model": "chatgpt-4o-latest",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": full_prompt
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                ]
            }
        ],
        "max_tokens": 300
    }
    
    try:
        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
        response.raise_for_status()  # Überprüft auf HTTP-Fehler
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Fehler bei der API-Anfrage: {e}")
        sys.exit(1)

# Ergebnis verarbeiten und Befehl ausführen
def process_response(result, image_path, search_term, full_prompt, command):
    response_text = result.get("choices", [{}])[0].get("message", {}).get("content", "")
    print(f"Antwort von der API: {response_text}")
    
    if "ALARM" in response_text:
        protokolliere_ergebnis(image_path, search_term, "ALARM", full_prompt)
        print("ALARM erkannt. Ausführen des Befehls...")
        try:
            subprocess.run(command, shell=True, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Fehler beim Ausführen des Befehls: {e}")
    else:
        protokolliere_ergebnis(image_path, search_term, "SAFE", full_prompt)
        print("Alles sicher. Kein Alarm.")

# Hauptfunktion
def main():
    # Argumente prüfen
    if len(sys.argv) < 4:
        print("Usage: python image-recognition6.py <Bildpfad> <Suchbegriff> <Befehl>")
        sys.exit(1)

    # Bildpfad, Suchbegriff und Befehl aus den Argumenten
    image_path = sys.argv[1]
    search_term = sys.argv[2]
    command = sys.argv[3]

    # API-Schlüssel holen
    api_key = get_api_key()

    # Bild in Base64 umwandeln
    base64_image = encode_image(image_path)

    # Definierter Prompt
    full_prompt = f"Zu suchende(s) Objekt(e): {search_term}; Wenn du alle gesuchten Objekte nach exakt der Beschreibung siehst, schreibst du [ALARM], ansonsten [SAFE]."

    # Log den gesamten Prompt
    print(f"Übergebener Prompt: {full_prompt}")

    # Zeitmessung starten
    start = time.time()

    # API-Anfrage senden und verarbeiten
    result = send_request(api_key, base64_image, full_prompt)
    process_response(result, image_path, search_term, full_prompt, command)

    # Zeitmessung beenden
    end = time.time()
    elapsed_time = end - start
    print(f"Die Anfrage dauerte {elapsed_time:.2f} Sekunden.")

# Skript ausführen
if __name__ == "__main__":
    main()
