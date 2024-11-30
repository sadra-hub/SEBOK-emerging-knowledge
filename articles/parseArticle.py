import os
import json
import pdfplumber
from collections import defaultdict

def processPDF(pdf_directory, json_path):
    """
    Processes all PDF files in the specified directory and a JSON file to calculate scores for refIDs based on the occurrence of names
    in the PDF documents. The function returns the sorted list of refIDs with their associated names and counts.

    :param pdf_directory: Directory containing the PDF files.
    :param json_path: Path to the JSON file containing name and refID data.
    :return: A tuple containing:
        - A sorted list of refIDs.
        - A dictionary of refIDs with their scores.
    """
    
    # Load the JSON file
    with open(json_path, "r", encoding="utf-8") as file:
        json_data = json.load(file)

    # Initialize dictionaries for scores and name appearances
    concept_refid_counts = defaultdict(int)
    diagram_refid_counts = defaultdict(int)

    # Initialize a dictionary to store the code (refid) associated with names
    name_to_refid = {}

    # List all PDF files in the directory
    pdf_files = [f for f in os.listdir(pdf_directory) if f.endswith('.pdf')]
    
    # Process each PDF file in the directory
    for pdf_file in pdf_files:
        pdf_path = os.path.join(pdf_directory, pdf_file)  # Full path to the PDF file

        # Extract text from the PDF
        with pdfplumber.open(pdf_path) as pdf:
            pdf_text = " ".join(page.extract_text() for page in pdf.pages)

        # Search for names and update scores for their corresponding refIDs
        for item in json_data:
            name = item["name"]
            code = item["code"]
            appears_in = item["appearsIn"]

            # Map the name to its code (refid)
            name_to_refid[name] = code

            # Count occurrences of the name in the PDF text
            name_occurrences = pdf_text.count(name)
            if name_occurrences > 0:
                # Record the name count
                concept_refid_counts[name] += name_occurrences

                # Increment scores for all refIDs in appearsIn based on occurrences
                for ref in appears_in:
                    diagram_refid_counts[ref["refid"]] += name_occurrences

    # Sort names and refIDs by counts in descending order
    sorted_concept_refid = sorted(concept_refid_counts.items(), key=lambda x: x[1], reverse=True)
    
    # This can be later used to draw heatmap for multiple diagrams but for now we manaully choose 
    # which diagram to use
    # sorted_diagram_refid = sorted(diagram_refid_counts.items(), key=lambda x: x[1], reverse=True)
  
    # Create sorted_concept_refid_score as a dictionary with refID as key and score as value
    sorted_concept_refid_score = {
        name_to_refid[name]: count for name, count in sorted_concept_refid
    }
    
    sorted_concept_refid = [
        (name_to_refid[name], count) for name, count in sorted_concept_refid
    ]

    # Create sorted_concept_refid with only refIDs
    sorted_concept_refid = [item[0] for item in sorted_concept_refid]

    # Return the results as sorted lists
    return sorted_concept_refid, sorted_concept_refid_score