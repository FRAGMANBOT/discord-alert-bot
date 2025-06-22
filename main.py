import requests
import time
import os
import xml.etree.ElementTree as ET

# Ton webhook Discord
WEBHOOK_URL = "https://discord.com/api/webhooks/xxxxxxxxx"  # Remplace par ton vrai lien

# Mots-clés critiques à surveiller
KEYWORDS = [
    "nucléaire", "war", "invasion", "explosion", "escalade", "attentat", "tremblement", "earthquake",
    "tsunami", "blackout", "mobilisation", "iran", "usa", "israel", "bombe", "crise", "missile",
    "poutine", "otan", "attaque", "armée", "guerre", "militaire", "canada", "québec", "russie",
    "corée", "iran", "israel", "3e guerre mondiale", "WW3", "World War"
]

# Flux RSS Google Actualités (modifie ici si tu veux des sources supplémentaires)
RSS_URL = "https://news.google.com/rss/search?q=france+monde&hl=fr&gl=FR&ceid=FR:fr"

# Fonction pour extraire les titres du flux RSS
def get_latest_news():
    try:
        response = requests.get(RSS_URL)
        response.raise_for_status()
        root = ET.fromstring(response.content)
        return root
    except Exception as e:
        print(f"Erreur lors de la récupération des nouvelles : {e}")
        return None

# Fonction pour filtrer les titres selon les mots-clés
def extract_alerts(rss_root):
    alerts = []
    for item in rss_root.findall(".//item"):
        title = item.find("title").text
        link = item.find("link").text
        if any(keyword.lower() in title.lower() for keyword in KEYWORDS):
            alerts.append((title, link))
    return alerts

# Fonction pour envoyer une alerte sur Discord
def send_alert(title, link):
    message = {"content": f"🚨 **ALERTE CRITIQUE** 🚨\n\n{title}\n{link}"}
    try:
        response = requests.post(WEBHOOK_URL, json=message)
        print(f"Envoyé : {title}")
    except Exception as e:
        print(f"Erreur d'envoi : {e}")

# Pour ne pas renvoyer les mêmes nouvelles en boucle
sent_titles = set()

# Boucle principale
while True:
    rss_root = get_latest_news()
    if rss_root:
        alerts = extract_alerts(rss_root)
        for title, link in alerts:
            if title not in sent_titles:
                send_alert(title, link)
                sent_titles.add(title)
    time.sleep(360)  # Vérifie toutes les 6 minutes (ajuste si besoin)
