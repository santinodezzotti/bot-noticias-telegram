import feedparser
import logging
import asyncio
import pytz
from datetime import datetime
from telegram import Bot
import os

print("ENV VARIABLES DISPONIBLES:")
print(os.environ)

TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

print("TOKEN leído:", TOKEN)
print("CHAT_ID leído:", CHAT_ID)


bot = Bot(token=TOKEN)

sent_links = set()

feeds = {
    "Clarín": "https://www.clarin.com/rss/politica/",
    "La Nación": "https://www.lanacion.com.ar/arc/outboundfeeds/rss/category/politica/",
    "Infobae": "https://www.infobae.com/feeds/rss/politica.xml",
    "La Política Online": "https://www.lapoliticaonline.com/rss.xml",
    "BBC": "http://feeds.bbci.co.uk/news/world/rss.xml",
    "AP News": "https://apnews.com/hub/politics?outputType=xml",
    "Washington Post": "http://feeds.washingtonpost.com/rss/politics"
}

arg_tz = pytz.timezone("America/Argentina/Buenos_Aires")

async def send_news():
    now = datetime.now(arg_tz)

    if now.hour < 6 or now.hour > 22:
        return

    if now.hour % 2 != 0:
        return

    message = "📰 Noticias actualizadas:\n\n"

    for source, url in feeds.items():
        feed = feedparser.parse(url)
        message += f"🔹 {source}\n"

        count = 0
        for entry in feed.entries[:5]:
            if entry.link not in sent_links:
                message += f"- {entry.title}\n{entry.link}\n\n"
                sent_links.add(entry.link)
                count += 1
            if count == 3:
                break

        message += "\n"

    await bot.send_message(chat_id=CHAT_ID, text=message[:4096])

async def main():
    while True:
        await send_news()
        await asyncio.sleep(3600)

if __name__ == "__main__":
    asyncio.run(main())
