# Flask REST API for Movies

A simple and lightweight RESTful API for managing a collection of movies. This project demonstrates full CRUD (Create, Read, Update, Delete) functionality using Flask, Flask-RESTful, and SQLAlchemy with a SQLite database.

## Features

-   **List all movies:** Retrieve the entire collection of movies.
-   **Add a new movie:** Add a new movie to the collection.
-   **Update a movie:** Modify the details of an existing movie.
-   **Delete a movie:** Remove a movie from the collection.
-   **Input Validation:** Ensures that required fields (`title`, `director`, `release_year`) are provided for creating and updating movies.

## Technologies Used

-   **Backend:** Python
-   **Framework:** Flask
-   **API Extension:** Flask-RESTful
-   **Database ORM:** Flask-SQLAlchemy
-   **Database:** SQLite

---

## Prerequisites

Before you begin, ensure you have the following installed on your system:
-   Python 3.8+
-   `pip` (Python package installer)
-   Git (for version control)

## Installation and Setup

Follow these steps to get the application running on your local machine.

**1. Clone the Repository (or download the source code):**
```bash
git clone <your-repository-url>
cd flask-movie-api
```

**2. Create and Activate a Virtual Environment:**
It is highly recommended to use a virtual environment to manage project dependencies.

*   **For macOS/Linux:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

*   **For Windows:**
    ```bash
    python -m venv venv
    .\venv\Scripts\activate
    ```

**3. Install Dependencies:**
The required packages are listed in `requirements.txt`. Install them using pip.
```bash
pip install -r requirements.txt
```
*(Note: If you haven't created a `requirements.txt` file yet, you can do so by running `pip freeze > requirements.txt`)*

**4. Run the Application:**
This command will start the Flask development server. The first time you run it, a `movies.db` SQLite database file will be created automatically.
```bash
python app.py
```
The API will now be running at `http://127.0.0.1:5000`.

---

## API Endpoints

The API provides the following endpoints to manage movies.

| Method | Endpoint             | Description                       | Request Body (JSON)                                                              | Successful Response (JSON)                                                                  |
| :----- | :------------------- | :-------------------------------- | :------------------------------------------------------------------------------- | :------------------------------------------------------------------------------------------ |
| `GET`    | `/movies`            | Get a list of all movies.         | _(None)_                                                                         | `[ { "id": 1, "title": "...", ... }, { "id": 2, ... } ]`                                     |
| `POST`   | `/movies`            | Add a new movie to the collection.| `{ "title": "Inception", "director": "Christopher Nolan", "release_year": 2010 }` | `{ "id": 3, "title": "Inception", "director": "...", "release_year": 2010 }` (Status: 201) |
| `GET`    | `/movies/<int:id>`   | Get a single movie by its ID.     | _(None)_                                                                         | `{ "id": 1, "title": "...", "director": "...", "release_year": ... }`                      |
| `PATCH`  | `/movies/<int:id>`   | Update an existing movie.         | `{ "title": "The Dark Knight Rises", "director": "...", "release_year": 2012 }`    | `{ "id": 1, "title": "The Dark Knight Rises", "director": "...", "release_year": 2012 }`   |
| `DELETE` | `/movies/<int:id>`   | Delete a movie by its ID.         | _(None)_                                                                         | `{ "message": "Movie deleted successfully" }`                                               |


## How to Test the API

You can use any API client like [Postman](https://www.postman.com/) or the [Thunder Client](https://www.thunderclient.com/) extension for VS Code to test the endpoints.

**Example: Creating a new movie**
-   **Method:** `POST`
-   **URL:** `http://127.0.0.1:5000/movies`
-   **Body (raw, JSON):**
    ```json
    {
        "title": "Interstellar",
        "director": "Christopher Nolan",
        "release_year": 2014
    }
    ```

**Example: Updating a movie with ID `1`**
-   **Method:** `PATCH`
-   **URL:** `http://127.0.0.1:5000/movies/1`
-   **Body (raw, JSON):**
    ```json
    {
        "title": "Interstellar (IMAX Edition)",
        "director": "Christopher Nolan",
        "release_year": 2014
    }
    ```
