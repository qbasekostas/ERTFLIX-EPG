import requests
from bs4 import BeautifulSoup
import yaml

# Load the configuration from the YAML file
with open('config.yml', 'r') as file:
    config = yaml.safe_load(file)

# Extract the URL and parameters from the configuration
url = config['url']
params = config['params']

# Send a GET request to the search page with the parameters
response = requests.get(url, params=params)
response.raise_for_status()  # Check that the request was successful

# Parse the HTML content of the page
soup = BeautifulSoup(response.content, "html.parser")

# Extract HTML parsing settings from the configuration
epg_entries_selector = config['parsing']['epg_entries_selector']
time_selector = config['parsing']['time_selector']
title_selector = config['parsing']['title_selector']
description_selector = config['parsing']['description_selector']

# Find the EPG entries
epg_entries = soup.select(epg_entries_selector)

# Extract and print the relevant information
for entry in epg_entries:
    time = entry.select_one(time_selector).get_text(strip=True)
    title = entry.select_one(title_selector).get_text(strip=True)
    description = entry.select_one(description_selector).get_text(strip=True)
    print(f"{time} - {title}: {description}")
