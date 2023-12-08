from pyrogram import Client, filters
from pyrogram.types import (ReplyKeyboardMarkup, InlineKeyboardMarkup,
                            InlineKeyboardButton)
import os
import re
import scraper as s
import sqlite3

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

@app.on_message(filters.command("members") & filters.user(1117004028))
async def count_mem(client, message):
    c = count_records()
    message_to_send = f"We have {c} members..."
    await client.send_message(chat_id=1117004028, text=message_to_send)

@app.on_message(filters.command("search_by_keyword") & filters.private)
async def start(bot, message):   
    await bot.send_message(message.chat.id, 'Enter keyword to search:')

@app.on_message(filters.regex(r"\d{6,}") & filters.private)
async def result(client, message):
    # await client.send_message(message.chat.id, 'Processing...')
    chat_id = message.chat.id
    user_id = message.from_user.id

    eid = get_callback_data(user_id)

    if eid:
        roll_number = message.text

        res = s.get_your_result(eid,roll_number)
        await client.send_message(chat_id, res)

        # clear_callback_data(user_id)
    else :
        await client.send_message(chat_id, 'Run the command \n/latest_result or \n/search_by_keyword \nThen select the course from given links...')

@app.on_message(filters.text & filters.private)
async def result(client, message):
    # await client.send_message(message.chat.id, 'Processing...')
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
    chat_id = callback_query.message.chat.id
    user_id = callback_query.from_user.id
    data = callback_query.data

    store_callback_data(user_id, data)
    # print(callback_query)
    # global eid
    # eid = callback_query.data
    for i in links:
        if i['eid'] == data:
            eid_data = i['date'] + " " + i['course']
    await callback_query.edit_message_text(eid_data)
    await client.send_message(chat_id,"Please enter your roll number:")


# Function to store callback data in the database
def store_callback_data(user_id, data):
    conn = sqlite3.connect('user_data.db')
    cursor = conn.cursor()
    existing_data = get_callback_data(user_id)

    if existing_data:
        # Update the existing callback data
        cursor.execute("UPDATE user_data SET callback_data=? WHERE user_id=?", (data, user_id))
    else:
        # Store the new callback data
        cursor.execute("INSERT INTO user_data (user_id, callback_data) VALUES (?, ?)", (user_id, data))

    conn.commit()
    conn.close()

# Function to retrieve callback data from the database
def get_callback_data(user_id):
    conn = sqlite3.connect('user_data.db')
    cursor = conn.cursor()
    cursor.execute("SELECT callback_data FROM user_data WHERE user_id=?", (user_id,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None

# Function to clear callback data from the database
def clear_callback_data(user_id):
    conn = sqlite3.connect('user_data.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM user_data WHERE user_id=?", (user_id,))
    conn.commit()
    conn.close()

def count_records():
    conn = sqlite3.connect('user_data.db')
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM user_data")
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else 0

if __name__ == "__main__":
    conn = sqlite3.connect('user_data.db')
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS user_data (user_id INTEGER, callback_data TEXT)")
    conn.commit()
    conn.close()
    print("I'm alive...")
    app.run()



