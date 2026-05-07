import requests
from bs4 import BeautifulSoup
from database import create_table, insert_quotes

def scrape_quotes():
    url = "http://quotes.toscrape.com/"
    response = requests.get(url)

    soup = BeautifulSoup(response.text, "html.parser")

    quotes_data = []

    quotes = soup.find_all("div", class_="quote")

    for q in quotes:
        text = q.find("span", class_="text").text
        author = q.find("small", class_="author").text
        tags = [tag.text for tag in q.find_all("a", class_="tag")]

        quotes_data.append({
            "text": text,
            "author": author,
            "tags": tags
        })

    return quotes_data


if __name__ == "__main__":
    data = scrape_quotes()

    create_table()
    insert_quotes(data)

    print("Data saved to database!")