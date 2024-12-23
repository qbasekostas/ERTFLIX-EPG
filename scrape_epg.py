import requests
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET

# Define the URL to scrape
url = "https://www.ertflix.gr/epg/channel/ert-christmas"

# Send a GET request to the URL
response = requests.get(url)
response.raise_for_status()  # Raise an exception for HTTP errors

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(response.content, 'html.parser')

# Create the root element for the EPG XML
epg_root = ET.Element('tv')

# Find the relevant elements containing the program information
program_elements = soup.find_all('div', class_='epg-item')

for program in program_elements:
    # Extract program details
    channel = "ERT Christmas"  # Static channel name
    start_time = program.find('time', class_='epg-start')['datetime']
    stop_time = program.find('time', class_='epg-end')['datetime']
    title = program.find('h3', class_='epg-title').text.strip()
    description = program.find('p', class_='epg-description').text.strip() if program.find('p', class_='epg-description') else ""

    # Create the programme element
    epg_programme = ET.SubElement(epg_root, 'programme')
    epg_programme.set('channel', channel)
    epg_programme.set('start', start_time)
    epg_programme.set('stop', stop_time)

    # Add title element
    epg_title = ET.SubElement(epg_programme, 'title')
    epg_title.text = title

    # Add description element
    epg_desc = ET.SubElement(epg_programme, 'desc')
    epg_desc.text = description

# Convert the tree to a string and save it
epg_tree = ET.ElementTree(epg_root)
epg_tree.write('EPG_Input.xml', encoding='utf-8', xml_declaration=True)

print("EPG data has been saved to 'EPG_Input.xml'.")
