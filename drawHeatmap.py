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


