import requests
from bs4 import BeautifulSoup
import json

BASE_URL = "http://quotes.toscrape.com"

all_quotes = []
authors_info = {}
visited_authors = set()

def get_author_details(author_url):
    response = requests.get(BASE_URL + author_url)
    soup = BeautifulSoup(response.text, "html.parser")
    
    name = soup.find("h3", class_="author-title").get_text(strip=True)
    born_date = soup.find("span", class_="author-born-date").get_text(strip=True)
    born_location = soup.find("span", class_="author-born-location").get_text(strip=True)
    description = soup.find("div", class_="author-description").get_text(strip=True)
    
    return {
        "fullname": name,
        "born_date": born_date,
        "born_location": born_location,
        "description": description
    }

def scrape():
    url = "/page/1/"
    
    while url:
        response = requests.get(BASE_URL + url)
        soup = BeautifulSoup(response.text, "html.parser")

        quotes = soup.find_all("div", class_="quote")
        for quote in quotes:
            text = quote.find("span", class_="text").get_text(strip=True)
            author = quote.find("small", class_="author").get_text(strip=True)
            tags = [tag.get_text(strip=True) for tag in quote.find_all("a", class_="tag")]
            
            all_quotes.append({
                "tags": tags,
                "author": author,
                "quote": text
            })
            
            author_link = quote.find("a")["href"]
            if author not in visited_authors:
                author_data = get_author_details(author_link)
                authors_info[author] = author_data
                visited_authors.add(author)

        next_btn = soup.find("li", class_="next")
        url = next_btn.find("a")["href"] if next_btn else None

    # Save to JSON
    with open("quotes.json", "w", encoding="utf-8") as qf:
        json.dump(all_quotes, qf, ensure_ascii=False, indent=2)

    with open("authors.json", "w", encoding="utf-8") as af:
        json.dump(list(authors_info.values()), af, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    scrape()