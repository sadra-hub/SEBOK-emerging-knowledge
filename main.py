import diagrams.parseDiagram as parseDiagram
import articles.parseArticle as parseArticle

# Load the image
image_path = "data/SECM/SECM Version 09-15-2016_files/_18_1_3b70190_1461072592807_927839_93477.jpg"

# Load the XML diagram
diagram_xml_file = "data/SECM/SECM Version 09-15-2016_files/xml/_18_1_3b70190_1461072592807_927839_93477.xml"

# Load the article
pdf_directory = "articles/documents"  # Directory containing PDF files

# Load the data
json_path = "data/data.json"  # Path to JSON file

# Define the square size (resolution of the heatmap)
square_size = 5

point_interval = 5

triangle_delta = 10

gradient_width = 30

# The percentage of each rectangle to be covered [0 - 0.99]
rectangle_coverage = 0.9

transparency = 120

# Process the PDFs and get the sorted results which are refid of rectangles in XML
rect_refid_list, sorted_concept_refid_score = parseArticle.processPDF(pdf_directory, json_path)

# Process the diagram according to result of processing PDF(s)
image = parseDiagram.processDiagram(
    image_path, 
    diagram_xml_file, 
    rect_refid_list, 
    sorted_concept_refid_score,
    square_size, 
    point_interval,
    triangle_delta,
    gradient_width,
    rectangle_coverage,
    transparency
)

# Save the colored image with transparency to a new file
image.save(
    "diagrams/images/outputDiagram.png"
)  # Save as PNG to preserve transparency