import math
from PIL import Image
import xml.etree.ElementTree as ET

def get_shapes(rect_refid_list, sorted_concept_refid_score, diagram_xml_file):
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
    magicdraw = tree.getroot()

    # Namespace check (if XML uses namespaces, update as needed)
    namespace = ""
    if magicdraw.tag.startswith("{"):
        namespace = magicdraw.tag.split("}")[0] + "}"

    # Navigate to the "map" element within "diagram" and "magicdraw"
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

            # Identify rectangles connected to this polygon
            connected_rects = []
            for rect_refid, rect_points in refId_coordinates.items():
                # Calculate bounding box of the rectangle
                rect_min_x = min(p[0] for p in rect_points)
                rect_max_x = max(p[0] for p in rect_points)
                rect_min_y = min(p[1] for p in rect_points)
                rect_max_y = max(p[1] for p in rect_points)

                # Check if any polygon point is inside the rectangle's bounding box
                for px, py in points:
                    if rect_min_x <= px <= rect_max_x and rect_min_y <= py <= rect_max_y:
                        connected_rects.append(rect_refid)
                        break

            # If this polygon connects more than one rectangle, add it
            if len(connected_rects) > 1:
                refId_coordinates[refid] = points
                score = 0
                for rect_refid in connected_rects:
                    score += sorted_concept_refid_score[rect_refid]
                
                #score of a poly is avarage of connecting rect
                sorted_concept_refid_score[refid] = score/len(connected_rects)  
                
                
    return refId_coordinates
