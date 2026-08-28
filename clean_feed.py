import subprocess
import re

url = "https://www.t-online.de/nachrichten/id_76883394/rss.xml"

# Simuliert einen vollständigen Desktop-Browser inklusive aller Head-Informationen
cmd = [
    "curl", "-s", "-L",
    "-A", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "-H", "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "-H", "Accept-Language: de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7",
    "-H", "Sec-Fetch-Dest: document",
    "-H", "Sec-Fetch-Mode: navigate",
    "-H", "Sec-Fetch-Site: none",
    "-H", "Upgrade-Insecure-Requests: 1",
    url
]

try:
    result = subprocess.run(cmd, capture_output=True, text=True, check=True)
    content = result.stdout

    # Prüfen, ob der tatsächliche RSS-Inhalt angekommen ist
    if "<rss" in content or "<feed" in content:
        # Säubere alle HTML-Bilder, Abbildungen und Medien-Tags
        content = re.sub(r'&lt;img[^&]*&gt;', '', content)
        content = re.sub(r'<img[^>]*>', '', content)
        content = re.sub(r'&lt;figure.*?&lt;/figure&gt;', '', content, flags=re.DOTALL)
        content = re.sub(r'<figure>.*?</figure>', '', content, flags=re.DOTALL)
        content = re.sub(r'<enclosure[^>]*/>', '', content)
        content = re.sub(r'<media:[^>]*/>', '', content)
        content = re.sub(r'<media:[^>]*>.*?</media:[^>]*>', '', content, flags=re.DOTALL)

        with open("feed.xml", "w", encoding="utf-8") as f:
            f.write(content)
        print("Erfolg: Feed ohne Bilder gespeichert!")
    else:
        print("Sicherheitsseite empfangen, versuche erneuten Abruf...")

except Exception as e:
    print(f"Fehler beim Abruf: {e}")
