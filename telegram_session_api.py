from telethon.sync import TelegramClient
from config import TELEGRAM_API_ID
from config import TELEGRAM_API_HASH


def get_last_post(channel_username: str) -> None:
    with TelegramClient('session_1', TELEGRAM_API_ID, TELEGRAM_API_HASH,
                        system_version="4.16.30-vxCUSTOM",
                        device_model="ubuntu-server",
                        app_version="5.15.9") as client:
        channel_entity = client.get_entity(channel_username)

        posts = client.get_messages(channel_entity)
        if posts[0].grouped_id:
            posts += [m for m in client.get_messages(channel_entity, max_id=posts[0].id, limit=9)
                        if m.grouped_id == posts[0].grouped_id]

        media = []
        for post in posts:
            if post.text:
                message_text = post.text

            if post.media:
                media.append(post.media)
        if media:
            if message_text:
                message_text += str(len(media))
            else:
                message_text = str(len(media))
            client.send_message("@rekevant_news_feed_bot", message_text, file=media)
        else:
            if message_text:
                client.send_message("@rekevant_news_feed_bot", message_text)


get_last_post("@my_devotions")

