import streamlit as st
from ipynb.fs.full.recom1 import (
    recommend_books_collaborative,
    recommend_books_content_based,
    hybrid_recommendation,
    recommend_books_content_based_photo
)

# Set the title of the app with custom HTML
st.markdown("<h1 style='text-align: center; color: #ffcd00;'>Book Recommendation System 📚</h1>", unsafe_allow_html=True)

# Custom CSS to style the app
st.markdown("""
    <style>
        /* Google Font for better typography */
        @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap');

        body {
        
            
            color: #ffffff;  /* White text */
            font-family: 'Roboto', sans-serif;
            padding: 20px; /* Add padding around the body */
        }
        .stButton>button {
            background: linear-gradient(90deg, #ffcd00, #f8b400);
            color: white;  /* White text color */
            font-weight: bold;
            border-radius: 5px;
            padding: 10px 20px;
            border: none;
            transition: background-color 0.3s, color 0.3s; /* Added transition for color */
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.4);
        }
        .stButton>button:hover {
            background-color: #f8b400; /* Darker yellow on hover */
            color: white; /* Keep text white on hover */
        }
        .card {
            background-color: #1a1a1a; /* Card background */
            border-radius: 10px;
            padding: 10px;
            margin: 10px 0;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
        }
        .book-title {
            font-size: 1.5em;
            font-weight: bold;
            margin: 10px 0;
            text-align: center;
            transition: color 0.2s; /* Smooth transition */
            color: #ffffff; /* Set default color to white */
        }
        .image-container {
            display: flex;
            justify-content: center;
            margin: 10px 0;
        }
        img {
            border-radius: 10px; /* Rounded corners for images */
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.5);
            transition: transform 0.3s; /* Smooth scaling */
        }
        img:hover {
            transform: scale(1.1); /* Slightly enlarge on hover */
        }
    </style>
""", unsafe_allow_html=True)

# Input for book title
book_title = st.text_input("Enter a Book Title:", value="PLEADING GUILTY")

# Button to generate recommendations
if st.button("Get Recommendations"):
    # Content-Based Recommendations
    st.subheader("Content-Based Recommendations:")
    content_based_recommendations = recommend_books_content_based_photo(book_title)

    # Display the recommendations
    for recommendation in content_based_recommendations:
        # Display the book title inside a card
        st.markdown(f"<div class='card'><div class='book-title'>{recommendation['title']}</div>", unsafe_allow_html=True)
        
        # Display the book image if available
        if recommendation['image_url']:
            st.image(recommendation['image_url'], width=200)  # Adjust width as needed
        else:
            st.write("Image not available")

        st.markdown("</div>", unsafe_allow_html=True)  # Close the card div
