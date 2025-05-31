## RB - 31.05.2025 , This Program is to take input a URL and extract all the content URL's within the URL
# RB - this program make use of BeautifulSoup


import requests
from bs4 import BeautifulSoup


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
            new_url = new_url + a_tag['href']
            # print(new_url)
            links.append(new_url)   
            new_url = None
            print("\n") 
                    
        return links

    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL {url}: {e}")
        return []
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return []

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

