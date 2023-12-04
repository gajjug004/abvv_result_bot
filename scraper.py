from bs4 import BeautifulSoup
import requests
import re
from fuzzywuzzy import fuzz
from datetime import datetime

page_s = 2
page_e = 15
results = []


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


def for_first_page():

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
            results.append({'link': link, 'course': course, 'eid': eid, 'date': date})
    
    return results

def for_all_pages():
    for page in range(page_s,page_e+1):

        url = f'https://resulthour.com/cg/bilaspur-university/?page={page}'

        response = requests.get(url)

        if response.status_code == 200 :
            soup = BeautifulSoup(response.content, 'html.parser')
            
            url_lst = soup.find_all('div', class_='list-group')

            lst = url_lst[0]

            for item in lst.find_all('a', class_='list-group-item'):
                link = item['href']
                eid = re.search(r'/(\d+)\.html', link).group(1)
                course = item.text.strip().split('\n')[1].strip()
                date = item.find('b', class_='date').text.strip()
                results.append({'link': link, 'course': course, 'eid': eid, 'date': date})
    
    return results

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
        return False
    
def extract_data_between_dates(data, start_date_str, end_date_str):
    start_date = datetime.strptime(start_date_str, '%d-%b-%y')
    end_date = datetime.strptime(end_date_str, '%d-%b-%y')

    result = []
    for entry in data:
        entry_date = datetime.strptime(entry['date'], '%d-%b-%y')
        if start_date <= entry_date <= end_date:
            result.append(entry)

    return result

# # Example: Extract data between '01-Jan-23' and '31-Dec-23'
# start_date_str = '18-Oct-23'
# end_date_str = '28-Oct-23'
# result_data = extract_data_between_dates(results, start_date_str, end_date_str)

# # Print the result
# for entry in result_data:
#     print(entry)

def get_result_by_name(name,eid):
    name = name.replace(" ", "+")
    b_link_ = f"https://resulthour.com/Home/byname?exam={eid}&uid=1&name="+name
    
    response = requests.get(b_link_)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        tables = soup.find_all('table')

        data = []

        for row in tables[0].find_all('tr'):
            cols = row.find_all('td')
            if len(cols) == 0:
                cols = row.find_all('th')
            cols = [ele.text.strip() for ele in cols]
            data.append([ele for ele in cols if ele])
    
    roll = data[1][2]