import requests
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
import yaml
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_config(file_path):
    """Loads the YAML configuration file."""
    logging.info(f"Loading configuration from {file_path}")
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

def fetch_epg_data(url):
    """Fetches the EPG data from the specified URL."""
    logging.info(f"Fetching EPG data from {url}")
    response = requests.get(url)
    response.raise_for_status()  # Ensure the request was successful
    return response.content

def parse_epg_data(html_content, selectors):
    """Parses the EPG data from the HTML content using the provided selectors."""
    logging.info("Parsing EPG data from HTML content")
    soup = BeautifulSoup(html_content, "html.parser")
    programs = soup.select(selectors['program_selector'])
    
    if not programs:
        logging.warning("No EPG entries found. Check the CSS selectors in config.yml")

    epg_data = []
    for program in programs:
        time = program.select_one(selectors['time_selector']).get_text(strip=True)
        title = program.select_one(selectors['title_selector']).get_text(strip=True)
        description = program.select_one(selectors['description_selector']).get_text(strip=True)
        epg_data.append({
            'time': time,
            'title': title,
            'description': description
        })
    return epg_data

def generate_epg_xml(epg_data, file_path):
    """Generates an XML file from the EPG data."""
    logging.info(f"Generating EPG XML file at {file_path}")
    root = ET.Element("tv")

    for entry in epg_data:
        program_element = ET.SubElement(root, "programme", start=entry['time'])
        title_element = ET.SubElement(program_element, "title")
        title_element.text = entry['title']
        desc_element = ET.SubElement(program_element, "desc")
        desc_element.text = entry['description']

    tree = ET.ElementTree(root)
    tree.write(file_path, encoding='utf-8', xml_declaration=True)
    logging.info("EPG XML file has been generated successfully")

def main():
    config = load_config('config.yml')
    
    url = config['url']
    selectors = config['parsing']
    output_path = config['output']['file_path']
    
    html_content = fetch_epg_data(url)
    epg_data = parse_epg_data(html_content, selectors)
    
    if epg_data:
        generate_epg_xml(epg_data, output_path)
        logging.info(f"EPG data has been saved to {output_path}")
    else:
        logging.error("No EPG data to save")

if __name__ == "__main__":
    main()
