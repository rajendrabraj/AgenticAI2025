## RB - 31.05.2025 , This Program is to take input a URL and extract all the content URL's within the URL
#  RB - this program make use of BeautifulSoup and checks the embedded URLS within the website.
#  RB - this makes use of BeautifulSoup 


import requests
from bs4 import BeautifulSoup
import re


def get_links_from_url(url):
    """
    Fetches the content of a given URL and extracts all hyperlinks.

    Args:
        url (str): The URL of the webpage to scrape.

    Returns:
        list: A list of all extracted URLs (href attributes of <a> tags).
    """
    try:
        # Send an HTTP GET request to the URL
        response = requests.get(url)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx or 5xx)

        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all anchor tags (<a>) and extract their 'href' attribute
        
        # print(new_url)

        links = []
        for a_tag in soup.find_all('a', href=True):
            #links.append(a_tag['href'])
            new_url = url[:-1]
            str_pattern="https"
            text_string=a_tag['href']

            if re.search(str_pattern, text_string):
                # print("Found")   
                new_url = a_tag['href']     
            else:
                new_url = new_url + a_tag['href']
                # print("Not Found")
            if re.search("Javascript", new_url):
                # print("Found")   
                ## Skip this URL and don't add to array.
                new_url = None     
            else:
                # print(new_url)
                links.append(new_url) 
                # print("Not Found")
                                
           
            #get data of the extracted URL inside the web page
            # get_data_contents(new_url)  
            print(new_url)
            new_url = None          
            print("\n") 
                    
        return links

    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL {url}: {e}")
        return []
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return []


## This function extracts the data inside the URL 
def get_data_contents(start_url):
# start_url = "https://en.wikipedia.org/wiki/Agentic_AI"
    current_url = start_url
    print("Inside the DATA FUNCTION.........")
    print("Input URL received : {current_url}  ")
    print("\n")
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
            print("-"*100)
            print("-", article.get_text(strip=True))
        
        articles = soup.find_all('h3') # Adjust the tag as needed
        print("Processing contents of h3")    
        print("-"*100)
        # articles = soup.find_all(string=["h2", "h3", "h1"]) # Adjust the tag as needed      
        for article in articles:
            print("-"*100)
            print("-", article.get_text(strip=True))
            
            
# Pagination and process the pages
        # print("-"*100)
        # print("\n")
        # next_link = soup.find('a', string='Next') # Adjust if "Next" is a symbol or image 
        # if next_link:
        #     current_url = urljoin(current_url, next_link['href'])
        #     #print(f"New URL is :  {current_url}:")
        # else:
        #     break

# # 🔍 Replace this with your actual starting URL
# # start_url = 'https://en.wikipedia.org/wiki/Agentic_AI'
# start_url="https://www.cricbuzz.com/"
# get_data_contents(start_url)


## Execute this program.

# Example usage:
if __name__ == "__main__":
    # target_url = "https://www.example.com"  # Replace with the URL you want to scrape
    target_url = "https://www.cricbuzz.com/"

    extracted_links = get_links_from_url(target_url)

    if extracted_links:
        print(f"Links found on {target_url}:")
        for link in extracted_links:
            print(link)
    else:
        print(f"No links found or an error occurred while processing {target_url}.")

