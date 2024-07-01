import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Sample dataset (or use your own dataset)
data = {
    'title': [
        'Atomic Habits',
        'The Lean Startup',
        'Sapiens',
        'Thinking, Fast and Slow',
        'Becoming',
        'The Subtle Art of Not Giving a F*ck',
        'Educated',
        'The Power of Habit',
        'Start with Why',
        'The Four Agreements'
    ],
    'author': [
        'James Clear',
        'Eric Ries',
        'Yuval Noah Harari',
        'Daniel Kahneman',
        'Michelle Obama',
        'Mark Manson',
        'Tara Westover',
        'Charles Duhigg',
        'Simon Sinek',
        'Don Miguel Ruiz'
    ],
    'genre': [
        'Self-Help',
        'Business',
        'History',
        'Psychology',
        'Autobiography',
        'Self-Help',
        'Memoir',
        'Psychology',
        'Leadership',
        'Personal Development'
    ],
    'description': [
        'Atomic Habits offers a proven framework for improving—every day. Tiny changes, remarkable results.',
        'The Lean Startup methodology provides a scientific approach to creating and managing startups.',
        'Sapiens explores how Homo sapiens became the dominant species through cognitive, agricultural, and scientific revolutions.',
        'Thinking, Fast and Slow reveals how our minds are tripped up by error and prejudice, and how we can think more clearly.',
        'Becoming shares Michelle Obama\'s journey from a girl on the South Side of Chicago to First Lady of the United States.',
        'The Subtle Art of Not Giving a F*ck is a refreshing take on how to live a good life by focusing on what truly matters.',
        'Educated is a memoir about a woman who grew up in a strict and abusive household but goes on to earn a PhD from Cambridge University.',
        'The Power of Habit explores why habits exist and how they can be changed to improve individual and organizational success.',
        'Start with Why shows that the leaders who\'ve had the greatest influence in the world all think, act, and communicate the same way.',
        'The Four Agreements offers a powerful code of conduct that can rapidly transform our lives to a new experience of freedom, true happiness, and love.'
    ]
}

df = pd.DataFrame(data)

# Initialize TF-IDF vectorizer
tfidf = TfidfVectorizer(stop_words='english')

# Fit and transform the description text
tfidf_matrix = tfidf.fit_transform(df['description'])

# Compute cosine similarity matrix
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

# Recommendation function
def recommend_books_by_genres(genres):
    # Filter books by selected genres
    genre_books = df[df['genre'].isin(genres)]

    # Reset index for filtered DataFrame
    genre_books = genre_books.reset_index(drop=True)

    # Get TF-IDF matrix indices for filtered books
    indices = genre_books.index

    # Compute cosine similarity for filtered books
    genre_cosine_sim = cosine_sim[indices, :][:, indices]

    # Initialize an empty list to store recommendations
    recommendations = []

    # Iterate over each genre
    for genre in genres:
        # Get books in the current genre
        genre_subset = genre_books[genre_books['genre'] == genre]

        # Iterate over each book in the current genre
        for idx, row in genre_subset.iterrows():
            # Get index of current book
            book_idx = row.name

            # Get similarity scores
            sim_scores = list(enumerate(genre_cosine_sim[book_idx]))

            # Sort books based on similarity scores
            sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

            # Get top 5 recommendations (excluding itself)
            top_books = sim_scores[1:6]

            # Get book titles from indices
            recommended_books = [genre_books.iloc[score[0]]['title'] for score in top_books]

            # Add current book and its recommendations to the list
            recommendations.append({
                'Book': row['title'],
                'Recommendations': recommended_books
            })

    return recommendations[:5]  # Limit to 5 recommendations total
