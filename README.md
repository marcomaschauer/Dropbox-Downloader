# Dropbox Downloader

This Python script allows you to download multiple files from Dropbox by providing their shared links. It saves each file as a ZIP archive in a specified directory. The script provides progress updates as it processes each link.

## Prerequisites

- Python 3
- `requests` module: Install it using `pip install requests` if you haven't already.

## How to Use

1. Run the script using:
   ```bash
   python dropbox_downloader.py
   ```

2. When prompted, enter the Dropbox shared links separated by spaces:
   ```
   Enter the Dropbox links separated by spaces: <YOUR_DROPBOX_LINK_1> <YOUR_DROPBOX_LINK_2> ...
   ```

3. Next, specify the directory where you'd like to save the ZIP archives:
   ```
   Enter the directory to save all ZIP archives: <YOUR_DIRECTORY_PATH>
   ```

4. The script will start processing each link, downloading the content, and saving it as a ZIP archive in the specified directory.

5. Watch the progress bar and messages to keep track of the download process.

## Features

- **Link Validation**: Before downloading, the script checks if the provided links are valid Dropbox links and are accessible.
- **Directory Validation**: The script verifies if the provided directory path is valid.
- **Auto-renaming**: If a ZIP archive with the same name already exists in the directory, the script will automatically rename the new archive to avoid overwriting.
- **Progress Indicators**: The script provides a progress bar and messages to inform you about the download status and completion.

---

