
# Personal Library Manager

A simple and interactive library management system built with Streamlit. This app allows you to manage your personal library by adding, removing, searching, and analyzing books. It supports basic library features such as tracking read/unread status and genre distribution.

## Features

- **View all books**: Display a list of all books in your library with details such as title, author, year, genre, and read status.
- **Add new books**: Easily add books by providing details like title, author, year, genre, and read status.
- **Remove books**: Remove books from your library.
- **Search books**: Search for books by title or author.
- **Library statistics**: View statistics on your library such as total books, books read, and genre distribution.

## Requirements

- Python 3.11 or higher
- Streamlit (for the frontend interface)
- Pandas (for displaying data tables)
- JSON (to save and load library data)

## Installation

1. Clone the repository to your local machine:
   ```bash
   git clone https://github.com/Roohia-Bashir/Personal-Library-Manager.git
Navigate to the project directory:

bash
Copy
cd library-manager
Create and activate a virtual environment:

On Windows:

bash
Copy
python -m venv .venv
.venv\Scripts\activate
On macOS/Linux:

bash
Copy
python -m venv .venv
source .venv/bin/activate
Install the required dependencies:

bash
Copy
pip install streamlit pandas
Run the Streamlit app:

bash
Copy
streamlit run library_manager.py
Usage
Once the app is running, you will be presented with the following tabs:

📋 All Books: View all books in your library.

➕ Add Book: Add a new book to your library by providing its title, author, year, genre, and read status.

🗑️ Remove Book: Select and remove a book from your library.

🔍 Search: Search for books by title or author.

📊 Statistics: View library statistics such as total books, books read, and genre distribution.

Library Data Storage
The app saves the library data locally in a library.json file, which is automatically loaded when the app is launched. Any changes to the library are saved in this file.

Contributing
Fork the repository.

Create a new branch for your feature or bugfix.

Make your changes and commit them.

Push your changes and submit a pull request.

License
This project is licensed under the MIT License.

=======
