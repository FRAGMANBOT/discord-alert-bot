import os
import discord
import requests
import time

TOKEN = os.getenv("DISCORD_TOKEN")
WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK")

intents = discord.Intents.default()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'Connecté comme {client.user}')
    while True:
        try:
            r = requests.get("https://www.aljazeera.com/news/", timeout=10)
            if "Iran" in r.text or "nuclear" in r.text or "attack" in r.text:
                requests.post(WEBHOOK_URL, json={"content": "🚨 Une alerte potentielle détectée sur Al Jazeera."})
            time.sleep(300)  # 5 minutes
        except Exception as e:
            print(f"Erreur : {e}")
            time.sleep(300)

client.run(TOKEN)
