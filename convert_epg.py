import xml.etree.ElementTree as ET
from datetime import datetime
import gzip

def convert_time_format(time_str):
    # Convert time format from "YYYYMMDDHHMM" to "YYYYMMDDHHMM +0200"
    dt = datetime.strptime(time_str, "%Y%m%d%H%M")
    return dt.strftime("%Y%m%d%H%M") + " +0200"

def indent(elem, level=0):
    i = "\n" + level * "  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for subelem in elem:
            indent(subelem, level + 1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i

def convert_epg(input_file, output_file):
    tree = ET.parse(input_file)
    root = tree.getroot()

    new_root = ET.Element("tv")

    # Add the <channel> element
    channel_element = ET.SubElement(new_root, "channel", id="ERTChristmas")
    display_name_element = ET.SubElement(channel_element, "display-name")
    display_name_element.text = "ERT CHRISTMAS"

    for programme in root.findall('programme'):
        start = convert_time_format(programme.get('start'))
        stop = convert_time_format(programme.get('stop'))
        channel = programme.get('channel')

        new_programme = ET.SubElement(new_root, "programme", start=start, stop=stop, channel=channel)

        title = programme.find('title')
        if title is not None:
            title_element = ET.SubElement(new_programme, "title", lang="el")
            title_element.text = title.text

        desc = programme.find('desc')
        if desc is not None:
            desc_element = ET.SubElement(new_programme, "desc", lang="el")
            desc_element.text = desc.text

    indent(new_root)  # Indent the XML tree for pretty printing
    new_tree = ET.ElementTree(new_root)

    # Write to a gzip file
    with gzip.open(output_file, 'wb') as f:
        new_tree.write(f, encoding='utf-8', xml_declaration=True)

if __name__ == "__main__":
    input_file = "ERT_Christmas_EPG.xml"
    output_file = "converted_EPG.xml.gz"
    convert_epg(input_file, output_file)
