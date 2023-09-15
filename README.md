# Dropbox Downloader

This Python script allows you to download multiple files from Dropbox by providing their shared links. Instead of you specifying the filenames, the script will automatically use the webpage's title from each Dropbox link as the filename for the downloaded content. Each file will be saved with a `.zip` extension in the specified directory.

## Prerequisites

- Python 3
- `requests` module: Install it using `pip install requests`.
- `beautifulsoup4` and `lxml`: Install them using `pip install beautifulsoup4 lxml`.

## How to Use

1. Run the script using:
   ```bash
   python dropbox_downloader.py
   ```

2. When prompted, enter the Dropbox shared links separated by spaces:
   ```
   Enter the Dropbox links separated by spaces: <YOUR_DROPBOX_LINK_1> <YOUR_DROPBOX_LINK_2> ...
   ```

3. Next, specify the directory where you'd like to save the files:
   ```
   Enter the directory to save all files: <YOUR_DIRECTORY_PATH>
   ```

4. The script will start processing each link. It will fetch the title of the webpage associated with the link and use it as the filename for the downloaded content. The content will then be saved with a `.zip` extension in the specified directory.

5. Watch the progress bar and messages to keep track of the download process.

## Features

- **Link Validation**: Before downloading, the script checks if the provided links are valid Dropbox links and are accessible.
- **Directory Validation**: The script verifies if the provided directory path is valid.
- **Auto Naming**: The script fetches the webpage's title from the Dropbox link and uses it as the filename.
- **Auto-renaming**: If a file with the same name already exists in the directory, the script will automatically rename the new file to avoid overwriting.
- **Progress Indicators**: The script provides a progress bar and messages to inform you about the download status and completion.

---