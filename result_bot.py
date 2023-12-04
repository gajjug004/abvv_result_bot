from pyrogram import Client, filters
from pyrogram.types import (ReplyKeyboardMarkup, InlineKeyboardMarkup,
                            InlineKeyboardButton)
from dotenv import load_dotenv
import os
import re
import scraper as s

links = s.get_latest_links()
eid = []

load_dotenv()

api_id = os.getenv("api_id")
api_hash = os.getenv("api_hash")
bot_token = os.getenv("bot_token")

app = Client(
    "result_bot",
    api_id=api_id, api_hash=api_hash,
    bot_token=bot_token
)

@app.on_message(filters.command("start") & filters.private)
async def start(bot, message):
    await bot.send_message(message.chat.id, f'Hello, {message.chat.first_name} \nWelcome to this Channel..')
    
    await app.send_message(
        message.chat.id,
        "Choose Your Exam :",
        reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton(link['date']+' '+link['course'],callback_data=link['eid'])] for link in links]
        )
    )
@app.on_callback_query()
async def answer(client, callback_query):
    global eid
    eid = callback_query.data
    # print(callback_query)
    await client.send_message(callback_query.from_user.id,"Please enter your roll number:")

@app.on_message(filters.text & filters.private)
async def result(client, message):
    text = message.text
    if re.search(r'\d{7}', text):
        roll = message.text
        res = s.get_your_result(eid,roll)
        await client.send_message(message.chat.id, res)

print("I'm alive...")

app.run()

