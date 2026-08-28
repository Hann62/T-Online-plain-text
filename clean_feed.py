import urllib.request
from bs4 import BeautifulSoup

url = "https://www.t-online.de/rss.xml"
# Simuliert einen normalen Web-Browser, damit t-online die Anfrage nicht blockiert
req = urllib.request.Request(
    url, 
    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
)

try:
    xml_data = urllib.request.urlopen(req).read()
    soup = BeautifulSoup(xml_data, "xml")

    # Entfernt alle Bilder und Multimedia-Tags aus der Beschreibung
    for item in soup.find_all("item"):
        if item.description and item.description.string:
            desc_soup = BeautifulSoup(item.description.string, "html.parser")
            for img in desc_soup.find_all(["img", "picture", "figure", "iframe"]):
                img.decompose()
            item.description.string = desc_soup.get_text()

    # Erstellt die finale feed.xml
    with open("feed.xml", "wb") as f:
        f.write(soup.prettify(encoding="utf-8"))
    print("feed.xml erfolgreich erstellt!")

except Exception as e:
    print(f"Fehler beim Abrufen: {e}")
