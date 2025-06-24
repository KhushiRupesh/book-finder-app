# File: backend/main.py

import asyncio
import httpx
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from bs4 import BeautifulSoup

# --- App and CORS Setup ---
app = FastAPI()
origins = ["http://localhost", "http://127.0.0.1", "null"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, allow_credentials=True, allow_methods=["*"], allow_headers=["*"],
)

# --- Base URLs ---
GUTENBERG_BASE_URL = "https://www.gutenberg.org"
OPENLIBRARY_SEARCH_URL = "https://openlibrary.org/search.json"
COVER_BASE_URL = "https://covers.openlibrary.org/b/id/"

# --- Asynchronous Scraper/API Functions ---

async def search_gutenberg(client: httpx.AsyncClient, query: str):
    """Asynchronously searches Project Gutenberg and returns top results."""
    try:
        url = f"{GUTENBERG_BASE_URL}/ebooks/search/?query={query}"
        response = await client.get(url, follow_redirects=True)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        books = []
        for item in soup.select('li.booklink')[:5]: # Get top 5 results
            books.append({
                "source": "Project Gutenberg",
                "title": item.select_one('.title').get_text(strip=True),
                "author": item.select_one('.subtitle').get_text(strip=True),
                "url": GUTENBERG_BASE_URL + item.select_one('a.link')['href'],
                "cover_url": None, # Gutenberg doesn't provide covers
                "action": "Download"
            })
        return books
    except Exception as e:
        print(f"Error scraping Gutenberg: {e}")
        return []

async def search_open_library(client: httpx.AsyncClient, query: str):
    """Asynchronously searches Open Library API and returns top results."""
    try:
        params = {"q": query, "limit": 5} # Get top 5 results
        response = await client.get(OPENLIBRARY_SEARCH_URL, params=params)
        response.raise_for_status()
        data = response.json()
        
        books = []
        for item in data.get('docs', []):
            cover_id = item.get('cover_i')
            books.append({
                "source": "Open Library",
                "title": item.get('title', 'Unknown Title'),
                "author": ", ".join(item.get('author_name', [])),
                "url": "https://openlibrary.org" + item.get('key', ''),
                "cover_url": f"{COVER_BASE_URL}{cover_id}-M.jpg" if cover_id else None,
                "action": "Borrow Online"
            })
        return books
    except Exception as e:
        print(f"Error fetching from Open Library: {e}")
        return []

# --- Main API Endpoint ---

@app.get("/search/{query}")
async def search_all_sources(query: str):
    """
    Searches all available sources concurrently and returns a merged list of results.
    """
    async with httpx.AsyncClient() as client:
        # Run both searches at the same time
        gutenberg_task = search_gutenberg(client, query)
        open_library_task = search_open_library(client, query)
        
        results = await asyncio.gather(
            gutenberg_task,
            open_library_task
        )
    
    # The results will be a list of lists, e.g., [[gutenberg_books], [open_library_books]]
    # Flatten the list and return
    all_books = [book for sublist in results for book in sublist]
    
    # (Optional but good) De-duplicate results based on title
    unique_books = []
    seen_titles = set()
    for book in all_books:
        if book['title'].lower() not in seen_titles:
            unique_books.append(book)
            seen_titles.add(book['title'].lower())
            
    if not unique_books:
        raise HTTPException(status_code=404, detail="No books found from any source.")
        
    return unique_books