from search_api import search_google
from url_filter import is_valid
from scraper import scrape_metadata
from visual_scraper import extract_text_visual
from indexer import load_index, save_index, is_duplicate, add_to_index

API_KEY = "AIzaSyDU4DfnApEHDMe9yKRNV6Aa1oB_jS0-rYY"
CSE_ID = "e2050d8d70f194311"

def run_scraping(query):
    urls = search_google(query, API_KEY, CSE_ID)
    index = load_index()

    for url in urls:
        if not is_valid(url) or is_duplicate(url, index):
            continue

        print(f"Scraping: {url}")
        metadata = scrape_metadata(url)
        if metadata:
            add_to_index(url, metadata, index)
        else:
            visual_data = extract_text_visual(url)
            add_to_index(url, visual_data, index)

    save_index(index)
    return index  # retourne l’index pour usage ultérieur

def main():
    query = input("Recherche : ")
    run_scraping(query)

if __name__ == "__main__":
    main()
