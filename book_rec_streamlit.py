import streamlit as st
import requests

# Function to get books based on genre
def get_books_by_genre(genre, api_key, max_results=5):
    url = f"https://www.googleapis.com/books/v1/volumes?q=subject:{genre}&maxResults={max_results}&key={api_key}"
    st.write(f"Request URL: {url}")  # Print the URL for debugging
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        books = data.get("items", [])
        return books
    else:
        st.error(f"Failed to fetch data from Google Books API: {response.status_code} - {response.text}")
        return []

# Streamlit app
def main():
    st.title("Book Recommender")
    
    #api_key = st.secrets["GOOGLE_BOOKS_API_KEY"]  # Store your API key in Streamlit secrets
    api_key="AIzaSyDdotkNKAbVrpN6si7XS9sti3S0hj2pAF8"

    genres = [
        "ARCHITECTURE", "LITERARY CRITICISM", "ART", "MATHEMATICS", "BIBLES", "MEDICAL",
        "BIOGRAPHY & AUTOBIOGRAPHY", "MUSIC", "BODY, MIND & SPIRIT", "NATURE", "BUSINESS & ECONOMICS",
        "PERFORMING ARTS", "COMICS & GRAPHIC NOVELS", "PETS", "COMPUTERS", "PHILOSOPHY", "COOKING",
        "PHOTOGRAPHY", "CRAFTS & HOBBIES", "POETRY", "DESIGN", "POLITICAL SCIENCE", "DRAMA",
        "PSYCHOLOGY", "EDUCATION", "REFERENCE", "FAMILY & RELATIONSHIPS", "RELIGION", "FICTION",
        "SCIENCE", "FOREIGN LANGUAGE STUDY", "SELF-HELP", "GAMES & ACTIVITIES", "SOCIAL SCIENCE",
        "GARDENING", "SPORTS & RECREATION", "HEALTH & FITNESS", "STUDY AIDS", "HISTORY",
        "TECHNOLOGY & ENGINEERING", "HOUSE & HOME", "TRANSPORTATION", "HUMOR", "TRAVEL",
        "JUVENILE FICTION", "TRUE CRIME", "JUVENILE NONFICTION", "YOUNG ADULT FICTION",
        "LANGUAGE ARTS & DISCIPLINES"
    ]
    
    genre = st.selectbox("Select a genre", genres)
    
    if st.button("Get Recommendations"):
        books = get_books_by_genre(genre, api_key)
        if books:
            st.subheader(f"Top 5 Books in {genre}")
            for book in books:
                title = book["volumeInfo"].get("title", "No title")
                authors = ", ".join(book["volumeInfo"].get("authors", ["No authors"]))
                description = book["volumeInfo"].get("description", "No description")
                st.write(f"**Title:** {title}")
                st.write(f"**Authors:** {authors}")
                st.write(f"**Description:** {description}")
                st.write("---")
        else:
            st.write("No books found for the selected genre.")

if __name__ == "__main__":
    main()
