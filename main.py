import os
import requests
import zipfile

def is_valid_dropbox_link(link):
    # Check if link has correct structure
    if not (link.startswith('https://www.dropbox.com/') or link.startswith('https://dropbox.com/')):
        return False

    # Check if link returns HTTP 200
    try:
        response = requests.head(link, allow_redirects=True)
        return response.status_code == 200
    except requests.RequestException:
        return False

def is_valid_path(path):
    # Check if path ends with .zip
    if not path.endswith(".zip"):
        return False
    # Check for malicious path patterns
    if ".." in path or os.path.isabs(path):
        return False
    # Check if directory exists
    directory = os.path.dirname(path)
    if directory and not os.path.exists(directory):
        return False
    return True

def file_rename_if_exists(path):
    """
    If the file at the given path exists, rename it by appending an incremental number.
    For example, if 'file.zip' exists, try 'file_1.zip', 'file_2.zip', etc.
    Return the path (either original or modified) where the file can be saved without overwriting.
    """
    directory, filename = os.path.split(path)
    base, ext = os.path.splitext(filename)
    counter = 1

    while os.path.exists(path):
        path = os.path.join(directory, f"{base}_{counter}{ext}")
        counter += 1

    return path

def extract_filename_from_link(link):
    """
    Extract the filename from a Dropbox link.
    """
    # Split by '/' and take the last part as the file name
    filename = link.split('/')[-1]
    # Remove any query parameters
    filename = filename.split('?')[0]
    return filename

def download_from_dropbox(link, zip_path, internal_filename):
    # Ensure the link forces download
    if "?dl=0" in link:
        direct_link = link.replace("?dl=0", "?dl=1")
    else:
        direct_link = link

    response = requests.get(direct_link, stream=True)
    response.raise_for_status()

    # Create a ZIP archive and store the content inside it
    with zipfile.ZipFile(zip_path, 'w') as zf:
        with zf.open(internal_filename, 'w') as f_in_zip:
            for chunk in response.iter_content(chunk_size=8192):
                f_in_zip.write(chunk)

    print(f"File from {link} downloaded and saved in ZIP archive: {zip_path}.")

if __name__ == "__main__":
    links = input("Enter the Dropbox links separated by spaces: ").split()

    # Validate Dropbox links
    for link in links:
        link = link.strip()
        if not is_valid_dropbox_link(link):
            print(f"Invalid Dropbox link: {link}")
            exit(1)

    for link in links:
        link = link.strip()
        zip_save_path = input(f"Enter the local save path for ZIP for {link} (e.g., ./archive.zip): ")
        
        # Validate path
        if not is_valid_path(zip_save_path):
            print(f"Invalid path: {zip_save_path}")
            exit(1)

        # Rename file if already exists
        zip_save_path = file_rename_if_exists(zip_save_path)
        
        # Automatically determine the internal file name from the Dropbox link
        internal_name = extract_filename_from_link(link)
        download_from_dropbox(link, zip_save_path, internal_name)
