import telebot
from bs4 import BeautifulSoup
from telebot import types
import requests
import re

Token = '6900705999:AAG5QVR8-ACSc8k6RmZ8qQ9oZaFQOPoRfYk'

bot = telebot.TeleBot(Token)


site_url = 'https://resulthour.com/cg/bilaspur-university/'

response_site = requests.get(site_url)

if response_site.status_code == 200 :
    soup = BeautifulSoup(response_site.content, 'html.parser')
    course_data = []
    url_lst = soup.find_all('div', class_='list-group')

    lst = url_lst[0]

    for item in lst.find_all('a', class_='list-group-item'):
        link = item['href']
        eid = re.search(r'/(\d+)\.html', link).group(1)
        course = item.text.strip().split('\n')[1].strip()
        date = item.find('b', class_='date').text.strip()
        course_data.append({'link': link, 'course': course, 'eid': eid, 'date': date})



# Define a dictionary containing course data
# course_data = [{'link': '/cg/bilaspur-university/reval-result-ba-partii-two/113700.html', 'course': 'Reval Result B.A. PART-II (TWO)', 'eid': '113700', 'date': '08-Nov-23'}, {'link': '/cg/bilaspur-university/reval-result-ma-previous-history/113699.html', 'course': 'Reval Result M.A. (Previous)  History', 'eid': '113699', 'date': '07-Nov-23'}, {'link': '/cg/bilaspur-university/reval-result-b-sc-parti-biogroup/113698.html', 'course': 'Reval Result B. SC. PART-I (BIO-GROUP)', 'eid': '113698', 'date': '07-Nov-23'}, {'link': '/cg/bilaspur-university/reval-result-b-sc-parti-maths-group/113697.html', 'course': 'Reval Result B. SC. PART-I (MATHS GROUP)', 'eid': '113697', 'date': '07-Nov-23'}, {'link': '/cg/bilaspur-university/reval-result-ma-previous-english/113696.html', 'course': 'Reval Result M.A. (Previous) English', 'eid': '113696', 'date': '07-Nov-23'}, {'link': '/cg/bilaspur-university/reval-result-ba-parti-one-private/113695.html', 'course': 'Reval Result B.A. PART-I (ONE) (PRIVATE)', 'eid': '113695', 'date': '07-Nov-23'}, {'link': '/cg/bilaspur-university/reval-result-bcom-partii-two-1023/113694.html', 'course': 'Reval Result B.COM PART-II (TWO) (10+2+3)', 'eid': '113694', 'date': '07-Nov-23'}, {'link': '/cg/bilaspur-university/reval-result-bcom-parti-one-1023/113693.html', 'course': 'Reval Result B.COM PART-I (ONE) (10+2+3)', 'eid': '113693', 'date': '07-Nov-23'}, {'link': '/cg/bilaspur-university/reval-result-b-sc-partii-two/113691.html', 'course': 'Reval Result B. SC. PART-II (TWO)', 'eid': '113691', 'date': '07-Nov-23'}, {'link': '/cg/bilaspur-university/reval-result-b-sc-partiii-three/113692.html', 'course': 'Reval Result B. SC. PART-III (THREE)', 'eid': '113692', 'date': '07-Nov-23'}, {'link': '/cg/bilaspur-university/reval-result-ba-parti-one-regular/113690.html', 'course': 'Reval Result B.A. PART-I (ONE) (REGULAR)', 'eid': '113690', 'date': '07-Nov-23'}, {'link': '/cg/bilaspur-university/reval-result-bca-partii-two/113677.html', 'course': 'Reval Result B.C.A. PART-II (TWO)', 'eid': '113677', 'date': '03-Nov-23'}, {'link': '/cg/bilaspur-university/retotaling-result-ba-partii-two/113671.html', 'course': 'Retotaling Result  B.A. PART-II (TWO)', 'eid': '113671', 'date': '01-Nov-23'}, {'link': '/cg/bilaspur-university/retotaling-result-ba-partiii-three/113670.html', 'course': 'Retotaling Result B.A. PART-III (THREE)', 'eid': '113670', 'date': '01-Nov-23'}, {'link': '/cg/bilaspur-university/retotaling-result-b-sc-partii-two/113669.html', 'course': 'Retotaling Result B. SC. PART-II (TWO)', 'eid': '113669', 'date': '01-Nov-23'}, {'link': '/cg/bilaspur-university/retotaling-result-b-sc-partiii-three/113668.html', 'course': 'Retotaling Result B. SC. PART-III (THREE)', 'eid': '113668', 'date': '01-Nov-23'}, {'link': '/cg/bilaspur-university/retotaling-result-bcom-parti-one-1023/113667.html', 'course': 'Retotaling Result B.COM PART-I (ONE) (10+2+3)', 'eid': '113667', 'date': '01-Nov-23'}, {'link': '/cg/bilaspur-university/retotaling-result-b-sc-parti-maths-group/113665.html', 'course': 'Retotaling Result B. SC. PART-I (MATHS GROUP)', 'eid': '113665', 'date': '01-Nov-23'}, {'link': '/cg/bilaspur-university/retotaling-result-bca-partii-two/113666.html', 'course': 'Retotaling Result B.C.A. PART-II (TWO)', 'eid': '113666', 'date': '01-Nov-23'}, {'link': '/cg/bilaspur-university/retotaling-result-b-sc-parti-biogroup/113664.html', 'course': 'Retotaling Result B. SC. PART-I (BIO-GROUP)', 'eid': '113664', 'date': '01-Nov-23'}, {'link': '/cg/bilaspur-university/master-of-computer-application-third-semester/113661.html', 'course': 'MASTER OF COMPUTER APPLICATION (THIRD SEMESTER)', 'eid': '113661', 'date': '28-Oct-23'}, {'link': '/cg/bilaspur-university/reval-result-bca-parti-one/113657.html', 'course': 'REVAL RESULT B.C.A. PART-I (ONE)', 'eid': '113657', 'date': '26-Oct-23'}, {'link': '/cg/bilaspur-university/master-of-computer-application-second-semester/113648.html', 'course': 'MASTER OF COMPUTER APPLICATION (SECOND SEMESTER)', 'eid': '113648', 'date': '18-Oct-23'}, {'link': '/cg/bilaspur-university/reval-result-b-sc-partiii/113655.html', 'course': 'Reval Result B. SC. PART-III', 'eid': '113655', 'date': '12-Oct-23'}, {'link': '/cg/bilaspur-university/reval-result-ba-partiii-three/113608.html', 'course': 'REVAL RESULT B.A. PART-III (THREE)', 'eid': '113608', 'date': '12-Oct-23'}, {'link': '/cg/bilaspur-university/reval-result-bcom-part-3bba-parti-onebba-partii-twobca-partiii-threepg-diploma-in-business-managemen/113656.html', 'course': 'Reval Result BCom Part 3,B.B.A.  PART-I (ONE),B.B.A.  PART-II (TWO),B.C.A. PART-III (THREE),P.G. DIPLOMA IN BUSINESS MANAGEMENT', 'eid': '113656', 'date': '10-Oct-23'}, {'link': '/cg/bilaspur-university/msc-ii-sem-computer-science/113591.html', 'course': 'M.SC. II SEM. COMPUTER SCIENCE', 'eid': '113591', 'date': '10-Oct-23'}, {'link': '/cg/bilaspur-university/ufm-result-main-exam-even-sem-notification-no1999-date-09102023/113585.html', 'course': 'UFM RESULT MAIN EXAM & EVEN SEM  NOTIFICATION NO.1999 Date 09.10.2023', 'eid': '113585', 'date': '09-Oct-23'}, {'link': '/cg/bilaspur-university/ba-llb-iv-sem/113559.html', 'course': 'B.A. L.L.B. (IV SEM.)', 'eid': '113559', 'date': '30-Sep-23'}, {'link': '/cg/bilaspur-university/ba-llb-vi-sem/113558.html', 'course': 'B.A. L.L.B. (VI SEM.)', 'eid': '113558', 'date': '30-Sep-23'}, {'link': '/cg/bilaspur-university/bcom-llb-sixth-semester-new-course/113566.html', 'course': 'B.COM. LL.B. SIXTH SEMESTER (NEW COURSE)', 'eid': '113566', 'date': '30-Sep-23'}, {'link': '/cg/bilaspur-university/bsc-vi-sem-computer-science-under-5yrs-int-course/113565.html', 'course': 'B.SC. VI SEM. COMPUTER SCIENCE (UNDER 5YRS INT. COURSE)', 'eid': '113565', 'date': '30-Sep-23'}, {'link': '/cg/bilaspur-university/bsc-v-sem-computer-science-under-5yrs-int-course/113564.html', 'course': 'B.SC. V SEM. COMPUTER SCIENCE (UNDER 5YRS INT. COURSE)', 'eid': '113564', 'date': '30-Sep-23'}, {'link': '/cg/bilaspur-university/bsc-honours-microbiology-semesteriv/113555.html', 'course': 'B.SC. HONOURS MICROBIOLOGY SEMESTER-IV', 'eid': '113555', 'date': '29-Sep-23'}, {'link': '/cg/bilaspur-university/msc-microbiology-bioinformatics-iii-sem-under-2yr-post-graduate-course/113553.html', 'course': 'M.SC. MICROBIOLOGY & BIOINFORMATICS III SEM (UNDER 2YR POST GRADUATE COURSE)', 'eid': '113553', 'date': '29-Sep-23'}, {'link': '/cg/bilaspur-university/bsc-hons-biotechnology-semester-ii/113554.html', 'course': 'B.Sc. (Hons.) Biotechnology Semester II', 'eid': '113554', 'date': '29-Sep-23'}, {'link': '/cg/bilaspur-university/bhm-under-4-year-degree-course-semester-iv/113551.html', 'course': 'B.H.M. (UNDER 4 YEAR DEGREE COURSE) -SEMESTER IV', 'eid': '113551', 'date': '29-Sep-23'}, {'link': '/cg/bilaspur-university/bcom-hons-semester-v/113552.html', 'course': 'B.COM (Hons) -Semester V', 'eid': '113552', 'date': '29-Sep-23'}, {'link': '/cg/bilaspur-university/bhm-under-4-year-degree-course-semester-viii/113549.html', 'course': 'B.H.M. (UNDER 4 YEAR DEGREE COURSE) -SEMESTER VIII', 'eid': '113549', 'date': '29-Sep-23'}, {'link': '/cg/bilaspur-university/bcom-hons-semester-ii/113550.html', 'course': 'B.COM (Hons) -Semester II', 'eid': '113550', 'date': '29-Sep-23'}, {'link': '/cg/bilaspur-university/mba-tourism-and-travel-management-mbattm-semester-iv/113548.html', 'course': 'MBA- TOURISM AND TRAVEL MANAGEMENT (MBA-TTM) -SEMESTER IV', 'eid': '113548', 'date': '29-Sep-23'}, {'link': '/cg/bilaspur-university/bachelors-of-hotel-management-and-catering-technology-under-4-year-degree-course-semester-ii/113547.html', 'course': "BACHELOR'S OF HOTEL MANAGEMENT AND  CATERING TECHNOLOGY (UNDER 4 YEAR DEGREE COURSE) -SEMESTER II", 'eid': '113547', 'date': '29-Sep-23'}, {'link': '/cg/bilaspur-university/bcom-llb-eight-semester-new-course/113532.html', 'course': 'B.COM. LL.B. EIGHT SEMESTER (NEW COURSE)', 'eid': '113532', 'date': '27-Sep-23'}, {'link': '/cg/bilaspur-university/llm-ii-sem/113533.html', 'course': 'LL.M. (II SEM.)', 'eid': '113533', 'date': '27-Sep-23'}, {'link': '/cg/bilaspur-university/bsc-hons-computer-science-semester-iv/113531.html', 'course': 'B.Sc. (Hons) Computer Science -Semester IV', 'eid': '113531', 'date': '27-Sep-23'}, {'link': '/cg/bilaspur-university/mba-tourism-and-travel-management-mbattm-semester-ii/113529.html', 'course': 'MBA- TOURISM AND TRAVEL MANAGEMENT (MBA-TTM) -SEMESTER II', 'eid': '113529', 'date': '27-Sep-23'}, {'link': '/cg/bilaspur-university/bhm-under-4-year-degree-course-semester-vi/113530.html', 'course': 'B.H.M. (UNDER 4 YEAR DEGREE COURSE) -SEMESTER VI', 'eid': '113530', 'date': '27-Sep-23'}, {'link': '/cg/bilaspur-university/master-of-business-administration-semester-ii/113528.html', 'course': 'MASTER OF BUSINESS ADMINISTRATION Semester II', 'eid': '113528', 'date': '27-Sep-23'}, {'link': '/cg/bilaspur-university/bcom-llb-fourth-semester-new-course/113527.html', 'course': 'B.COM. LL.B. FOURTH SEMESTER (NEW COURSE)', 'eid': '113527', 'date': '26-Sep-23'}, {'link': '/cg/bilaspur-university/bcom-llb-second-semester-new-course/113526.html', 'course': 'B.COM. LL.B. SECOND SEMESTER (NEW COURSE)', 'eid': '113526', 'date': '26-Sep-23'}]

user_data = {}  # Dictionary to store user data

def handle_callback_query(call):
    for course in course_data:
        if call.data == course["eid"]:
            user_data[call.message.chat.id] = {"course_eid": course["eid"]}
            bot.answer_callback_query(call.id, f"You clicked {course['course']}")
            bot.send_message(call.message.chat.id, "Please enter your roll number:")
            bot.register_next_step_handler(call.message, get_roll_number)

def get_roll_number(message):
    user_id = message.chat.id
    roll_number = message.text
    user_data[user_id]["roll_number"] = roll_number

    # Call your function here using user_data[user_id]["course_eid"] and roll_number
    course_eid = user_data[user_id]["course_eid"]
    res = get_your_result(course_eid, roll_number)
    bot.send_message(user_id, res)

def get_your_result(course_eid, roll_number):
    # print(course_eid, roll_number)

    url = f'https://resulthour.com/Home/getResult/0?uid=1&eid={course_eid}&rollno={roll_number}'
    
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        tables = soup.find_all('table')
        
        # Check if tables exist
        if len(tables) > 0:
    
            data = []

            for row in tables[1].find_all('tr'):
                cols = row.find_all('td')
                if len(cols) == 0:
                    cols = row.find_all('th')
                cols = [ele.text.strip() for ele in cols]
                data.append([ele for ele in cols if ele])

            keys_to_extract = ['Name', 'Roll No']
            extracted_info = {}

            for item in data:
                if item[0] in keys_to_extract:
                    if item[0] == 'Roll No':
                        extracted_info[item[0]] = int(re.search(r'\d+', item[1]).group())
                    else:
                        extracted_info[item[0]] = item[1]

            data2 = []

            for row in tables[4].find_all('tr'):
                cols = row.find_all('td')
                if len(cols) == 0:
                    cols = row.find_all('th')
                cols = [ele.text.strip() for ele in cols]
                data2.append([ele for ele in cols if ele])

            text = data2[1][1]
            numbers = re.findall(r'\d+', text)

            int_numbers = [int(num) for num in numbers]

            percentage = (int_numbers[0] / int_numbers[1]) * 100

            formatted_percentage = "{:.2f}".format(percentage)

            output_string = "Hey {Name}, You got {percentage} %".format(
                Name=extracted_info['Name'], 
                percentage=formatted_percentage
            )
            return output_string

        else:
            output_string = 'Result not found!'
            return output_string

    # print(output_string)

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    handle_callback_query(call)

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    for course in course_data:
        button_text = f"{course['date']} - {course['course']}"
        button = types.InlineKeyboardButton(button_text, callback_data=course["eid"])
        markup.add(button)
    bot.send_message(message.chat.id, "Choose your course:", reply_markup=markup)
    # bot.send_message(message.chat.id, "If your course in not here. Enter here...")

bot.polling(none_stop=True)