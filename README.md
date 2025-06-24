# Full-Stack E-Book Finder

![App Screenshot](https://i.imgur.com/gK9xJYW.png)

A full-stack web application that searches multiple sources (Project Gutenberg and the Open Library API) to find and display legally free e-books. The project features a modern, responsive frontend and a powerful Python API backend.

---

## ✨ Key Features

* **Multi-Source Aggregation:** Fetches and merges results from both the Project Gutenberg and the Open Library in a single search.
* **Asynchronous Backend:** Built with FastAPI and `asyncio`, the backend performs concurrent requests to data sources for a fast user experience.
* **Rich Data Display:** The UI displays book covers (from Open Library), titles, authors, and the source of the book.
* **Context-Aware Actions:** Provides a "Download" link for public domain books from Project Gutenberg and a "Borrow Online" link for books from the Open Library.
* **Aesthetic UI:** A clean, responsive, dark-mode interface built with Tailwind CSS.

---

## 🛠️ Tech Stack

### Backend
* **Language:** Python 3
* **Framework:** FastAPI
* **Server:** Uvicorn
* **HTTP Client:** HTTPX (for asynchronous requests)
* **HTML Parsing:** BeautifulSoup4

### Frontend
* **Structure:** HTML5
* **Styling:** Tailwind CSS
* **Logic:** Vanilla JavaScript (ES6+)

---

## 🚀 Getting Started

Follow these instructions to get a copy of the project up and running on your local machine.

### Prerequisites

* Python 3.8+
* Git
* A web browser

### Installation & Setup

1.  **Clone the repository:**
    ```sh
    git clone [https://github.com/YOUR_USERNAME/api-book-finder.git](https://github.com/YOUR_USERNAME/api-book-finder.git)
    cd api-book-finder
    ```

2.  **Set up the backend:**
    ```sh
    # Navigate into the backend directory
    cd backend

    # Create and activate a virtual environment
    python -m venv venv
    # Windows:
    .\venv\Scripts\activate
    # macOS/Linux:
    source venv/bin/activate

    # Install the required packages
    pip install -r requirements.txt
    ```

### Running the Application

This project has two parts that need to be running at the same time: the backend API and the frontend client.

1.  **Start the Backend Server:**
    * In a terminal, make sure you are in the `backend` directory with your virtual environment activated.
    * Run the Uvicorn server:
        ```sh
        uvicorn main:app --reload
        ```
    * The API will now be running at `http://127.0.0.1:8000`.

2.  **Launch the Frontend:**
    * Navigate to the `frontend` folder in your file explorer.
    * Open the `index.html` file directly in your web browser.

You can now search for books in the browser!

---

## 📚 API Endpoints

The backend exposes the following endpoint:

* **`GET /search/{query}`**
    * Searches all configured data sources for the given query.
    * Returns a JSON array of book objects, each containing a `title`, `author`, `source`, `url`, `cover_url`, and `action`.
    * Returns a `404` error if no books are found.

---

## 🔮 Future Improvements

- [ ] Deploy the backend to a cloud service like Render.
- [ ] Deploy the frontend to a static host like Netlify or Vercel.
- [ ] Add a database (SQLite) to cache results and reduce redundant scraping.
- [ ] Implement more advanced error handling and logging.