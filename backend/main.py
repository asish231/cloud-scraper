from fastapi import FastAPI, HTTPException
import requests
from bs4 import BeautifulSoup
from googlesearch import search
from typing import List
import uvicorn

app = FastAPI()

def find_websites(query: str, num_results: int = 5) -> List[str]:
    """Search Google for websites related to the query."""
    return list(search(query, num=num_results, stop=num_results, pause=2))

def scrape_website(url: str) -> str:
    """Scrape text content from the provided URL."""
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
        text_data = []
        for element in soup.find_all(["p", "h1", "h2", "h3", "li"]):
            text_data.append(element.get_text(strip=True))
        return "\n".join(text_data)
    except Exception as e:
        return f"Error scraping {url}: {str(e)}"

@app.get("/scrape")
def scrape_data(query: str):
    """Endpoint to search and scrape websites based on a query."""
    websites = find_websites(query)
    if not websites:
        raise HTTPException(status_code=404, detail="No relevant websites found.")
    all_data = {}
    for site in websites:
        all_data[site] = scrape_website(site)
    return {"data": all_data}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
