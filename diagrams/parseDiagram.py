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

def get_center(refId_coordinates, diagram_xml_file, rectangle_coverage, point_interval=10, triangle_delta=20):
    """
    Calculate the center of rectangles and points along polygons based on their refId_coordinates.

    :param refId_coordinates: A dictionary of refid: [(x1, y1), (x2, y2), ...].
    :param diagram_xml_file: Path to the XML file containing shape metadata.
    :param point_interval: Distance in pixels between points for polygons.
    :return: A dictionary of refid to center point(s).
    """
    # Parse the XML file
    tree = ET.parse(diagram_xml_file)
    magicdraw = tree.getroot()

    # Namespace check (if XML uses namespaces, update as needed)
    namespace = ""
    if magicdraw.tag.startswith("{"):
        namespace = magicdraw.tag.split("}")[0] + "}"

    # Navigate to the "map" element within "diagram" and "magicdraw"
    diagram = magicdraw.find(f"{namespace}diagram")
    map_element = diagram.find(f"{namespace}map")

    # Dictionary to store the calculated center points or polygon points
    center_coordinates = {}

    # Iterate through the refId_coordinates
    for refid, coordinates in refId_coordinates.items():
        # Find the shape type in the XML
        area = map_element.find(f"{namespace}area[@refid='{refid}']")
        shape = area.get("shape") if area is not None else None

        if shape == "rect" and len(coordinates) == 4:
            # For rectangle, calculate the bounds of the rectangle
            x_coords = [point[0] for point in coordinates]
            y_coords = [point[1] for point in coordinates]

            x_min = min(x_coords)
            x_max = max(x_coords)
            y_min = min(y_coords)
            y_max = max(y_coords)

            # Calculate the dimensions of the oval
            width = (x_max - x_min) * rectangle_coverage
            height = (y_max - y_min) * rectangle_coverage
            center_x = (x_min + x_max) / 2
            center_y = (y_min + y_max) / 2
            radius_x = width / 2
            radius_y = height / 2

            # Generate points covering the inside of the oval
            points = []
            for dx in range(-int(radius_x), int(radius_x) + 1, point_interval):
                for dy in range(-int(radius_y), int(radius_y) + 1, point_interval):
                    # Check if the point (center_x + dx, center_y + dy) lies inside the oval
                    if (dx / radius_x) ** 2 + (dy / radius_y) ** 2 <= 1:
                        x = int(center_x + dx)
                        y = int(center_y + dy)
                        points.append((x, y))
                    
            center_coordinates[refid] = points
            
        elif shape == "poly":
            # Generate points along the polygon line and add delta-shaped triangles at both ends
            polygon_points = []
            for i in range(len(coordinates)):
                x1, y1 = coordinates[i]
                x2, y2 = coordinates[(i + 1) % len(coordinates)]  # Connect the last point to the first
                distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
                num_points = max(1, int(distance // point_interval))

                for j in range(num_points):
                    t = j / num_points
                    px = x1 + t * (x2 - x1)
                    py = y1 + t * (y2 - y1)
                    polygon_points.append((px, py))
            
            if len(coordinates) == 4:
                start_x, start_y = coordinates[0]  # First point
                end_x, end_y = coordinates[1]  # Last point

                # Horizontal end (triangle extending vertically from the end)
                if abs(end_x - start_x) > abs(end_y - start_y):
                    # Triangle extends vertically from the horizontal end
                    delta_vertical = []
                    for dx in range(-triangle_delta, triangle_delta + 1, point_interval):
                        for dy in range(-triangle_delta, triangle_delta + 1, point_interval):
                            if abs(dx) <= (triangle_delta - dy):  # Inside triangular region
                                delta_vertical.append((end_x + dx, end_y + dy))
                    polygon_points += delta_vertical

                # Vertical end (triangle extending horizontally from the end)
                if abs(end_y - start_y) > abs(end_x - start_x):
                    # Triangle extends horizontally from the vertical end
                    delta_horizontal = []
                    for dy in range(-triangle_delta, triangle_delta + 1, point_interval):
                        for dx in range(-triangle_delta, triangle_delta + 1, point_interval):
                            if abs(dy) <= (triangle_delta - dx):  # Inside triangular region
                                delta_horizontal.append((end_x + dx, end_y + dy))
                    polygon_points += delta_horizontal
            
            
            
            elif len(coordinates) > 4:
                start_x, start_y = coordinates[1]  # First point
                end_x, end_y = coordinates[0]  # Last point
                
                delta_vertical = []
                delta_horizontal = []
                
                # Horizontal end (triangle extending vertically from the end)
                if abs(end_x - start_x) > abs(end_y - start_y):
                    # Triangle extends vertically from the horizontal end
                    for dx in range(-triangle_delta, triangle_delta + 1, point_interval):
                        for dy in range(-triangle_delta, triangle_delta + 1, point_interval):
                            if abs(dx) <= (triangle_delta - dy):  # Inside triangular region
                                delta_vertical.append((end_x + dx, end_y + dy))
                    polygon_points += delta_vertical

                # Vertical end (triangle extending horizontally from the end)
                if abs(end_y - start_y) > abs(end_x - start_x):
                    # Triangle extends horizontally from the vertical end
                    for dy in range(-triangle_delta, triangle_delta + 1, point_interval):
                        for dx in range(-triangle_delta, triangle_delta + 1, point_interval):
                            if abs(dy) <= (triangle_delta - dx):  # Inside triangular region
                                delta_horizontal.append((end_x + dx, end_y + dy))
                    polygon_points += delta_horizontal
                
                
                start_x, start_y = coordinates[len(coordinates)//2 - 2]  # First point
                end_x, end_y = coordinates[len(coordinates)//2 - 1]  # Last point

                # Horizontal end (triangle extending vertically from the end)
                if abs(end_x - start_x) > abs(end_y - start_y):
                    # Triangle extends vertically from the horizontal end
                    for dx in range(-triangle_delta, triangle_delta + 1, point_interval):
                        for dy in range(-triangle_delta, triangle_delta + 1, point_interval):
                            if abs(dx) <= (triangle_delta - dy):  # Inside triangular region
                                delta_vertical.append((end_x + dx, end_y + dy))
                    polygon_points += delta_vertical

                # Vertical end (triangle extending horizontally from the end)
                if abs(end_y - start_y) > abs(end_x - start_x):
                    # Triangle extends horizontally from the vertical end
                    for dy in range(-triangle_delta, triangle_delta + 1, point_interval):
                        for dx in range(-triangle_delta, triangle_delta + 1, point_interval):
                            if abs(dy) <= (triangle_delta - dx):  # Inside triangular region
                                delta_horizontal.append((end_x + dx, end_y + dy))
                    polygon_points += delta_horizontal

            # Store all points
            center_coordinates[refid] = polygon_points
            
        else:
            print(f"Unknown shape or invalid coordinates for refid: {refid}")

    return center_coordinates

# Function to get the score for each square
def get_score(x, y, refId_coordinates_center, sorted_concept_refid_score, gradient_width=50):
    """
    Calculates the score based on how close (x, y) is to the closest coordinate
    in refId_coordinates_center. The closer (x, y) is to the center, the higher the score.
    If (x, y) is more than 50 units away from the closest coordinate, the score is 0.

    :param x: The x-coordinate of the point.
    :param y: The y-coordinate of the point.
    :param refId_coordinates_center: A dictionary of refId and their center coordinates.
    :return: A score based on the distance to the closest coordinate.
    """

    # Initialize a variable to keep track of the minimum distance
    min_distance = float("inf")
    closest_refid = None
        
    # Loop through the centers of the reference shapes to find the closest one
    for refid, points in refId_coordinates_center.items():
        # calculate the distance to each point
        distance = min(math.sqrt((x - px) ** 2 + (y - py) ** 2) for px, py in points)
        
        if distance < min_distance:
            closest_refid = refid
            
        # Track the minimum distance
        min_distance = min(min_distance, distance)
                
    # If the distance is greater than gradient_width, return score of 0
    if min_distance > gradient_width:
        return 0
    
    closest_refid_score = sorted_concept_refid_score[closest_refid]
    
    # Calculate the score based on the minimum distance
    score = max(0, 10 - min_distance) * math.log(closest_refid_score)  # Ensure score doesn't go below 0
    
    return score

# Function to assign a color with transparency based on the score and color palette
def get_color(score, min_score, max_score, transparency=255):
    """
    Get a color (RGBA) based on the score, transitioning from Green → Yellow → Red,
    with optional transparency.

    :param score: The score of the square
    :param min_score: The minimum score (for normalization)
    :param max_score: The maximum score (for normalization)
    :param transparency: The transparency level (0 to 255, default 255 for fully opaque)
    :return: A tuple representing the RGBA color
    """
    # Normalize the score to the range [0, 1]
    normalized_score = (score - min_score) / (max_score - min_score)

    if normalized_score == 0:
        # white for all pixels out of gradient_width
        red = 255
        green = 255
        blue = 255
        transparency = 0
    elif 0 < normalized_score <= 0.5:
        # Green → Yellow
        # Red increases from 0 to 255, Green stays at 255, Blue stays at 0
        red = int(
            255 * (normalized_score * 2)
        )  # Scale normalized_score [0, 0.5] → [0, 1]
        green = 255
        blue = 0
    elif 0.5 < normalized_score <= 1.0:
        # Yellow → Red
        # Red stays at 255, Green decreases from 255 to 0, Blue stays at 0
        red = 255
        green = int(
            255 * (1 - (normalized_score - 0.5) * 2)
        )  # Scale normalized_score [0.5, 1] → [1, 0]
        blue = 0

    # Return the color with the specified transparency
    return (red, green, blue, transparency)

# Function to color the diagram according to the data received in rect_refid_list
def processDiagram(image_path, diagram_xml_file, rect_refid_list, sorted_concept_refid_score, square_size, point_interval, triangle_delta, gradient_width, rectangle_coverage, transparency):
    image = Image.open(image_path)
    
    # Get the image dimensions
    width, height = image.size
    
    # Create a list to store the scores
    scores = []
    
    # Get the coordinates of the reference shapes (rectangles, etc.)
    refId_coordinates = get_shapes(rect_refid_list, sorted_concept_refid_score, diagram_xml_file)
    
    # Get the center coordinates of the reference shapes
    refId_coordinates_center = get_center(refId_coordinates, diagram_xml_file, rectangle_coverage, point_interval, triangle_delta)
    
    # Loop over the image and calculate the scores for each square
    for y in range(0, height, square_size):
        for x in range(0, width, square_size):
            # Ensure that the square doesn't go out of bounds
            if x + square_size <= width and y + square_size <= height:
                score = get_score(x, y, refId_coordinates_center, sorted_concept_refid_score, gradient_width)
                scores.append(
                    (x, y, score)
                )  # Store the score with its top-left corner position

    # Find the minimum and maximum scores to normalize
    min_score = min(score for _, _, score in scores)
    max_score = max(score for _, _, score in scores)
    
    # Convert the original image to RGBA mode to support transparency
    image = image.convert("RGBA")

    # Loop through each square and assign color with transparency to the corresponding pixels
    for x, y, score in scores:
        # Get the color for the current square
        color = get_color(score, min_score, max_score, transparency)
        
        # Create an empty RGBA image for the overlay
        overlay = Image.new("RGBA", (width, height), (0, 0, 0, 0))

        # Set the color for the 10x10 block starting at (x, y)
        for dy in range(square_size):
            for dx in range(square_size):
                if x + dx < width and y + dy < height:
                    # Get the overlay color with transparency
                    overlay.putpixel((x + dx, y + dy), color)

        # Combine the overlay with the original image
        image = Image.alpha_composite(image, overlay)

    return image