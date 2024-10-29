import requests
from bs4 import BeautifulSoup

def scrape_page(url):
    # Send a GET request to the URL
    response = requests.get(url)
    
    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract all paragraphs (inside <p> tags)
        paragraphs = soup.find_all('p')
        
        # Join all the paragraph text into one string, separated by new lines
        scraped = "\n".join([para.get_text() for para in paragraphs])
        
        return scraped
    else:
        # Return None if the request fails
        return None
    