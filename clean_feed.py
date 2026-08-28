import urllib.request
import re

# Nutzt einen Proxy-Abruf, um die IP-Sperre von t-online zu umgehen
url = "https://api.allorigins.win/raw?url=https%3A%2F%2Fwww.t-online.de%2Fnachrichten%2Fid_76883394%2Frss.xml"

req = urllib.request.Request(
    url, 
    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
)

try:
    with urllib.request.urlopen(req) as response:
        content = response.read().decode('utf-8')

    # Entfernt alle Bild-Tags, Bilder-Links und Grafiken aus dem RSS-Text
    content = re.sub(r'&lt;img[^&]*&gt;', '', content)
    content = re.sub(r'<img[^>]*>', '', content)
    content = re.sub(r'&lt;figure.*?&lt;/figure&gt;', '', content, flags=re.DOTALL)
    content = re.sub(r'<figure>.*?</figure>', '', content, flags=re.DOTALL)
    content = re.sub(r'<enclosure[^>]*/>', '', content)
    content = re.sub(r'<media:content[^>]*>.*?</media:content>', '', content, flags=re.DOTALL)
    content = re.sub(r'<media:thumbnail[^>]*/>', '', content)

    # Speichert den sauberen Plain-Text Feed
    with open("feed.xml", "w", encoding="utf-8") as f:
        f.write(content)
        
    print("Feed erfolgreich ohne Bilder erstellt!")

except Exception as e:
    print(f"Fehler: {e}")
