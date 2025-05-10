# txt_json_data_extraction

A simple utility to download JSON or TXT files from URLs.

## Requirements

- Python 3
- requests library

Install the required packages:
```
pip install requests
```

## Usage

### Interactive Mode
Run the script:
```
python3 grabData.py
```

The script will prompt you to enter a URL. You can copy and paste URLs that begin with '@' as the script will handle removing this character.

### Batch Mode
To process all URLs from a data.txt file:
```
python3 grabData.py -all
```

This will read the data.txt file in the same directory, extract all URLs, and download each file.

## Features

- Automatically detects if the downloaded file is JSON or TXT
- Names the file based on the original URL and adds a timestamp
- Stores files in the 'output' folder
- Returns the filename after downloading
- Batch processing with the -all parameter 