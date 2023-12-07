from pyrogram import Client, filters
from pyrogram.types import (ReplyKeyboardMarkup, InlineKeyboardMarkup,
                            InlineKeyboardButton)
import os
import re
import scraper as s

links = s.get_latest_links()
eid = []


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
    await bot.send_message(message.chat.id, f'Hello, {message.chat.first_name} \nWelcome to this Channel')

    await bot.send_message(
            message.chat.id,
            "Get Your Result :",
            reply_markup=ReplyKeyboardMarkup(
                [
                    ["/latest_result"],
                    ["/search_by_keyword"]
                ],
                resize_keyboard=True  
            )
        )
@app.on_message(filters.command("latest_result") & filters.private)
async def start(bot, message):   
    await bot.send_message(
        message.chat.id,
        "Choose Your Exam :",
        reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton(link['date']+' '+link['course'],callback_data=link['eid'])] for link in links]
        )
    )

@app.on_message(filters.command("search_by_keyword") & filters.private)
async def start(bot, message):   
    await bot.send_message(message.chat.id, 'Enter keyword to search:')

@app.on_message(filters.regex(r"\d{6,}") & filters.private)
async def result(client, message):
    await client.send_message(message.chat.id, 'Processing...')
    text = message.text
    if re.search(r'\d{6,}', text):
        roll = message.text
        res = s.get_your_result(eid,roll)
        await client.send_message(message.chat.id, res)

@app.on_message(filters.text & filters.private)
async def result(client, message):
    await client.send_message(message.chat.id, 'Processing...')
    text = message.text
    # l1 = s.for_first_page()
    l2 = s.for_all_pages()
    results = links + s.results
    keyword_links = s.search_names_by_keyword(text,results)
    # print(len(keyword_links))
    if keyword_links != "No result found...":
        await client.send_message(
        message.chat.id,
        "Choose Your Exam :",
        reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton(link['date']+' '+link['course'],callback_data=link['eid'])] for link in keyword_links]
        )
    )
    else:
        await client.send_message(message.chat.id, 'No result found for the keyword')
        

@app.on_callback_query()
async def answer(client, callback_query):
    global eid
    eid = callback_query.data
    for i in links:
        if i['eid'] == eid:
            eid_data = i['date'] + " " + i['course']
    await callback_query.edit_message_text(eid_data)
    await client.send_message(callback_query.from_user.id,"Please enter your roll number:")


print("I'm alive...")

app.run()



