from pyrogram import Client, filters
from pyrogram.types import (ReplyKeyboardMarkup, InlineKeyboardMarkup,
                            InlineKeyboardButton)
import os
import re
import csv
import scraper as s
import sqlite3

links = s.get_latest_links()

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
    await bot.send_message(message.chat.id, f"Hi, {message.chat.first_name} \nI'm a Result Bot from ABVV\nI'm here to help you to find your result quickly")

    await bot.send_message(
            message.chat.id,
            "Get Your Result Now",
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
    await bot.send_message(message.chat.id, 'Enter keyword to search as\n@search [keyword]\ne.g. @search master of computer application')

@app.on_message(filters.text & filters.private)
async def result(client, message):
    # await client.send_message(message.chat.id, 'Processing...')

    text = message.text.lower()

    # Check if the input is for the search function
    if text.startswith("@search"):
        keyword = text[len("@search"):].strip()
        
        all_links = s.get_all_links_in_var()

        keyword_links = s.search_names_by_keyword(keyword,all_links)
        
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
    
    # Check if the input is for the call function
    elif text.startswith("@roll"):
        roll = text[len("@roll"):].strip()
        if re.compile(r'\d{4,}').search(str(roll)):
            chat_id = message.chat.id
            user_id = message.from_user.id

            eid = get_callback_data(user_id)

            if eid:
                res = s.get_your_result(eid,roll)
                await client.send_message(chat_id, res)
                # clear_callback_data(user_id)
            else :
                await client.send_message(chat_id, 'Run the command \n/latest_result or \n/search_by_keyword \nThen select the course from given links...')
    
    elif text.startswith("@name"):
        name = text[len("@name"):].strip()
        chat_id = message.chat.id
        user_id = message.from_user.id
        eid = get_callback_data(user_id)
        roll = s.get_result_by_name(name,eid)
        if roll:
            res = s.get_your_result(eid,roll)
            await client.send_message(chat_id, res)
        else:
            await client.send_message(chat_id, 'Result not found!')


@app.on_message(filters.private & filters.document)
def handle_document(bot, message):
    message.reply_text("Please wait while your request is processing...")
    chat_id = message.chat.id
    eid = get_callback_data(chat_id)

    # Check if the document is a CSV file
    if message.document.file_name.endswith(".csv"):
        # Download the CSV file
        file_id = message.document.file_id
        file_path = bot.download_media(file_id)
        
        # Rename the file to have a .csv extension
        csv_file_path = os.path.splitext(file_path)[0] + ".csv"
        os.rename(file_path, csv_file_path)
        
        # Read the CSV file using csv library and store data in lists
        try:
            with open(csv_file_path, 'r') as csv_file:
                csv_reader = csv.reader(csv_file)
                header = next(csv_reader)  # assuming the first row is the header
                
                name_list = None
                roll_list = None
                name_column_index = None
                roll_column_index = None
                
                for i, col_name in enumerate(header):
                    if col_name.lower() == 'name' or col_name.lower() == 'student name':
                        name_list = []
                        name_column_index = i

                for i, col_name in enumerate(header):
                    if col_name.lower() == 'roll no' or col_name.lower() == 'roll number':
                        roll_list = []
                        roll_column_index = i
                
                if name_list is None and roll_list is None:
                    # No supported headers found
                    message.reply_text("No supported headers found. Aborting processing.")
                    return
                
                for row in csv_reader:
                    for i, value in enumerate(row):
                        if name_list is not None:
                            if i is name_column_index:
                                name_list.append(value)
                    for i, value in enumerate(row):
                        if roll_list is not None:
                            if i is roll_column_index:
                                roll_list.append(value)
            
            # Process the lists as needed
            if roll_list is not None:
                file = s.get_results_by_rolls(eid,roll_list)
            
            absolute_path = os.path.abspath(file)

            # You can also send a reply to the user
            bot.send_document(chat_id, document=absolute_path, caption="Students result in CSV file")
            
        except Exception as e:
            print(f"Error processing CSV file: {e}")
            message.reply_text("Error processing CSV file. Please try again.")
        finally:
            # Delete the CSV file after processing
            os.remove(csv_file_path)
            os.remove(absolute_path)
    else:
        message.reply_text("Please upload a valid CSV file.")

@app.on_callback_query()
async def answer(client, callback_query):
    chat_id = callback_query.message.chat.id
    user_id = callback_query.from_user.id
    data = callback_query.data

    store_callback_data(user_id, data)

    all_links = s.get_all_links_in_var()

    for i in all_links:
        if i['eid'] == data:
            eid_data = i['date'] + " " + i['course']
              
    await callback_query.edit_message_text("You have selected:\n"+ eid_data)
    await client.send_message(chat_id,"Please enter your roll number or name as\n@roll [rollnumber] or\n@name [name]\n e.g. @roll 12345\nand @name Gopal")

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
