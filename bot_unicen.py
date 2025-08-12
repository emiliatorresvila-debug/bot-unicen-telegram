import requests
from bs4 import BeautifulSoup
from telegram import Bot
import os

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
URL = "https://www.econ.unicen.edu.ar/alumnos/ale/ofertas-ale-y-optativas?title=&page=0"

bot = Bot(token=TELEGRAM_TOKEN)

def obtener_publicaciones():
    r = requests.get(URL, timeout=10)
    soup = BeautifulSoup(r.text, "html.parser")
    publicaciones = []
    for item in soup.select("div.views-row"):
        titulo_tag = item.select_one("div.views-field-title a")
        if titulo_tag:
            titulo = titulo_tag.text.strip()
            link = "https://www.econ.unicen.edu.ar" + titulo_tag["href"]
            publicaciones.append((titulo, link))
    return publicaciones

def avisar_nuevos(_):
    publicaciones = obtener_publicaciones()
    if publicaciones:
        titulo, link = publicaciones[0]
        mensaje = f"📢 Nueva publicación:\n[{titulo}]({link})"
        bot.send_message(chat_id=CHAT_ID, text=mensaje, parse_mode="Markdown")

def main():
    print("Iniciando ejecución del bot...")
    avisar_nuevos(None)
    print("Bot finalizado correctamente.")

if __name__ == "__main__":
    main()
