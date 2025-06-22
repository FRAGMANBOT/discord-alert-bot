import requests
import time
import os

# Ton webhook Discord
WEBHOOK_URL = "https://discord.com/api/webhooks/1386304841189687478/DHjvYOFh3WEx6p0L7kVYsLMhUeB46viD8cqnEQx2nAIbzbg5eAMAwdLCUbCaK1l6S4Li"

# Mots-clés critiques à surveiller
KEYWORDS = [
    "nuclear", "war", "invasion", "explosion", "missile", "earthquake", "tsunami", "eruption",
    "attack", "strike", "military escalation", "mobilization", "bombing", "airstrike", "biohazard",
    "pandemic", "hurricane", "flood", "fire", "evacuation", "chemical", "crisis", "blackout",
    "Canada", "Québec", "USA", "Russia", "Iran", "Israel", "WW3", "World War"
]

# Fonction pour extraire les titres récents via un flux RSS de Google News
def get_latest_news():
    try:
        rss_url = "https://news.google.com/rss?hl=en&gl=CA&ceid=CA:en"
        response = requests.get(rss_url, timeout=10)
        response.raise_for_status()
        return response.text
    except Exception as e:
        print(f"[Erreur] Impossible de récupérer les nouvelles : {e}")
        return ""

# Fonction pour filtrer les nouvelles critiques
def extract_alerts(rss_content):
    import xml.etree.ElementTree as ET
    root = ET.fromstring(rss_content)
    alerts = []

    for item in root.findall(".//item"):
        title = item.find("title").text
        link = item.find("link").text

        if any(keyword.lower() in title.lower() for keyword in KEYWORDS):
            alerts.append((title, link))
    return alerts

# Envoi d'une alerte sur Discord
def send_alert(title, link):
    message = f"🚨 **ALERTE CRITIQUE**\n\n**{title}**\n{link}"
    try:
        requests.post(WEBHOOK_URL, json={"content": message})
        print(f"[Envoyé] {title}")
    except Exception as e:
        print(f"[Erreur d'envoi] {e}")

# Historique des titres pour éviter les doublons
sent_titles = set()

# Boucle principale
while True:
    rss = get_latest_news()
    if rss:
        alerts = extract_alerts(rss)
        for title, link in alerts:
            if title not in sent_titles:
                send_alert(title, link)
                sent_titles.add(title)

    # Attente de 5 minutes avant le prochain check
    time.sleep(300)
