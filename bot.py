from flask import Flask
import threading
import os
import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message
import os
TOKEN = "8859657712:AAHvfQWEv5V3ztH7ZFv9nL1bep-4KAJ9q7g"

bot = Bot(token=TOKEN)
dp = Dispatcher()


@dp.message(Command("start"))
async def start_command(message: Message):
    await message.answer("Привет! Я AI Assistant 🤖")


@dp.message(F.text)
async def answer_message(message: Message):
    text = message.text.lower()

    if "цена" in text or "стоимость" in text:
        await message.answer("Стоимость проживания 5000 тг в сутки")

    elif "адрес" in text:
        await message.answer("Наш адрес: Астана")

    elif "привет" in text:
        await message.answer("Здравствуйте! Чем могу помочь?")

    else:
        await message.answer("Извините, пока я не знаю ответа на этот вопрос.")


async def main():
    await dp.start_polling(bot)

app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is alive!"

def run_web():
    port = int(os.environ.get("PORT", 10000))
    app.run(
        host="0.0.0.0",
        port=port,
        debug=False,
        use_reloader=False
    )

if __name__ == "__main__":
    web_thread = threading.Thread(target=run_web, daemon=True)
    web_thread.start()

    asyncio.run(main())