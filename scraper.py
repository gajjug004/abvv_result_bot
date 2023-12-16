from bs4 import BeautifulSoup
import requests
import re
from fuzzywuzzy import fuzz
from datetime import datetime
from static_data import results
import pandas as pd
import dataframe_image as dfi
page_s = 2
page_e = 15

def page_update():
    site_url = 'https://resulthour.com/cg/bilaspur-university/'
    response_site = requests.get(site_url)

    if response_site.status_code == 200 :
        soup = BeautifulSoup(response_site.content, 'html.parser')

        pagination = [page.text.strip() for page in soup.find_all(['a'], class_='page-link') if page.text.strip().isdigit()]
        pages = [int(page) for page in pagination]

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

            marks_details = []

            for row in tables[3].find_all('tr'):
                cols = row.find_all('td')
                if len(cols) == 0:
                    cols = row.find_all('th')
                cols = [ele.text.strip() for ele in cols]
                marks_details.append([ele for ele in cols if ele])
            
            subject_names = [re.sub(r'^\d+\s*', '', row[0].strip()) for row in marks_details[1:]]

            th_tot_index = marks_details[0].index('TH TOT')
            pr_tot_index = marks_details[0].index('PR TOT')
            se_tot_index = marks_details[0].index('SE TOT')
            sub_tot_index = marks_details[0].index('SUB TOT')

            subject_dict = {}

            # Assuming all rows should have the same length as the first row
            expected_row_length = len(marks_details[0])

            for row in marks_details[1:]:
                # Check if the row has the expected length
                if len(row) < expected_row_length:
                    # If not, fill in the missing elements with zeros
                    row += ['0'] * (expected_row_length - len(row))
                
                # Continue with your existing logic
                subject_name = re.sub(r'^\d+\s*', '', row[0].strip())
                subject_dict[subject_name] = {
                    'TH TOT': row[th_tot_index],
                    'PR TOT': row[pr_tot_index],
                    'SE TOT': row[se_tot_index],
                    'SUB TOT': row[sub_tot_index]
                }
            
            for subject, totals in subject_dict.items():
                for key, value in totals.items():
                    if value.isdigit():
                        subject_dict[subject][key] = int(value)
                    elif value.endswith(('C', 'D', 'E', 'F', 'G','*')):
                        subject_dict[subject][key] = int(value[:-1])
                    elif value == '...':
                        subject_dict[subject][key] = 0
                    elif value == 'ABS':
                        subject_dict[subject][key] = 0

            df1 = pd.DataFrame(subject_dict).T
            df1.replace('...', pd.NA, inplace=True)
            df1 = df1.apply(pd.to_numeric, errors='coerce')
            df1['MAIN TOT'] = df1['TH TOT'].add(df1['PR TOT'], fill_value=0)
            df1.drop(['TH TOT', 'PR TOT'], axis=1, inplace=True)
            df1 = df1[['MAIN TOT', 'SE TOT', 'SUB TOT']]
            df1 = df1.astype({'MAIN TOT': int, 'SE TOT': int, 'SUB TOT': int})
            file_name = str(course_eid)+str(roll)+'.png'
            df1.dfi.export(file_name)
            
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
        return "No result found..."
    
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
