# this file generates the concepts_list_names.txt file in this directory

import json

def extract_and_format_name_codes(json_file, output_file):
    try:
        # Load the JSON file
        with open(json_file, 'r') as file:
            data = json.load(file)
        
        # Collect all name-code pairs
        name_code_pairs = []
        for item in data:
            if isinstance(item, dict):
                name = item.get("name", "Unnamed")
                code = item.get("code", "No Code")
                name_code_pairs.append((name, code))
        
        # Calculate the maximum width of the names for alignment
        max_name_length = max(len(name) for name, _ in name_code_pairs)
        
        # Write the formatted output to the file
        with open(output_file, 'w') as file:
            for name, code in sorted(name_code_pairs):
                file.write(f"{name.ljust(max_name_length)} : {code}\n")
        
        print(f"Extracted {len(name_code_pairs)} name-code pairs to {output_file}.")
    
    except Exception as e:
        print(f"An error occurred: {e}")

# Usage
json_file = "data.json"
output_file = "concepts_list_names.txt"
extract_and_format_name_codes(json_file, output_file)