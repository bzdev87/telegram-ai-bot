import os
import openai
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from dotenv import load_dotenv

# Load API Key dari .env
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ADMIN_ID = int(os.getenv("ADMIN_ID", 0))  # ID admin (default 0 jika tidak diisi)

# Setup bot
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

# Setup OpenAI API
openai.api_key = OPENAI_API_KEY

# Tombol menu utama
main_menu = ReplyKeyboardMarkup(resize_keyboard=True)
main_menu.add(KeyboardButton("📝 Tanya AI"), KeyboardButton("📢 Laporkan Masalah"))

@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.reply("Halo! Saya bot AI. Kirim pesan, dan saya akan menjawab dengan kecerdasan buatan!", reply_markup=main_menu)

@dp.message_handler(lambda message: message.text == "📢 Laporkan Masalah")
async def report_issue(message: types.Message):
    if ADMIN_ID:
        await bot.send_message(ADMIN_ID, f"🔔 Laporan dari {message.from_user.username}: {message.text}")
        await message.reply("Laporan telah dikirim ke admin.")
    else:
        await message.reply("Admin belum dikonfigurasi.")

@dp.message_handler(lambda message: message.text == "📝 Tanya AI")
async def ask_ai(message: types.Message):
    await message.reply("Kirim pertanyaanmu, saya akan menjawab!")

@dp.message_handler()
async def chat_ai(message: types.Message):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": message.text}],
            max_tokens=100
        )
        await message.reply(response["choices"][0]["message"]["content"])
    except Exception as e:
        logging.error(f"Error: {e}")
        await message.reply("Terjadi kesalahan, coba lagi nanti.")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    executor.start_polling(dp, skip_updates=True)
