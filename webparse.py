import os
import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urlparse

def fetch_webpage(url: str) -> str:
    try:
        response = requests.get(url)
        response.raise_for_status() 
        return response.text
    except requests.RequestException as e:
        print(f"Error fetching the webpage {url}: {e}")
        return ""

def extract_content(html: str):
    soup = BeautifulSoup(html, 'html.parser')

    text = ' '.join([t.get_text(strip=True) for t in soup.find_all(text=True)])
    headings = ' '.join([h.get_text(strip=True) for h in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])])
    images = [img['src'] for img in soup.find_all('img', src=True)]
    urls = [(a['href'], a.get_text(strip=True)) for a in soup.find_all('a', href=True)]

    return {'text': text, 'headings': headings, 'images': images, 'urls': urls}

def ensure_absolute_url(base: str, relative_url: str) -> str:
    if relative_url.startswith('//'):
        return f"https:{relative_url}"
    elif not relative_url.startswith('http'):
        return os.path.join(base, relative_url)
    return relative_url

def save_content(content: dict, base_url: str, folder_name: str):
    os.makedirs(folder_name, exist_ok=True)
    text_path = os.path.join(folder_name, 'content.txt')
    headings_path = os.path.join(folder_name, 'headings.txt')
    urls_path = os.path.join(folder_name, 'urls.txt')
    images_dir = os.path.join(folder_name, 'images')
    os.makedirs(images_dir, exist_ok=True)

    with open(text_path, 'w', encoding='utf-8') as f:
        f.write(content['text'])

    with open(headings_path, 'w', encoding='utf-8') as f:
        f.write(content['headings'])

    with open(urls_path, 'w', encoding='utf-8') as f:
        for url, text in content['urls']:
            f.write(f"{text}: {ensure_absolute_url(base_url, url)}\n")

    for index, img_src in enumerate(content['images']):
        img_url = ensure_absolute_url(base_url, img_src)
        img_ext = os.path.splitext(img_url)[1]
        img_path = os.path.join(images_dir, f'image{index}{img_ext}')
        try:
            img_data = requests.get(img_url).content
            with open(img_path, 'wb') as img_file:
                img_file.write(img_data)
        except requests.RequestException as e:
            print(f"Error saving image {img_url}: {e}")

def sanitize_folder_name(name: str) -> str:
    return re.sub(r'[^\w\-]', '_', name)

def add_to_gitignore(folder_name: str):
    gitignore_path = os.path.join(os.path.dirname(__file__), '.gitignore')
    folder_path = f"/{folder_name}"
    with open(gitignore_path, 'a') as gitignore_file:
        gitignore_file.write(f"\n{folder_path}")

def main():
    urls = [
        'https://en.wikipedia.org/wiki/Node.js',
        'https://en.wikipedia.org/wiki/Chess',
        'https://en.wikipedia.org/wiki/Python_(programming_language)'
        # Add more URLs here
    ]

    for url in urls:
        print(f"Processing URL: {url}")
        html = fetch_webpage(url)
        if html:
            content = extract_content(html)
            parsed_url = urlparse(url)
            folder_name = sanitize_folder_name(parsed_url.netloc + parsed_url.path)
            save_content(content, url, folder_name)
            add_to_gitignore(folder_name)
            print(f"Content saved in folder: {folder_name}")

if __name__ == "__main__":
    main()
