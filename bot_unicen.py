import requests
from bs4 import BeautifulSoup
from telegram import Bot
import os

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

bot = Bot(token=TELEGRAM_TOKEN)

def avisar_nuevos(_):
    mensaje = "🧪 Mensaje de prueba para verificar que el bot funciona."
    bot.send_message(chat_id=CHAT_ID, text=mensaje)

def main():
    print("Iniciando ejecución del bot...")
    print(f"TELEGRAM_TOKEN: {'OK' if TELEGRAM_TOKEN else 'NO definido'}")
    print(f"CHAT_ID: {'OK' if CHAT_ID else 'NO definido'}")

    avisar_nuevos(None)
    print("Bot finalizado correctamente.")

if __name__ == "__main__":
    main()
