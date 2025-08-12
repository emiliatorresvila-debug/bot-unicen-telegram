import requests
from bs4 import BeautifulSoup
from telegram import Bot
import time
import os
import json

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
URL = "https://www.econ.unicen.edu.ar/alumnos/ale/ofertas-ale-y-optativas?title=&page=0"
STATE_FILE = "vistos.json"

bot = Bot(token=TELEGRAM_TOKEN)

def cargar_vistos():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as f:
            return set(json.load(f))
    return set()

def guardar_vistos(vistos):
    with open(STATE_FILE, "w") as f:
        json.dump(list(vistos), f)

def obtener_publicaciones():
    r = requests.get(URL)
    soup = BeautifulSoup(r.text, "html.parser")
    publicaciones = []
    for item in soup.select("div.views-row"):
        titulo_tag = item.select_one("div.views-field-title a")
        if titulo_tag:
            titulo = titulo_tag.text.strip()
            link = "https://www.econ.unicen.edu.ar" + titulo_tag["href"]
            publicaciones.append((titulo, link))
    return publicaciones

def avisar_nuevos(vistos):
    publicaciones = obtener_publicaciones()
    nuevos = [p for p in publicaciones if p[0] not in vistos]
    
    for titulo, link in nuevos:
        mensaje = f"📢 Nueva publicación:\n[{titulo}]({link})"
        bot.send_message(chat_id=CHAT_ID, text=mensaje, parse_mode="Markdown")
    
    vistos.update([p[0] for p in nuevos])
    return vistos

def main():
    vistos = cargar_vistos()
    while True:
        vistos = avisar_nuevos(vistos)
        guardar_vistos(vistos)
        time.sleep(300)  # Espera 5 minutos

if __name__ == "__main__":
    main()
