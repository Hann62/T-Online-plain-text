import urllib.request
import re

url = "https://www.t-online.de/nachrichten/id_76883394/rss.xml"

req = urllib.request.Request(
    url, 
    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
)

try:
    with urllib.request.urlopen(req) as response:
        content = response.read().decode('utf-8')

    # Entfernt alle <img>, <picture>, <figure> Tags samt Inhalt per Textfilter
    content = re.sub(r'<img[^>]*>', '', content)
    content = re.sub(r'<picture>.*?</picture>', '', content, flags=re.DOTALL)
    content = re.sub(r'<figure>.*?</figure>', '', content, flags=re.DOTALL)

    # Speichert die bereinigte feed.xml
    with open("feed.xml", "w", encoding="utf-8") as f:
        f.write(content)
        
    print("feed.xml erfolgreich erstellt!")

except Exception as e:
    print(f"Fehler: {e}")
    # Erstellt eine Notfall-Datei, damit Git nicht abstürzt
    with open("feed.xml", "w", encoding="utf-8") as f:
        f.write("<?xml version=\"1.0\"?><rss version=\"2.0\"><channel><title>Fehler</title></channel></rss>")
except Exception as e:
    print(f"Fehler beim Abrufen: {e}")
