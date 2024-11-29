import xml.etree.ElementTree as ET


def get_shapes(rect_refid_list, diagram_xml_file):
    """
    Extracts the x, y coordinates of rectangle shapes and any polygons connecting them
    from the given XML file.
    
    :param rect_refid_list: List of refid values for the rectangle shapes.
    :param diagram_xml_file: Path to the XML file containing diagram data.
    :return: A dictionary where keys are refids, and values are lists of 4 (x, y) coordinate tuples
             for rectangles and connecting polygons.
    """
    # Parse the XML file
    tree = ET.parse(diagram_xml_file)
    root = tree.getroot()
    
    # Namespace check (if XML uses namespaces, update as needed)
    namespace = ''
    if root.tag.startswith('{'):
        namespace = root.tag.split('}')[0] + '}'

    # Navigate to the "map" element within "diagram" and "magicdraw"
    magicdraw = root.find(f"{namespace}magicdraw")
    if magicdraw is None:
        raise ValueError("Invalid XML structure: 'magicdraw' tag not found.")
    
    diagram = magicdraw.find(f"{namespace}diagram")
    if diagram is None:
        raise ValueError("Invalid XML structure: 'diagram' tag not found.")
    
    map_element = diagram.find(f"{namespace}map")
    if map_element is None:
        raise ValueError("Invalid XML structure: 'map' tag not found.")
    
    # Dictionary to store coordinates of rectangles and polygons
    refId_coordinates = {}

    # Extract rectangles and polygons from "area" elements
    areas = map_element.findall(f"{namespace}area")
    
    # Step 1: Identify rectangle shapes and store their coordinates
    for area in areas:
        refid = area.get("refid")
        shape = area.get("shape")
        
        if refid in rect_refid_list and shape == "rect":
            points = [
                (int(point.get("x")), int(point.get("y")))
                for point in area.findall(f"{namespace}point")
            ]
            refId_coordinates[refid] = points

    # Step 2: Check for polygons that connect rectangles
    for area in areas:
        refid = area.get("refid")
        shape = area.get("shape")
        
        if shape == "poly":
            points = [
                (int(point.get("x")), int(point.get("y")))
                for point in area.findall(f"{namespace}point")
            ]
            # Check if this polygon connects rectangles in rect_refid_list
            connected_rects = [
                rect_refid for rect_refid in rect_refid_list if rect_refid in refId_coordinates
            ]
            if len(connected_rects) > 1:  # If more than two rectangles are connected
                refId_coordinates[refid] = points

    return refId_coordinates


# Function to get the score for each square (to be defined by you later)
def get_score(x, y, refid_list):
    # Placeholder for your actual scoring function
    return x + y