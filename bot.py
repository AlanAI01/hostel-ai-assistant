import google.generativeai as genai
import os
import asyncio
import threading

from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message

from fastapi import FastAPI
import uvicorn

# TOKEN = os.getenv("BOT_TOKEN")
TOKEN = os.getenv("BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-2.5-flash")

bot = Bot(token=TOKEN)
dp = Dispatcher()

# ---------- Telegram ----------

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
        response = model.generate_content(
            f"""
Ты администратор хостела в Астане.
Отвечай вежливо и кратко.
Если не знаешь ответа, так и скажи.

Вопрос клиента:
{message.text}
"""
        )

        await message.answer(response.text)


async def main():
    await dp.start_polling(bot)










def run_bot():
    asyncio.run(main())


# ---------- FastAPI ----------

app = FastAPI()


@app.get("/")
def home():
    return {"status": "Bot is alive"}


# ---------- Start ----------

if __name__ == "__main__":
    threading.Thread(target=run_bot, daemon=True).start()

    port = int(os.environ.get("PORT", 10000))

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=port
    )