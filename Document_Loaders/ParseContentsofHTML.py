## RB - 31.05.2025 , This program processes the contents of HTML e.g Cricbuzz.com
#  RB - this program make use of BeautifulSoup and checks the embedded URLS within the website.
#  RB - this makes use of BeautifulSoup 


from bs4 import BeautifulSoup,SoupStrainer 
import requests 
import requests
from bs4 import BeautifulSoup
import pandas
 
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin





## This function extracts the data inside the URL 
def scrape_site(start_url):
# start_url = "https://en.wikipedia.org/wiki/Agentic_AI"
    current_url = start_url

    while current_url:
        print(f"Processing: {current_url}")
        response = requests.get(current_url)
        soup = BeautifulSoup(response.content, 'html.parser')

#  Example: Get article titles
        articles = soup.find_all('h2') # Adjust the tag as needed
        # articles = soup.find_all(string=["h2", "h3", "h1"]) # Adjust the tag as needed  
        print("Processing contents of H2")    
        print("-"*100)

        for article in articles:
            print("\n")
            print("-"*100)
            print("-", article.get_text(strip=True))

        articles = soup.find_all('h3') # Adjust the tag as needed
        print("Processing contents of h3")    
        print("-"*100)
        # articles = soup.find_all(string=["h2", "h3", "h1"]) # Adjust the tag as needed      
        for article in articles:
            print("\n")
            print("-"*100)
            print("-", article.get_text(strip=True))
            
        articles = soup.find_all('h4') # Adjust the tag as needed
        print("Processing contents of h4")    
        print("-"*100)
        # articles = soup.find_all(string=["h2", "h3", "h1"]) # Adjust the tag as needed      
        for article in articles:
            print("\n")
            print("-"*100)
            print("-", article.get_text(strip=True))


# Pagination and process the pages
        print("-"*100)
        print("\n")
        next_link = soup.find('a', string='Next') # Adjust if "Next" is a symbol or image 
        if next_link:
            current_url = urljoin(current_url, next_link['href'])
            #print(f"New URL is :  {current_url}:")
        else:
            break






# Replace this with your actual starting URL
# start_url = 'https://en.wikipedia.org/wiki/Agentic_AI'
# start_url="https://www.cricbuzz.com/"

start_url="https://www.cricbuzz.com/cricket-team/papua-new-guinea/287"

scrape_site(start_url)

