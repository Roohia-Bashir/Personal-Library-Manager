import streamlit as st # type: ignore
import json
import os
from datetime import datetime

# Set page config
st.set_page_config(
    page_title="Personal Library Manager",
    page_icon="📚",
    layout="wide"
)

# Apply white theme
st.markdown("""
<style>
    .stApp {
        background-color: #ffffff;
        color: #333333;
    }
    .stButton>button {
        background-color: #4b0082;
        color: white;
    }
    .stTextInput>div>div>input, .stNumberInput>div>div>input {
        background-color: #f8f8f8;
        color: #333333;
        border: 1px solid #ddd;
    }
    .stSelectbox>div>div>div {
        background-color: #f8f8f8;
        color: #333333;
    }
    /* Fix dropdown visibility */
    .stSelectbox>div>div {
        color: #333333 !important;
        background-color: #f8f8f8 !important;
    }
    .stSelectbox [data-baseweb="select"] {
        color: #333333 !important;
    }
    .stSelectbox [data-baseweb="popover"] {
        background-color: white !important;
        color: #333333 !important;
    }
    h1, h2, h3 {
        color: #4b0082;
    }
    .stDataFrame {
        background-color: #f8f8f8;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: #f0f0f0;
        border-radius: 4px 4px 0px 0px;
        gap: 1px;
        padding-top: 10px;
        padding-bottom: 10px;
        color: #333333;
    }
    .stTabs [aria-selected="true"] {
        background-color: #4b0082;
        color: white;
    }
    /* Center footer */
    footer {
        text-align: center !important;
    }
    .footer-text {
        text-align: center;
        width: 100%;
        margin-top: 20px;
        padding: 10px;
        font-size: 14px;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state for library if it doesn't exist
if 'library' not in st.session_state:
    st.session_state.library = []
    
    # Load library from file if it exists
    if os.path.exists('library.json'):
        try:
            with open('library.json', 'r') as file:
                st.session_state.library = json.load(file)
        except Exception:
            # If there's an error, start with sample books
            st.session_state.library = [
                {
                    "id": "1",
                    "title": "The Great Gatsby",
                    "author": "F. Scott Fitzgerald",
                    "year": 1925,
                    "genre": "Fiction",
                    "read": True
                },
                {
                    "id": "2",
                    "title": "1984",
                    "author": "George Orwell",
                    "year": 1949,
                    "genre": "Dystopian",
                    "read": False
                }
            ]
    else:
        # Start with sample books
        st.session_state.library = [
            {
                "id": "1",
                "title": "The Great Gatsby",
                "author": "F. Scott Fitzgerald",
                "year": 1925,
                "genre": "Fiction",
                "read": True
            },
            {
                "id": "2",
                "title": "1984",
                "author": "George Orwell",
                "year": 1949,
                "genre": "Dystopian",
                "read": False
            }
        ]

# Function to save library to file
def save_library():
    try:
        with open('library.json', 'w') as file:
            json.dump(st.session_state.library, file, indent=2)
        return True
    except Exception:
        return False

# Main title
st.title("📚 Personal Library Manager")

# Create tabs for different sections
tabs = st.tabs(["📋 All Books", "➕ Add Book", "🗑️ Remove Book", "🔍 Search", "📊 Statistics"])

# All Books Tab
with tabs[0]:
    st.header("Your Library")
    
    if not st.session_state.library:
        st.info("Your library is empty. Add some books to get started!")
    else:
        # Display books in a table
        import pandas as pd
        
        # Convert to a format suitable for display
        books_for_display = []
        for book in st.session_state.library:
            books_for_display.append({
                "Title": book['title'],
                "Author": book['author'],
                "Year": book['year'],
                "Genre": book['genre'],
                "Status": "Read" if book['read'] else "Unread"
            })
        
        # Display as a dataframe
        df = pd.DataFrame(books_for_display)
        st.dataframe(df, use_container_width=True)

# Add Book Tab
with tabs[1]:
    st.header("Add a New Book")
    
    with st.form("add_book_form"):
        title = st.text_input("Title")
        author = st.text_input("Author")
        year = st.number_input("Publication Year", min_value=1000, max_value=datetime.now().year, value=datetime.now().year)
        
        # Provide some common genres as examples
        genre_options = ["Fiction", "Non-Fiction", "Mystery", "Science Fiction", "Fantasy", "Romance", "Horror", "Thriller", "Biography", "History", "Other"]
        genre = st.selectbox("Genre", options=genre_options)
        read = st.checkbox("I have read this book")
        
        submit_button = st.form_submit_button("Add Book")
        
        if submit_button:
            if title and author:
                # Create new book
                new_book = {
                    "id": str(datetime.now().timestamp()),
                    "title": title,
                    "author": author,
                    "year": year,
                    "genre": genre,
                    "read": read
                }
                
                # Add to library
                st.session_state.library.append(new_book)
                
                # Save to file
                save_library()
                
                st.success(f"Added: {title} by {author}")
            else:
                st.error("Title and author are required.")

# Remove Book Tab
with tabs[2]:
    st.header("Remove a Book")
    
    if not st.session_state.library:
        st.info("Your library is empty. Nothing to remove.")
    else:
        book_to_remove = st.selectbox(
            "Select a book to remove",
            options=[f"{book['title']} by {book['author']}" for book in st.session_state.library],
            key="remove_book_select"
        )
        
        if st.button("Remove Selected Book"):
            # Extract title from the selection
            title_to_remove = book_to_remove.split(" by ")[0]
            
            # Find and remove the book
            initial_length = len(st.session_state.library)
            st.session_state.library = [book for book in st.session_state.library if book['title'] != title_to_remove]
            
            if len(st.session_state.library) < initial_length:
                save_library()
                st.success(f"Removed: {book_to_remove}")
                # Use st.rerun() instead of st.experimental_rerun()
                st.rerun()
            else:
                st.error("Failed to remove book.")

# Search Tab
with tabs[3]:
    st.header("Search Books")
    
    search_by = st.radio("Search by", ["Title", "Author"])
    search_query = st.text_input("Enter search term")
    
    if st.button("Search") and search_query:
        search_field = search_by.lower()
        
        # Search for books
        results = []
        for book in st.session_state.library:
            if search_query.lower() in book[search_field].lower():
                results.append(book)
        
        if not results:
            st.info(f"No books found matching '{search_query}'")
        else:
            st.success(f"Found {len(results)} matching books")
            
            # Display results
            search_results = []
            for i, book in enumerate(results, 1):
                read_status = "Read" if book['read'] else "Unread"
                search_results.append({
                    "Title": book['title'],
                    "Author": book['author'],
                    "Year": book['year'],
                    "Genre": book['genre'],
                    "Status": read_status
                })
            
            import pandas as pd
            st.dataframe(pd.DataFrame(search_results), use_container_width=True)

# Statistics Tab
with tabs[4]:
    st.header("Library Statistics")
    
    total_books = len(st.session_state.library)
    read_books = sum(1 for book in st.session_state.library if book['read'])
    percentage_read = (read_books / total_books * 100) if total_books > 0 else 0
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Total Books", total_books)
        st.metric("Books Read", read_books)
        
        # Progress bar for reading progress
        st.subheader("Reading Progress")
        st.progress(percentage_read / 100)
        st.write(f"{percentage_read:.1f}% of books read")
    
    with col2:
        if total_books > 0:
            st.subheader("Genre Distribution")
            
            # Count genres
            genres = {}
            for book in st.session_state.library:
                genre = book['genre']
                if genre in genres:
                    genres[genre] += 1
                else:
                    genres[genre] = 1
            
            # Display as a bar chart using Streamlit's built-in chart
            import pandas as pd
            
            # Sort genres by count
            sorted_genres = sorted(genres.items(), key=lambda x: x[1], reverse=True)
            
            # Create dataframe
            genres_df = pd.DataFrame({
                'Genre': [g[0] for g in sorted_genres],
                'Count': [g[1] for g in sorted_genres]
            })
            
            # Use Streamlit's built-in bar chart
            st.bar_chart(genres_df.set_index('Genre'))

# Save library when the app is about to close
if st.button("Save and Exit"):
    if save_library():
        st.success("Library saved successfully!")
        st.balloons()
    else:
        st.error("Failed to save library.")

# footer with attribution
st.markdown("---")
st.markdown("<div class='footer-text'>Personal Library Manager © 2025<br>Created by Roohia_Bashir</div>", unsafe_allow_html=True)