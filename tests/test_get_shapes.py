from diagrams.parseDiagram import get_shapes

# Path to your existing test_diagram.xml
TEST_DIAGRAM_PATH = "tests/test_diagram.xml"

# Test cases
def test_get_shapes_with_valid_data():
    rect_refid_list = ["rect1", "rect2"]  # Update these IDs to match the actual `refid` in your XML
    expected_output = {
        "rect1": [(100, 200), (150, 200), (150, 250), (100, 250)],
        "rect2": [(300, 400), (350, 400), (350, 450), (300, 450)],
        # Add additional expected outputs as necessary
    }

    result = get_shapes(rect_refid_list, TEST_DIAGRAM_PATH)
    assert result == expected_output

def test_get_shapes_with_missing_shapes():
    rect_refid_list = ["nonexistent_refid"]  # ID that doesn't exist in the XML
    result = get_shapes(rect_refid_list, TEST_DIAGRAM_PATH)
    assert result == {}  # Should return an empty dictionary

def test_get_shapes_with_only_polygons():
    rect_refid_list = []  # No rectangles provided
    result = get_shapes(rect_refid_list, TEST_DIAGRAM_PATH)
    # Update expected_output if polygons should be returned without rectangles
    assert result == {}