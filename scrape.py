#Create a webscraper that will pull Job Title, Hiring Company, Salary if listed, and Job Location
#Then store the data into a Google Spreadsheet

import requests
from bs4 import BeautifulSoup

def stripHTML(text):
    hasSmall = text.find('smaller">')
    if hasSmall == -1:
        posStart = text.find('>')
        posEnd  = text.find('</span>')
        firstHalf = text[posStart+1:posEnd]
        return firstHalf
    else:
        posStart = text.find('>')
        posEnd  = text.find('<span style')
        firstHalf = text[posStart+1:posEnd]

        smallEnd = text.find('</span></span>')
        secondHalf = text[hasSmall+9:smallEnd]
        text = firstHalf + secondHalf
        return text

def extract(page):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36'}
    url = f"https://www.indeed.com/jobs?q=python+developer&l=Philadelphia,+PA&start={page}"
    r = requests.get(url, headers)
    soup = BeautifulSoup(r.content, 'html.parser')
    return soup


def transform(soup):
    divs = soup.find_all('div', class_ = 'jobsearch-SerpJobCard')
    for item in divs:
        title = item.find('a', class_ = 'jobtitle turnstileLink').text.strip()
        company = item.find('span', class_ = 'company').text.strip()
        spanLocation = item.find('span', class_ = 'location')
        try:
            salary = item.find('span', class_ = 'salaryText').text
            try:
                divLocation = item.find('div', class_ = 'location').text
                if divLocation == None:
                    temp = [title, company, salary[2:], stripHTML(str(spanLocation))]
                    print(temp, '\n')
                else:
                    temp = [title, company, salary[2:], divLocation]
                    print(temp, '\n')
            except:
                temp = [title, company, salary[2:], stripHTML(str(spanLocation))]
                print(temp, '\n')
        except:
            try:
                divLocation = item.find('div', class_ = 'location').text
                if divLocation == None:
                    temp = [title, company, 'No Salary Listed', spanLocation]
                    print(temp, '\n')
                else:
                    temp = [title, company, 'No Salary Listed', divLocation]
                    print(temp, '\n')
            except:
                temp = [title, company, 'No Salary Listed', stripHTML(str(spanLocation))]
                print(temp, '\n')
    return

def convert():
    return

c = extract(0)
print(transform(c))
