from bs4 import BeautifulSoup,SoupStrainer 
import requests 


URL = "https://en.wikipedia.org/wiki/Agentic_AI"

HEADERS = ({'User-Agent': 
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 \
        (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
            'Accept-Language': 'en-US, en;q=0.5'}) 

webpage = requests.get(URL, headers= HEADERS) 
soup = BeautifulSoup(webpage.content, "lxml", 
                     parse_only = SoupStrainer(
                       'span', class_ = 'mw-headline'))

print(soup.prettify())

import requests
from bs4 import BeautifulSoup
import pandas
 

print("Start : Parse the Contents of the URL") 


url = 'https://en.wikipedia.org/wiki/Agentic_AI'
response = requests.get(url)
soup = BeautifulSoup(response.content, features="html.parser")
for tag in soup.find_all('h2'):
    print(tag.text.strip())

print("End : Parse the Contents of the URL") 


print("Start : Show contents of Headers ...") 

#https://www.espncricinfo.com/


url = 'https://www.espncricinfo.com/'
r = requests.get(url)
soup = BeautifulSoup(r.text, features="lxml")
body_find = soup.find('body')

print("H1:")
for heading in body_find.find_all('H1'):
    print(heading.text)



print("h2:")
for heading in body_find.find_all('h2'):
    print(heading.text)
 
print("\nh3:")    
for heading in body_find.find_all('h3'):
    print(heading.text)


print("End : Show contents of Headers ...") 




print("\n")

print("-"*100)

print("Start : Show contents of Headers ...") 

for headings in soup.find_all(['h2', 'h3']):
    if str(headings).startswith("<h2"):
        print(f"H2, {headings.text.strip()}")
    else:
        print(f"H3, {headings.text.strip()}")

print("Start : Show contents of Headers ...") 

print("\n")

print("-"*100)

url = 'https://www.espncricinfo.com/'
r = requests.get(url)
soup = BeautifulSoup(r.text, features="lxml")
body_find = soup.find('body')
  
print("h2:")
for heading in body_find.find_all('h2'):
    print(heading.text)
 
print("\nh3:")    
for heading in body_find.find_all('h3'):
    print(heading.text)

print("\n")

print("-"*100)



