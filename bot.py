import json
from aiogram import Bot, Dispatcher, types
from config import BOT_TOKEN
from database import add_entry, update_entry_status

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)


def marks_keyboard(data: str):
    yes = f"{data}:1"
    no = f"{data}:0"
    print(yes)
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    button_like = types.InlineKeyboardButton(text='Нравится', callback_data=yes)
    button_dislike = types.InlineKeyboardButton(text='Не нравится', callback_data=no)
    keyboard.add(button_like, button_dislike)
    return keyboard


@dp.callback_query_handler()
async def button1_handler(callback_query: types.CallbackQuery):
    message_id = callback_query.message.message_id
    chat_id = callback_query.message.chat.id
    data = callback_query.data.split(":")
    post_id = int(data[0])
    mark = int(data[-1])
    update_entry_status(post_id, mark)
    await bot.delete_message(chat_id=chat_id, message_id=message_id)


post = {"files": []}

@dp.message_handler(content_types=[
    types.ContentType.PHOTO,
    types.ContentType.VIDEO,
    types.ContentType.DOCUMENT,
    types.ContentType.TEXT
])
async def forward_message(message: types.Message):
    try:
        global post
        if message.media_group_id:
            if post["files"]:
                if message.photo:
                    media_file_id = ["photo", message.photo[0].file_id]
                elif message.video:
                    media_file_id = ["video", message.video.file_id]
                elif message.document:
                    media_file_id = ["document", message.document.file_id]
                else:
                    media_file_id = ""
                if media_file_id:
                    post["files"].append(media_file_id)
                if len(post["files"]) == int(post["counter"]):
                    media_group = types.MediaGroup()
                    for i, file in enumerate(post["files"]):
                        if i == 0:
                            if file[0] == "photo":
                                media_group.attach_photo(file[-1], caption=post["message"])
                            elif file[0] == "video":
                                media_group.attach_video(file[-1], caption=post["message"])
                            elif file[0] == "document":
                                media_group.attach_document(file[-1], caption=post["message"])
                        else:
                            if file[0] == "photo":
                                media_group.attach_photo(file[-1])
                            elif file[0] == "video":
                                media_group.attach_video(file[-1])
                            elif file[0] == "document":
                                media_group.attach_document(file[-1])
                    #сохраняю текст в бд номне нужен id записи.
                    identificator = add_entry(user_id=735551549, text=post["message"])
                    await bot.send_media_group(chat_id=735551549, media=media_group)
                    await bot.send_message(chat_id=735551549, text="Понравился ли вам пост?",
                                           reply_markup=marks_keyboard(data = f"{identificator}:735551549"))
                    post = {"files": []}
            else:
                post["counter"] = message.caption[-1]
                post["message"] = message.caption[:-1]
                if message.photo:
                    media_file_id = ["photo", message.photo[0].file_id]
                elif message.video:
                    media_file_id = ["video", message.video.file_id]
                elif message.document:
                    media_file_id = ["document", message.document.file_id]
                else:
                    media_file_id = ""
                if media_file_id:
                    post["files"].append(media_file_id)


        else:

            media_group = types.MediaGroup()
            if message.caption:
                caption = message.caption[:-1]
            else:
                caption = None
            if message.photo:
                media_group.attach_photo(message.photo[0].file_id, caption=caption)
            elif message.video:
                media_group.attach_video(message.video.file_id, caption=caption)
            elif message.document:
                media_group.attach_document(message.document.file_id, caption=caption)
            if media_group.media:
                await bot.send_media_group(chat_id=735551549, media=media_group)
            else:
                await bot.send_message(chat_id=735551549, text=message.text)
    except Exception as e:
        print(f"Failed to send message to user {735551549}: {e}")


if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)
