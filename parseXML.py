import os
import xml.etree.ElementTree as ET
import json

# Define input and output paths
# Add a script to fetch only the file names from concept_refid_list.txt

filenames_list_path = "docs/concept_refid_list.txt"  # File containing filenames 

# Folder containing XML files (you can download this at 
# https://www.omgwiki.org/OMGSysML/doku.php?id=sysml-roadmap:systems_engineering_concept_model_workgroup)

folder_path = "SECM/SECM Version 09-15-2016_files/xml"  


output_json_path = "data.json"  # Path to save the JSON output

# Initialize a list to store the extracted data
output_data = []

# Read the list of filenames
with open(filenames_list_path, "r") as file:
    filenames = [line.strip() for line in file]

# Process each file
for filename in filenames:
    file_path = os.path.join(folder_path, filename + ".xml")  # Assume XML extension
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        continue

    # Parse the XML file
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()

        # Look for the <block> tag
        block = root.find(".//block")
        if block is None:
            print(f"No <block> found in file: {file_path}")
            continue

        # Extract the <name> and <documentation> tags within <block>
        name = block.findtext("name", default="N/A")
        documentation = block.findtext("documentation", default="N/A")

        # Extract <appearsIn> refid attributes and structure them
        appears_in = block.findall(".//appearsIn/diagram")
        appears_in_data = [{
            "name": diagram.attrib.get("name", "N/A"),
            "refid": diagram.attrib.get("refid", "N/A")
        } for diagram in appears_in]

        # Append to output data
        output_data.append({
            "code": filename,
            "name": name,
            "documentation": documentation,
            "appearsIn": appears_in_data
        })

    except ET.ParseError as e:
        print(f"Error parsing file {file_path}: {e}")

# Save to JSON
with open(output_json_path, "w") as json_file:
    json.dump(output_data, json_file, indent=4)

print(f"Data successfully saved to {output_json_path}")