from fastapi import FastAPI, HTTPException
import requests
from bs4 import BeautifulSoup
from googlesearch import search  # Ensure you install 'googlesearch-python'
from typing import List
import uvicorn

app = FastAPI()

def find_websites(query: str, num_results: int = 5) -> List[str]:
    """Search Google for websites related to the query."""
    try:
        return list(search(query, num=num_results, stop=num_results, pause=2))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Google Search Error: {str(e)}")

def scrape_website(url: str) -> str:
    """Scrape text content from the provided URL."""
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                          "(KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()  # Raise error for HTTP issues
        soup = BeautifulSoup(response.text, "html.parser")

        text_data = []
        for element in soup.find_all(["p", "h1", "h2", "h3", "li"]):
            text_data.append(element.get_text(strip=True))

        return "\n".join(text_data) if text_data else "No readable text found."
    except requests.exceptions.RequestException as e:
        return f"Error fetching {url}: {str(e)}"

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
