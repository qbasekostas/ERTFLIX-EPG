import xml.etree.ElementTree as ET
from datetime import datetime

def convert_to_xmltv_time(epg_time):
    dt = datetime.strptime(epg_time, "%Y%m%d%H%M")
    return dt.strftime("%Y%m%d%H%M%S %z")

# Parse the input XML file
tree = ET.parse('EPG_Input.xml')
root = tree.getroot()

# Create the root element for XMLTV format
xmltv_root = ET.Element('tv')

# Iterate over each programme and convert it to XMLTV format
for programme in root.findall('programme'):
    xmltv_programme = ET.SubElement(xmltv_root, 'programme')
    xmltv_programme.set('start', convert_to_xmltv_time(programme.get('start')))
    xmltv_programme.set('stop', convert_to_xmltv_time(programme.get('stop')))
    xmltv_programme.set('channel', programme.get('channel'))

    # Add title element
    title = programme.find('title')
    xmltv_title = ET.SubElement(xmltv_programme, 'title', lang=title.get('lang'))
    xmltv_title.text = title.text

    # Add description element
    desc = programme.find('desc')
    xmltv_desc = ET.SubElement(xmltv_programme, 'desc', lang=desc.get('lang'))
    xmltv_desc.text = desc.text
    
    # Add length element
    length = programme.find('length')
    xmltv_length = ET.SubElement(xmltv_programme, 'length', units=length.get('units'))
    xmltv_length.text = length.text

    # Add rating element
    rating = programme.find('rating')
    xmltv_rating = ET.SubElement(xmltv_programme, 'rating')
    rating_value = rating.find('value')
    xmltv_rating_value = ET.SubElement(xmltv_rating, 'value')
    xmltv_rating_value.text = rating_value.text

    # Add category element
    category = programme.find('category')
    xmltv_category = ET.SubElement(xmltv_programme, 'category', lang=category.get('lang'))
    xmltv_category.text = category.text

# Convert the tree to a string and save it
xmltv_tree = ET.ElementTree(xmltv_root)
xmltv_tree.write('EPG_XMLTV.xml', encoding='utf-8', xml_declaration=True)

print("Conversion complete. The XMLTV data has been saved to 'EPG_XMLTV.xml'.")
