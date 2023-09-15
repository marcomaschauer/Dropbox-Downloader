import os
import requests
from bs4 import BeautifulSoup

def is_valid_dropbox_link(link):
    if not (link.startswith('https://www.dropbox.com/') or link.startswith('https://dropbox.com/')):
        return False

    try:
        response = requests.head(link, allow_redirects=True)
        return response.status_code == 200
    except requests.RequestException:
        return False

def is_valid_directory(directory):
    return os.path.exists(directory) and os.path.isdir(directory)

def file_rename_if_exists(path):
    directory, filename = os.path.split(path)
    base, ext = os.path.splitext(filename)
    counter = 1

    while os.path.exists(path):
        path = os.path.join(directory, f"{base}_{counter}{ext}")
        counter += 1

    return path

def fetch_website_title(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'lxml')
        title = soup.title.string.strip()
        # Removing "Dropbox - " prefix if it exists
        return title.replace("Dropbox - ", "")
    except:
        return None

def download_from_dropbox(link, base_directory, current, total):
    print(f"\n[{current}/{total}] Downloading {link}...")

    website_title = fetch_website_title(link)
    if website_title:
        filename = f"{website_title}.zip"
    else:
        filename = f"download_{current}.zip"  # Default naming if title can't be fetched

    file_path = os.path.join(base_directory, filename)
    file_path = file_rename_if_exists(file_path)

    if "?dl=0" in link:
        direct_link = link.replace("?dl=0", "?dl=1")
    else:
        direct_link = link

    response = requests.get(direct_link, stream=True)
    response.raise_for_status()

    with open(file_path, 'wb') as f_out:
        for chunk in response.iter_content(chunk_size=8192):
            f_out.write(chunk)

    # Print progress bar
    progress = int((current / total) * 50)
    bar = ['=' * progress, ' ' * (50 - progress)]
    print(f"[{bar[0]}{bar[1]}] {current}/{total} downloads complete.")

if __name__ == "__main__":
    links = input("Enter the Dropbox links separated by spaces: ").split()

    for link in links:
        link = link.strip()
        if not is_valid_dropbox_link(link):
            print(f"Invalid Dropbox link: {link}")
            exit(1)

    base_directory = input("Enter the directory to save all files: ")
    
    if not is_valid_directory(base_directory):
        print(f"Invalid directory: {base_directory}")
        exit(1)

    total_links = len(links)
    for idx, link in enumerate(links, 1):
        link = link.strip()
        download_from_dropbox(link, base_directory, idx, total_links)
