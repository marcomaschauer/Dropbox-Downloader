import os
import requests
import zipfile

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

def extract_filename_from_link(link):
    filename = link.split('/')[-1]
    filename = filename.split('?')[0]
    return filename

def download_from_dropbox(link, base_directory, current, total):
    print(f"\n[{current}/{total}] Downloading {link}...")

    internal_filename = extract_filename_from_link(link)
    zip_filename = f"{internal_filename}.zip"
    zip_path = os.path.join(base_directory, zip_filename)

    zip_path = file_rename_if_exists(zip_path)

    if "?dl=0" in link:
        direct_link = link.replace("?dl=0", "?dl=1")
    else:
        direct_link = link

    response = requests.get(direct_link, stream=True)
    response.raise_for_status()

    # Use force_zip64 by setting allowZip64=True
    with zipfile.ZipFile(zip_path, 'w', allowZip64=True) as zf:
        with zf.open(internal_filename, 'w') as f_in_zip:
            for chunk in response.iter_content(chunk_size=8192):
                f_in_zip.write(chunk)

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

    base_directory = input("Enter the directory to save all ZIP archives: ")
    
    if not is_valid_directory(base_directory):
        print(f"Invalid directory: {base_directory}")
        exit(1)

    total_links = len(links)
    for idx, link in enumerate(links, 1):
        link = link.strip()
        download_from_dropbox(link, base_directory, idx, total_links)
