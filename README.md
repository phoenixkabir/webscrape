# Web Scraping Project

This project is a web scraper that fetches content from specified URLs and saves the extracted data in separate folders. The script extracts text, headings, images, and URLs from the webpages and organizes them into distinct files. Each folder is named based on the URL and added to the `.gitignore` file to prevent it from being tracked by Git.

## Features

- Fetches and parses HTML content from given URLs.
- Extracts text, headings, images, and URLs from the webpage.
- Saves extracted content into separate files:
  - `content.txt` for text.
  - `headings.txt` for headings.
  - `urls.txt` for URLs with their anchor text.
  - Images are saved in an `images` folder.
- Adds the folder names to `.gitignore` to avoid tracking by Git.

## Requirements

- Python 3.6 or higher
- `requests` library
- `beautifulsoup4` library

## Installation

1. Clone the repository:

    ```sh
    git clone https://github.com/your-username/web-scraping-project.git
    cd web-scraping-project
    ```

2. Create and activate a virtual environment (optional but recommended):

    ```sh
    python3 -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required libraries:

    ```sh
    pip install requests beautifulsoup4
    ```

## Usage

1. Update the list of URLs in the `main` function of `web_scraper.py`:

    ```python
    def main():
        urls = [
            'https://en.wikipedia.org/wiki/Node.js',
            'https://en.wikipedia.org/wiki/Chess'
            # Add more URLs here
        ]
        ...
    ```

2. Run the script:

    ```sh
    python3 web_scraper.py
    ```

3. The content will be saved in folders named based on the URL paths, and these folder names will be added to `.gitignore`.


