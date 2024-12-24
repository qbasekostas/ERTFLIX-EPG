import requests
from bs4 import BeautifulSoup
import yaml

def load_config(file_path):
    """Loads the YAML configuration file."""
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

def fetch_epg_data(url, params):
    """Fetches the EPG data from the specified URL with the given parameters."""
    response = requests.get(url, params=params)
    response.raise_for_status()  # Ensure the request was successful
    return response.content

def parse_epg_data(html_content, selectors):
    """Parses the EPG data from the HTML content using the provided selectors."""
    soup = BeautifulSoup(html_content, "html.parser")
    epg_entries = soup.select(selectors['epg_entries_selector'])
    
    epg_data = []
    for entry in epg_entries:
        time = entry.select_one(selectors['time_selector']).get_text(strip=True)
        title = entry.select_one(selectors['title_selector']).get_text(strip=True)
        description = entry.select_one(selectors['description_selector']).get_text(strip=True)
        epg_data.append({
            'time': time,
            'title': title,
            'description': description
        })
    return epg_data

def save_epg_data(epg_data, file_path):
    """Saves the EPG data to a text file."""
    with open(file_path, 'w') as file:
        for entry in epg_data:
            file.write(f"{entry['time']} - {entry['title']}: {entry['description']}\n")

def main():
    config = load_config('config.yml')
    
    url = config['url']
    params = config['params']
    selectors = config['parsing']
    
    html_content = fetch_epg_data(url, params)
    epg_data = parse_epg_data(html_content, selectors)
    
    save_epg_data(epg_data, 'result.txt')
    print("EPG data has been saved to result.txt")

if __name__ == "__main__":
    main()
