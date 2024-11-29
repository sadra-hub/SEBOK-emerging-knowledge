from PIL import Image
import xml.etree.ElementTree as ET

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


# Load the image
image_path = "diagram.jpg"  # Replace with your image path
image = Image.open(image_path)

# Get the image dimensions
width, height = image.size

# Define the square size
square_size = 10

# Create a list to store the scores
scores = []

# Loop over the image and calculate the scores for each square
for y in range(0, height, square_size):
    for x in range(0, width, square_size):
        # Ensure that the square doesn't go out of bounds
        if x + square_size <= width and y + square_size <= height:
            score = get_score(x, y)
            scores.append(
                (x, y, score)
            )  # Store the score with its top-left corner position

# Find the minimum and maximum scores to normalize
min_score = min(score for _, _, score in scores)
max_score = max(score for _, _, score in scores)

# Define a color palette (e.g., from red to green)
color_palette = [(255, 0, 0), (0, 255, 0)]  # Red to Green

# Convert the original image to RGBA mode to support transparency
image = image.convert("RGBA")


# Loop through each square and assign color with transparency to the corresponding pixels
for x, y, score in scores:
    # Get the color for the current square
    transparency = 180  # Set desired transparency level (0-255)
    color = get_color(score, min_score, max_score, transparency)

    # Set the color for the 10x10 block starting at (x, y)
    for dy in range(square_size):
        for dx in range(square_size):
            if x + dx < width and y + dy < height:  # Ensure we don't go out of bounds
                # Get the current pixel color from the original image
                original_pixel = image.getpixel((x + dx, y + dy))

                # Blend the original image pixel with the color using alpha transparency
                r1, g1, b1, a1 = original_pixel
                r2, g2, b2, a2 = color

                # Apply alpha blending (simple linear interpolation based on transparency)
                alpha = a2 / 255.0  # Transparency as a float between 0 and 1
                r = int(r1 * (1 - alpha) + r2 * alpha)
                g = int(g1 * (1 - alpha) + g2 * alpha)
                b = int(b1 * (1 - alpha) + b2 * alpha)
                a = int(a1 * (1 - alpha) + a2 * alpha)

                # Set the new blended color with transparency
                image.putpixel((x + dx, y + dy), (r, g, b, a))

# Save the colored image with transparency to a new file
image.save(
    "colored_image_with_transparency_overlay.png"
)  # Save as PNG to preserve transparency

# Optionally, show the image
image.show()
