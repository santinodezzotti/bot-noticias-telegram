import os
import feedparser
import requests
from datetime import datetime

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

def enviar_mensaje(texto):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "text": texto
    }
    r = requests.post(url, data=data)
    print("STATUS:", r.status_code)
    print("RESPUESTA:", r.text)


def obtener_noticias():
    feeds = {
        "Clarín - Política": "https://www.clarin.com/rss/politica/",
        "La Nación - Política": "https://www.lanacion.com.ar/arc/outboundfeeds/rss/category/politica/",
        "Infobae - Política": "https://www.infobae.com/feeds/rss/politica.xml",
        "La Política Online": "https://www.lapoliticaonline.com/feed/",
        "BBC - Mundo": "http://feeds.bbci.co.uk/mundo/rss.xml",
        "AP News": "https://apnews.com/rss",
        "Washington Post - Politics": "http://feeds.washingtonpost.com/rss/politics"
    }

    noticias_enviadas = set()

    for nombre, url in feeds.items():
        feed = feedparser.parse(url)

        if not feed.entries:
            continue

        mensaje = f"<b>{nombre}</b>\n\n"
        contador = 0

        for entry in feed.entries:
            if entry.link in noticias_enviadas:
                continue

            noticias_enviadas.add(entry.link)

            mensaje += f"• {entry.title}\n"
            mensaje += f"{entry.link}\n\n"

            contador += 1
            if contador == 5:
                break

        if contador > 0:
            enviar_mensaje(mensaje)

def main():
     obtener_noticias()
if __name__ == "__main__":
    main()
