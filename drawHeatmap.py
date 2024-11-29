def get_shapes(rect_refid_list, diagram_xml_file):
    # receive rect_refid_list which contains a list of refiD for shapes of rectangles
    # First it identifies the x and y for the rectangle shapes in the XML file
    # if there's more than two rect shapes it search to see if there's a poly that
    # connect these two rect, if there is a poly, the x and y of that poly is added to returned list
    # 
    # 
    # return a list of x,y cooordinates for rect and poly connecting rect to each other
    # for each item in the returned list 4 (x,y) cooridicates.
    refId_coordinates = []
    
    return refId_coordinates

def get_center(refId_coordinates):
    # receive a list of refId_coordinates and use 4 points of each refid to calclute
    # x and y center
    x_center = 0
    y_center = 0
    return x_center, y_center


# Function to get the score for each square (to be defined by you later)
def get_score(x, y, refid_list):
    # Placeholder for your actual scoring function
    return x + y


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

    if normalized_score <= 0.5:
        # Green → Yellow
        # Red increases from 0 to 255, Green stays at 255, Blue stays at 0
        red = int(
            255 * (normalized_score * 2)
        )  # Scale normalized_score [0, 0.5] → [0, 1]
        green = 255
        blue = 0
    else:
        # Yellow → Red
        # Red stays at 255, Green decreases from 255 to 0, Blue stays at 0
        red = 255
        green = int(
            255 * (1 - (normalized_score - 0.5) * 2)
        )  # Scale normalized_score [0.5, 1] → [1, 0]
        blue = 0

    # Return the color with the specified transparency
    return (red, green, blue, transparency)
