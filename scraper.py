from bs4 import BeautifulSoup
import requests
import re
from fuzzywuzzy import fuzz
import sqlite3
from datetime import datetime
import csv

def get_latest_links():
    site_url = 'https://resulthour.com/cg/bilaspur-university/'
    response_site = requests.get(site_url)

    course_data = []

    if response_site.status_code == 200 :
        soup = BeautifulSoup(response_site.content, 'html.parser')
        url_lst = soup.find_all('div', class_='list-group')

        lst = url_lst[0]

        for item in lst.find_all('a', class_='list-group-item'):
            link = "https://resulthour.com/" + item['href']
            eid = re.search(r'/(\d+)\.html', link).group(1)
            course = item.text.strip().split('\n')[1].strip()
            date = item.find('b', class_='date').text.strip()
            course_data.append({'link': link, 'course': course, 'eid': eid, 'date': date})

    return course_data

def get_your_result(course_eid, roll_number):

    url = f'https://resulthour.com/Home/getResult/0?uid=1&eid={course_eid}&rollno={roll_number}'
    
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        tables = soup.find_all('table')

        if len(tables) > 0:

            personal_details = []

            for row in tables[1].find_all('tr'):
                cols = row.find_all('td')
                if len(cols) == 0:
                    cols = row.find_all('th')
                cols = [ele.text.strip() for ele in cols]
                personal_details.append([ele for ele in cols if ele])

            keys_to_extract = ['Name', 'Roll No']
            name_and_roll = {}

            for item in personal_details:
                if item[0] in keys_to_extract:
                    if item[0] == 'Roll No':
                        name_and_roll[item[0]] = int(re.search(r'\d+', item[1]).group())
                    else:
                        name_and_roll[item[0]] = item[1]

            final_result = []

            for row in tables[4].find_all('tr'):
                cols = row.find_all('td')
                if len(cols) == 0:
                    cols = row.find_all('th')
                cols = [ele.text.strip() for ele in cols]
                final_result.append([ele for ele in cols if ele])

            extracted_score = final_result[1][1]
            extracted_numbers = re.findall(r'\d+', extracted_score)
            formated_numbers = [int(num) for num in extracted_numbers]
            percentage = (formated_numbers[0] / formated_numbers[1]) * 100
            formatted_percentage = "{:.2f}".format(percentage)

            Name = name_and_roll['Name']
            roll = name_and_roll['Roll No']
            score = str(formated_numbers[0])+"/"+str(formated_numbers[1])
            result = final_result[2][1]

            output_string = '''Name : {name}\nRoll No : {roll}\nScore : {score}\nPercent : {percent} %\nResult : {result}'''.format(
                name = Name,
                roll = roll,
                score = score,
                percent = formatted_percentage,
                result = result
            )

        else:
            output_string = 'Result not found!'

    return output_string

def search_names_by_keyword(keyword, data_list):
    keyword = keyword.lower()

    threshold = 70

    matching_course = []

    for item in data_list:
        course_name = item.get('course', '').lower()
        if fuzz.token_set_ratio(keyword, course_name) >= threshold:
            # matching_course.append(item.get('course', ''))
            matching_course.append(item)

    if matching_course:
        return matching_course
    else:
        return "No result found..."
    
def get_result_by_name(name,eid):
    name = name.replace(" ", "+")
    b_link_ = f"https://resulthour.com/Home/byname?exam={eid}&uid=1&name="+name
    
    response = requests.get(b_link_)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        tables = soup.find_all('table')

        if len(tables) > 0:

            data = []

            for row in tables[0].find_all('tr'):
                cols = row.find_all('td')
                if len(cols) == 0:
                    cols = row.find_all('th')
                cols = [ele.text.strip() for ele in cols]
                data.append([ele for ele in cols if ele])
        
            roll = data[1][2]
            return roll
        else :
            return "Result not found!"

def insert_new_records(data_to_insert):
    conn = sqlite3.connect('all_results_links.db')
    cursor = conn.cursor()

    for row in data_to_insert:
        cursor.execute('''
            INSERT INTO results (link, course, eid, date)
            VALUES (?, ?, ?, ?)
        ''', (row['link'], row['course'], row['eid'], row['date']))

    conn.commit()
    conn.close()

def fetch_old_record():
    conn = sqlite3.connect('all_results_links.db')
    cursor = conn.cursor()

    cursor.execute('SELECT course FROM results ORDER BY id DESC LIMIT 1')
    result = cursor.fetchone()

    if result:
        last_record = result[0]
    else:
        last_record = 'No records in the database.'
    
    conn.close()
    return last_record

def latest_links():
    latest_link = []

    site_url = 'https://resulthour.com/cg/bilaspur-university/'

    response = requests.get(site_url)

    if response.status_code == 200 :
        soup = BeautifulSoup(response.content, 'html.parser')

        url_lst = soup.find_all('div', class_='list-group')

        lst = url_lst[0]

        for item in lst.find_all('a', class_='list-group-item'):
            link = item['href']
            eid = re.search(r'/(\d+)\.html', link).group(1)
            course = item.text.strip().split('\n')[1].strip()
            date = item.find('b', class_='date').text.strip()
            latest_link.append({'link': link, 'course': course, 'eid': eid, 'date': date})
    
    return latest_link
            
def update_result_links():
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # print(f"Current time: {current_time}")

    latest_link = latest_links()
    top_link = latest_link[0]['course']
    
    last_record = fetch_old_record()

    new_links = []

    if top_link != last_record:
        for link in latest_link:
            if link['course'] == last_record:
                break
            else:
                new_links.append(link)

        new_links.reverse()
        insert_new_records(new_links)
        return current_time,'New records inserted successfully...'

    else:
        return current_time,"You have nothing..."

def get_all_links_in_var():
    conn = sqlite3.connect('all_results_links.db')

    cursor = conn.cursor()

    cursor.execute('SELECT * FROM results ORDER BY id DESC')
    fetched_records = cursor.fetchall()

    conn.close()

    if fetched_records:
        
        data_from_database = [{'link': row[1], 'course': row[2], 'eid': row[3], 'date': row[4]} for row in fetched_records]

    else:
        data_from_database = 'No records in the database.'

    return data_from_database

def get_all_rolls_by_names(names,eid):
    rolls = []
    for name in names:
        name = name.replace(" ", "+")
        b_link_ = f"https://resulthour.com/Home/byname?exam={eid}&uid=1&name="+name
        
        response = requests.get(b_link_)

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')

            tables = soup.find_all('table')

            if len(tables) > 0:

                data = []

                for row in tables[0].find_all('tr'):
                    cols = row.find_all('td')
                    if len(cols) == 0:
                        cols = row.find_all('th')
                    cols = [ele.text.strip() for ele in cols]
                    data.append([ele for ele in cols if ele])
            
                roll = data[1][2]
                rolls.append(roll)
            else :
                rolls.append('')
    return rolls

def get_results_by_rolls(eid,rolls):
    base_url = f'https://resulthour.com/Home/getResult/0?uid=1&eid={eid}&rollno='

    output_results = []

    for roll in rolls:
        url = base_url + str(roll)

        response = requests.get(url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')

            tables = soup.find_all('table')

            # Check if tables exist
            if len(tables) > 0:

                personal_details = []

                for row in tables[1].find_all('tr'):
                    cols = row.find_all('td')
                    if len(cols) == 0:
                        cols = row.find_all('th')
                    cols = [ele.text.strip() for ele in cols]
                    personal_details.append([ele for ele in cols if ele])

                keys_to_extract = ['Name', 'Roll No']
                name_and_roll = {}

                for item in personal_details:
                    if item[0] in keys_to_extract:
                        if item[0] == 'Roll No':
                            name_and_roll[item[0]] = int(re.search(r'\d+', item[1]).group())
                        else:
                            name_and_roll[item[0]] = item[1]

                final_result = []

                for row in tables[4].find_all('tr'):
                    cols = row.find_all('td')
                    if len(cols) == 0:
                        cols = row.find_all('th')
                    cols = [ele.text.strip() for ele in cols]
                    final_result.append([ele for ele in cols if ele])

                extracted_score = final_result[1][1]
                extracted_numbers = re.findall(r'\d+', extracted_score)
                formated_numbers = [int(num) for num in extracted_numbers]
                percentage = (formated_numbers[0] / formated_numbers[1]) * 100
                formatted_percentage = "{:.2f}".format(percentage)

                Name = name_and_roll['Name']
                roll = name_and_roll['Roll No']
                score = str(formated_numbers[0])+"/"+str(formated_numbers[1])
                result = final_result[2][1]

                output_results.append((formatted_percentage, roll, Name, score, result))

            else:
                pass
    
    output_results.sort(reverse=True)
    
    headers = ['Roll Number', 'Student Name', 'Score', 'Percentage', 'Result']

    # Extracting and rearranging the data
    arranged_data = [(row[1], row[2], row[3], row[0], row[4]) for row in output_results]

    current_time = datetime.now()
    formatted_time = current_time.strftime("%Y%m%d%H%M%S")
    unique_name = f"_{formatted_time}"
    file_name = str(eid) + str(unique_name) + '.csv' 

    # Writing to CSV file
    with open(file_name, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)

        # Writing headers
        csvwriter.writerow(headers)

        # Writing data
        csvwriter.writerows(arranged_data)

    return file_name

