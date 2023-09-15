import requests

def download_from_dropbox(link, destination):
    """
    Download a file from Dropbox via link.

    Args:
    - link (str): Dropbox shared link.
    - destination (str): Local path where the file should be saved.
    """
    # Ensure the link forces download
    if "?dl=0" in link:
        direct_link = link.replace("?dl=0", "?dl=1")
    else:
        direct_link = link

    response = requests.get(direct_link, stream=True)

    # Check if the download was successful
    response.raise_for_status()

    with open(destination, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)

    print(f"File downloaded to {destination}.")

if __name__ == "__main__":
    dropbox_link = input("Enter the Dropbox link: ")
    save_path = input("Enter the local save path (e.g., ./downloaded_file.txt): ")
    download_from_dropbox(dropbox_link, save_path)
