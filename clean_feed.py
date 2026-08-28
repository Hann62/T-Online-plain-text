
import urllib.request
from bs4 import BeautifulSoup

url = "https://www.t-online.de/rss.xml"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
html = urllib.request.urlopen(req).read()

soup = BeautifulSoup(html, "xml")

# Alle Bild- und HTML-Tags aus den Beschreibungen löschen
for item in soup.find_all("item"):
    if item.description and item.description.string:
        desc_soup = BeautifulSoup(item.description.string, "html.parser")
        # Löscht alle <img> und <picture> Tags
        for img in desc_soup.find_all(["img", "picture", "figure"]):
            img.decompose()
        item.description.string = desc_soup.get_text()

# Speichert den bereinigten Feed
with open("feed.xml", "wb") as f:
    f.write(soup.prettify(encoding="utf-8"))
