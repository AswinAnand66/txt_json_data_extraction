#!/usr/bin/env python3

import os
import sys
import warnings
import re

# Suppress the urllib3 warning about LibreSSL compatibility
warnings.filterwarnings("ignore", category=Warning, message=".*OpenSSL.*LibreSSL.*")

import requests
import json
from urllib.parse import urlparse
from datetime import datetime

def grab_data(url):
    # Remove '@' from the beginning of the URL if present
    if url.startswith('@'):
        url = url[1:]
    
    # Create output directory if it doesn't exist
    output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")
    os.makedirs(output_dir, exist_ok=True)
    
    try:
        # Get the file from the URL
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception if request failed
        
        # Try to detect content type
        content_type = response.headers.get('Content-Type', '')
        
        # Try to determine file type
        if 'json' in content_type or is_json(response.text):
            file_ext = '.json'
        else:
            file_ext = '.txt'
        
        # Generate filename using timestamp and parsed URL
        parsed_url = urlparse(url)
        base_name = os.path.basename(parsed_url.path) or 'download'
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Remove existing extension if any
        base_name = os.path.splitext(base_name)[0]
        
        # Create the filename
        filename = f"{base_name}_{timestamp}{file_ext}"
        file_path = os.path.join(output_dir, filename)
        
        # Write to file
        with open(file_path, 'wb') as f:
            f.write(response.content)
        
        print(f"File saved as: {filename}")
        return filename
    
    except requests.exceptions.RequestException as e:
        print(f"Error downloading file: {e}")
        return None

def is_json(text):
    """Check if the text is valid JSON"""
    try:
        json.loads(text)
        return True
    except ValueError:
        return False

def extract_urls_from_file(file_path):
    """Extract URLs from a text file"""
    urls = []
    try:
        with open(file_path, 'r') as f:
            content = f.read()
            # Match URLs starting with http:// or https://
            url_pattern = r'https?://[^\s)"]+'
            urls = re.findall(url_pattern, content)
        return urls
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return []

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "-all":
        # Process all URLs from data.txt
        current_dir = os.path.dirname(os.path.abspath(__file__))
        data_file = os.path.join(current_dir, "data.txt")
        
        if not os.path.exists(data_file):
            print(f"Error: data.txt file not found in {current_dir}")
            sys.exit(1)
        
        urls = extract_urls_from_file(data_file)
        
        if not urls:
            print("No URLs found in data.txt")
            sys.exit(1)
        
        print(f"Found {len(urls)} URLs in data.txt")
        for i, url in enumerate(urls):
            print(f"\nProcessing URL {i+1}/{len(urls)}: {url}")
            grab_data(url)
    else:
        # Interactive mode - ask for URL
        url = input("Enter URL to download: ")
        grab_data(url) 