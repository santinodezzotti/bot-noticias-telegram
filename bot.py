import os
import feedparser
import requests

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")


def enviar_mensaje(texto):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    data = {
        "chat_id": CHAT_ID,
        "text": texto,
        "parse_mode": "HTML"
    }

    requests.post(url, data=data)


def obtener_noticias():
    feeds = {
        "Clarín - Política": "https://www.clarin.com/rss/politica/",
        "La Nación - Política": "https://www.lanacion.com.ar/arc/outboundfeeds/rss/category/politica/",
        "Infobae": "https://www.infobae.com/arc/outboundfeeds/rss/",
        "Reuters - Politics": "https://www.reutersagency.com/feed/?best-topics=politics&post_type=best",
        "BBC - Mundo": "http://feeds.bbci.co.uk/mundo/rss.xml",
        "Washington Post - Politics": "http://feeds.washingtonpost.com/rss/politics"
    }

    feedparser.USER_AGENT = "Mozilla/5.0"
    noticias_enviadas = set()

    for nombre, url in feeds.items():
        feed = feedparser.parse(url)

        if not feed.entries:
            continue

        mensaje = f"<b>{nombre}</b>\n\n"
        contador = 0

        for entry in feed.entries:
            link = entry.get("link", "")
            titulo = entry.get("title", "Sin título")

            if not link or link in noticias_enviadas:
                continue

            noticias_enviadas.add(link)

            mensaje += f"• {titulo}\n"
            mensaje += f"{link}\n\n"

            contador += 1
            if contador == 5:
                break

        if contador > 0:
            enviar_mensaje(mensaje)


def main():
    obtener_noticias()


if __name__ == "__main__":
    main()
