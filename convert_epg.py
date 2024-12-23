import xml.etree.ElementTree as ET
from datetime import datetime

# Function to convert to Unix time
def convert_to_unix_time(epg_time):
    dt = datetime.strptime(epg_time, "%Y%m%d%H%M%S")
    return int(dt.timestamp())

# Function to create Enigma2 EPG XML
def create_enigma2_epg(programme):
    e2event = ET.Element('e2event')

    # Extract relevant information
    start_time = convert_to_unix_time(programme.get('start'))
    stop_time = convert_to_unix_time(programme.get('stop'))
    duration = stop_time - start_time
    title = programme.find('title').text
    desc = programme.find('desc').text
    channel = programme.get('channel')

    # Create Enigma2 EPG elements
    ET.SubElement(e2event, 'e2eventid').text = str(hash(title + str(start_time)))
    ET.SubElement(e2event, 'e2eventstart').text = str(start_time)
    ET.SubElement(e2event, 'e2eventduration').text = str(duration)
    ET.SubElement(e2event, 'e2eventtitle').text = title
    ET.SubElement(e2event, 'e2eventdescription').text = desc
    ET.SubElement(e2event, 'e2eventdescriptionextended').text = desc
    ET.SubElement(e2event, 'e2eventservicename').text = channel
    ET.SubElement(e2event, 'e2eventservicereference').text = "1:0:1:0:0:0:0:0:0:0:"

    return e2event

# Parse the input XML file
tree = ET.parse('EPG_Input.xml')
root = tree.getroot()

# Create the root element for Enigma2 EPG format
enigma2_root = ET.Element('e2eventlist')

# Iterate over each programme and convert it to Enigma2 format
for programme in root.findall('programme'):
    e2event = create_enigma2_epg(programme)
    enigma2_root.append(e2event)

# Convert the tree to a string and save it
enigma2_tree = ET.ElementTree(enigma2_root)
enigma2_tree.write('EPG_Enigma2.xml', encoding='utf-8', xml_declaration=True)

print("Conversion complete. The Enigma2 EPG data has been saved to 'EPG_Enigma2.xml'.")
