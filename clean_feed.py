import urllib.request
import re

# Diese direkte Quelle hat keine 5-Sekunden-Sperre
url = "https://feeds.t-online.de/rss/nachrichten"

req = urllib.request.Request(
    url, 
    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:125.0) Gecko/20100101 Firefox/125.0'}
)

try:
    with urllib.request.urlopen(req) as response:
        content = response.read().decode('utf-8')

    # Entfernt lückenlos alle Bild-Tags und Medien-Elemente aus den Artikeln
    content = re.sub(r'&lt;img[^&]*&gt;', '', content)
    content = re.sub(r'<img[^>]*>', '', content)
    content = re.sub(r'&lt;figure.*?&lt;/figure&gt;', '', content, flags=re.DOTALL)
    content = re.sub(r'<figure>.*?</figure>', '', content, flags=re.DOTALL)
    content = re.sub(r'<enclosure[^>]*/>', '', content)
    content = re.sub(r'<media:[^>]*/>', '', content)
    content = re.sub(r'<media:[^>]*>.*?</media:[^>]*>', '', content, flags=re.DOTALL)

    # Speichert den sauberen Plain-Text Feed
    with open("feed.xml", "w", encoding="utf-8") as f:
        f.write(content)
        
    print("Feed ohne Bilder erfolgreich generiert!")

except Exception as e:
    print(f"Fehler: {e}")
