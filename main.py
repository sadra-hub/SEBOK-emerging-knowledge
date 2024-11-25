import json
import pdfplumber
from collections import defaultdict

# Load the JSON file
with open("data.json", "r", encoding="utf-8") as file:
    json_data = json.load(file)

# Load the PDF file
pdf_path = "document.pdf"

# Initialize dictionaries for scores and name appearances
refid_scores = defaultdict(int)
name_counts = defaultdict(int)

# Extract text from the PDF
with pdfplumber.open(pdf_path) as pdf:
    pdf_text = " ".join(page.extract_text() for page in pdf.pages)

# Search for names and update scores for their corresponding refIDs
for item in json_data:
    name = item["name"]
    appears_in = item["appearsIn"]

    # Count occurrences of the name in the PDF text
    name_occurrences = pdf_text.count(name)
    if name_occurrences > 0:
        # Record the name count
        name_counts[name] += name_occurrences

        # Increment scores for all refIDs in appearsIn based on occurrences
        for ref in appears_in:
            refid_scores[ref["refid"]] += name_occurrences

# Sort names and refIDs by counts in descending order
sorted_names = sorted(name_counts.items(), key=lambda x: x[1], reverse=True)
sorted_refids = sorted(refid_scores.items(), key=lambda x: x[1], reverse=True)

# Output results
print("Matched Names and Their Counts:")
for name, count in sorted_names:
    print(f"{name}: {count}")

print("\nRefID Scores:")
for refid, score in sorted_refids:
    print(f"{refid}: {score}")