import requests
from bs4 import BeautifulSoup

def scrape_metadata(url):
    try:
        response = requests.get(url, timeout=5)
        soup = BeautifulSoup(response.text, 'html.parser')

        title = soup.title.string if soup.title else ""
        meta_desc = soup.find("meta", {"name": "description"})
        description = meta_desc["content"] if meta_desc else ""

        return {
            "url": url,
            "title": title,
            "description": description
        }
    except:
        return None
