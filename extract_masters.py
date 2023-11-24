import requests
from bs4 import BeautifulSoup

def extract_msc_page(msc_page_url):
    contents = {'url': msc_page_url}
    try:
        page_url = requests.get(msc_page_url)
        page_soup = BeautifulSoup(page_url.text, 'html.parser')
        #Course Name
        name_links = page_soup.find_all('h1', {'class':'course-header__course-title'})
        if name_links:
            contents['courseName'] = name_links[0].text.strip()
        else:
            contents['courseName'] = ''       
        # University name
        uni_links = page_soup.find_all('a', {'class': 'course-header__institution'})
        if uni_links:
            contents['universityName'] = uni_links[0].get_text(strip=True)
        else:
            contents['universityName'] = ''

        # Faculty Name
        faculty_links = page_soup.find_all('a', {'class': 'course-header__department'})
        if faculty_links:
            contents['facultyName'] = faculty_links[0].get_text(strip=True)
        else:
            contents['facultyName'] = ''

        # Full time or not
        FullTime_links = page_soup.find_all('a', {'class':'concealLink' })
        FullTime = any(item['href'] == "/masters-degrees/full-time/" for item in FullTime_links)
        contents['fullTime'] = FullTime

        # Description
        description_element = page_soup.find("div", id='Snippet')
        if description_element:
            contents['description'] = description_element.get_text(strip=True)
        else:
            contents['description'] = ''

        # Start Date
        start_links = page_soup.find('span', {'class': 'key-info__start-date'})
        if start_links:
            contents['startDate'] = start_links.get_text(strip=True)
        else:
            contents['startDate'] = ''

        # Fees
        fees_element = page_soup.find('div', {'class': "course-sections__fees"})
        if fees_element:
            fees_links = fees_element.get_text(strip=True)
            contents['fees'] = fees_links
        else:
            contents['fees'] = ''

        # Modality
        modality_element = page_soup.find('span', {'class': "key-info__qualification"})
        if modality_element:
            modality_links = modality_element.get_text(strip=True)
            contents['modality'] = modality_links
        else:
            contents['modality'] = ''

        # Duration
        duration_links = page_soup.find('span', {'class': "key-info__duration"})
        if duration_links:
            contents['duration'] = duration_links.get_text(strip=True)
        else:
            contents['duration'] = ''

        # City
        city_links = page_soup.find_all('a', {'class':'course-data__city'})
        if city_links:
            contents['city'] = city_links[0].get_text(strip=True)
        else:
            contents['city'] = ''

        # Country
        country_links = page_soup.find_all('a', {'class': 'course-data__country'})
        if country_links:
            contents['country'] = country_links[0].get_text(strip=True)
        else:
            contents['country'] = ''

        # Administrator
        admin_links = page_soup.find_all('a', {'class': 'course-data__on-campus'})
        if admin_links:
            contents['administator'] = admin_links[0].get_text(strip=True)
        else:
            contents['administator'] = ''

    except Exception as e:
        print(f"Error processing {msc_page_url}: {e}")

    return contents