import requests
import xml.etree.ElementTree as ET

# Define the URL to fetch EPG data
url = "https://api.app.ertflix.gr/v2/Tile/GetTiles"
headers = {
    "Content-Type": "application/json;charset=utf-8",
    "X-Api-Date-Format": "iso",
    "X-Api-Camel-Case": "true"
}

# Send a GET request to the URL
response = requests.get(url, headers=headers)
response.raise_for_status()  # Raise an exception for HTTP errors

# Parse the JSON response
epg_data = response.json()

# Create the root element for the EPG XML
epg_root = ET.Element('tv')

# Iterate over each programme in the JSON data and convert it to XML
for programme in epg_data.get('tiles', []):
    # Extract programme details
    channel = programme.get('channel', 'Unknown Channel')
    start_time = programme.get('startTime')
    stop_time = programme.get('endTime')
    title = programme.get('title')
    description = programme.get('description', '')

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
epg_tree.write('ERTFLIX_EPG.xml', encoding='utf-8', xml_declaration=True)

print("EPG data has been saved to 'ERTFLIX_EPG.xml'.")
