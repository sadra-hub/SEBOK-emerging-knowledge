import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import textwrap

# Parse the XML file
tree = ET.parse('diagram.xml')
root = tree.getroot()

# Find the diagram element
diagram = root.find('.//diagram')

# Set up the figure
fig, ax = plt.subplots(figsize=(10, 6))
ax.set_xlim(0, int(diagram.get('width')))
ax.set_ylim(0, int(diagram.get('height')))
ax.set_aspect('equal')
ax.set_title(diagram.find('name').text)

# Helper function to adjust text size
def get_optimal_font_size(text, max_width, max_height, max_font_size=12):
    """Determine font size so text fits within a rectangle."""
    font_size = max_font_size
    wrapped_text = text  # Default, no wrapping
    
    # Make sure we don't attempt to scale down below font size 6
    while font_size > 6:
        test_text = ax.text(0, 0, wrapped_text, fontsize=font_size, ha='center', va='center')
        fig.canvas.draw()  # Force the figure to be drawn and updated
        bbox = test_text.get_window_extent()
        text_width = bbox.width / fig.dpi * 72  # Convert width from pixels to points
        text_height = bbox.height / fig.dpi * 72  # Convert height from pixels to points

        # Check if the text fits within the rectangle
        if text_width <= max_width and text_height <= max_height:
            return font_size, wrapped_text
        
        # If it doesn't fit, reduce font size and try wrapping
        font_size -= 1
        
        # Prevent zero width issues by setting a valid minimum width for wrapping
        if font_size > 6:
            wrapped_text = textwrap.fill(text, width=int(max_width // font_size))
        else:
            break  # Break out of the loop if font size is too small

    # Return minimum font size and wrapped text
    return 6, wrapped_text

# Parse and draw areas
for area in diagram.find('map').findall('area'):
    points = area.findall('point')
    x_coords = [int(point.get('x')) for point in points]
    y_coords = [int(point.get('y')) for point in points]
    
    # Compute rectangle dimensions
    x_min, x_max = min(x_coords), max(x_coords)
    y_min, y_max = min(y_coords), max(y_coords)
    width = x_max - x_min
    height = y_max - y_min
    
    # Draw rectangle
    rect = Rectangle((x_min, int(diagram.get('height')) - y_max), width, height, 
                     edgecolor='blue', facecolor='lightblue', alpha=0.5)
    ax.add_patch(rect)
    
    # Get optimal font size and wrapped text for the label
    label_text = area.get('name')
    font_size, wrapped_text = get_optimal_font_size(label_text, width, height)

    # Add label
    label_x = x_min + width / 2
    label_y = int(diagram.get('height')) - y_max + height / 2
    ax.text(label_x, label_y, wrapped_text, color='black', ha='center', va='center', 
            fontsize=font_size)

# Hide axes
ax.axis('off')

# Show the diagram
plt.show()