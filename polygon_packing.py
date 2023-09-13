import numpy as np
from rectangle_packing import *
from plotting import *
import random
import numpy as np
from fractions import Fraction

def compute_polygon_width(polygon, return_vertices=False):
    """Compute the width of a polygon based on its vertices.
    
    Args:
    - polygon (list of tuple): A list of vertices of the polygon.
    - return_vertices (bool, optional): If set to True, the function also returns the leftmost and rightmost vertices of the polygon. Defaults to False.

    Returns:
    - float or tuple: Width of the polygon. If return_vertices is True, it returns the width, leftmost vertex, and rightmost vertex.
    """
    # Find the leftmost and rightmost vertices
    min_vert = min(polygon,key=lambda i:i[0])
    max_vert = max(polygon,key = lambda i:i[0])
    
    # If return_vertices flag is set, return width along with leftmost and rightmost vertices
    if return_vertices:
        return max_vert[0] - min_vert[0], min_vert, max_vert
    # Otherwise, just return width of the polygon
    else:
        return max_vert[0] - min_vert[0]

def compute_polygon_height(polygon, return_vertices=False):
    """Compute the height of a polygon based on its vertices.

    Args:
    - polygon (list of tuple): A list of vertices of the polygon.
    - return_vertices (bool, optional): If set to True, the function also returns the bottommost and topmost vertices of the polygon. Defaults to False.

    Returns:
    - float or tuple: Height of the polygon. If return_vertices is True, it returns the height, bottommost vertex, and topmost vertex.
    """
    # Find the bottommost and topmost vertices
    min_vert = min(polygon,key=lambda i:i[1])
    max_vert = max(polygon,key = lambda i:i[1])
    
    # If return_vertices flag is set, return height along with leftmost and rightmost vertices
    if return_vertices:
        return max_vert[1] - min_vert[1], min_vert, max_vert
    # Otherwise, just return height of the polygon
    else:
        return max_vert[1] - min_vert[1]
    
def compute_max_min_vertices_wrt_vector(polygon,vector):
    """
    Determines the vertices of the polygon with maximum and minimum dot products with respect to a given vector.
    These vertices correspond to the points that are furthest / least furthest in the diretion of the vector.

    Args:
    - polygon (list of tuple): A list of vertices of the polygon.
    - vector (tuple): A given vector.

    Returns:
    - tuple: Vertices with the minimum and maximum dot product values.
    """
    min_vert = min(polygon,key=lambda i: np.dot(vector,i))
    max_vert = max(polygon,key=lambda i: np.dot(vector,i))
    
    return min_vert, max_vert

def compute_bounding_parallelogram(polygon):
    """
    Compute the bounding parallelogram of a given polygon.

    Args:
    - polygon (list of tuple): A list of vertices of the left- and bottom-adjusted polygon. Left- and bottom-adjusted means that the lowest x-coordinate vertex of the polygon has x-coordinate 0 and similar for the lowest y-coordinate vertex.

    Returns:
    - tuple: The bounding parallelogram and the location of its left lower corner relative to the coordinate system of the polygon.
    """
    height, min_h_vert, max_h_vert = compute_polygon_height(polygon, return_vertices=True)
    # The spine connects a topmost and bottommost vertice
    spine = ([min_h_vert,max_h_vert])
    wside = spine[1][0] - spine[0][0]
    # Compute normal (perpendicular) to the spine
    normal_to_spine = ([max_h_vert[1]-min_h_vert[1],min_h_vert[0]-max_h_vert[0]])
    
    # Find the leftmost and rightmost vertices with respect to the spine
    leftest_wrt_spine, rightest_wrt_spine = compute_max_min_vertices_wrt_vector(polygon,normal_to_spine)
    right_lower_point = (rightest_wrt_spine[0] - wside*rightest_wrt_spine[1]/height,0)
    left_lower_point = (leftest_wrt_spine[0] -  wside*leftest_wrt_spine[1]/height,0)
    
    # Compute the base of the parallelogram
    base = right_lower_point[0] - left_lower_point[0]
    width, min_w_vert, max_w_vert = compute_polygon_width(polygon,return_vertices=True)
    
    # If the base of the parallelogram is smaller than the width of the polygon, return the parallelogram, as well as the left_lower_point
    if base < width:
        return (base,height,wside), left_lower_point[0]
    # Otherwise, return a bounding rectangle of the polygon instead
    else:
        return (width,height,0), 0

def ordering_parallelograms_by_slope(parallelograms,return_map = False):
    """
    Orders a list of parallelograms by their slope (=wside/height).

    Args:
    - parallelograms (list of tuple): A list of parallelograms.
    - return_map (bool, optional): If set to True, the function also returns the original indices of the sorted parallelograms. Defaults to False.

    Returns:
    - list or tuple: A list of parallelograms sorted by slope. If return_map is True, it returns the list and a map mapping the original indices to their new positions.
    """
    # Sort parallelograms based on the slope formed by height and wside
    parallelograms_sorted = sorted(parallelograms,key = lambda i:i[2]/i[1],reverse=False)
    
    if return_map:
        # Return the sorted order and the corresponding map
        parallelograms_order = sorted(range(len(parallelograms)),key = lambda i:parallelograms[i][2]/parallelograms[i][1],reverse=False)
        parallelograms_map = sorted(range(len(parallelograms)),key = lambda i:parallelograms_order[i])
        return parallelograms_sorted, parallelograms_map
    return parallelograms_sorted

def polygon_packing(polygons,c=3,rectangle_strip_packing_algorithm="ffdh",return_shelf_lines=False,return_rectangles_packing = False):
    """
    Tightly packs a list of polygons into a strip of fixed width, using the algorithm from https://drops-beta.dagstuhl.de/entities/document/10.4230/LIPIcs.ESA.2023.76.

    Args:
    - polygons (list of list): A list of left- and bottom-adjusted polygons. Left- and bottom-adjusted means that the lowest x-coordinate vertex of the polygon has x-coordinate 0 and similar for the lowest y-coordinate vertex.
    - c (int, optional): A constant determining the strip width. Defaults to 3 (which gives the best approximation guarantee for area minimization).
    - rectangle_strip_packing_algorithm (str, optional): The algorithm used for rectangle strip packing, either "ffdh" or "nfdh". Defaults to "ffdh".
    - return_shelf_lines (bool, optional): If set to True, the function also returns lines that separate the shelves. Defaults to False.
    - return_rectangles_packing (bool, optional): If set to True, the function returns data about how rectangles are packed. Defaults to False.

    Returns:
    - tuple: Depending on flags, the function returns the packed polygons, parallelograms, width and height of the packing, and optionally other information.
    """    
    # Compute the bounding parallelogram of each polygon and compute w_max, the maximum width of any polygon.
    parallelograms = []
    delta = []
    w_max = 0
    for polygon in polygons:
        parallelogram, delta_i = compute_bounding_parallelogram(polygon)
        parallelograms += [parallelogram]
        delta += [delta_i] #delta_i is the location of the left lower corner of the parallelogram with respect to (0,0) in the coordinate system of the polygon
        w = compute_polygon_width(polygon)
        if w > w_max:
            w_max = w
    
    # Define the width of the strip
    stripwidth = c*w_max    
    
    # For each Polygon q=(base,height,wside), define a rectangle r=(base,height)
    rectangles = [[parallelogram[0],parallelogram[1]] for parallelogram in parallelograms]
    
    # Pack rectangles with FFDH or NFDH algorithm
    if rectangle_strip_packing_algorithm == "ffdh":
        rectangles_shelves, heights_shelves, map_rectangles_shelves = ffdh(rectangles, stripwidth=stripwidth, return_map=True)
    elif rectangle_strip_packing_algorithm == "nfdh":
        rectangles_shelves, heights_shelves, map_rectangles_shelves = nfdh(rectangles, stripwidth=stripwidth, return_map=True)
    else:
        print("Rectangle Shelf Packing Algorithm \"",rectangle_strip_packing_algorithm,"\" is not supported.") 
        return None
    
    # Compute the shelves with the parallelograms and create a mapping between parallelograms and their shelf number and order within that shelf.
    parallelograms_shelves = [[0]*len(shelf) for shelf in rectangles_shelves]
    for i in range(len(polygons)):
        parallelograms_shelves[map_rectangles_shelves[i][0]][map_rectangles_shelves[i][1]] = parallelograms[i]
    
    # Order the parallelograms within each shelf by their slope
    parallelograms_shelves_ordered = [[] for x in range(len(rectangles_shelves))]
    parallelograms_shelves_ordering_map = [[] for x in range(len(rectangles_shelves))]
    for i in range(len(parallelograms_shelves)):
        parallelograms_shelves_ordered[i], parallelograms_shelves_ordering_map[i] = ordering_parallelograms_by_slope(parallelograms_shelves[i],return_map = True)
    
    map_parallelograms_shelves = [(map_rectangles_shelves[i][0],parallelograms_shelves_ordering_map[map_rectangles_shelves[i][0]][map_rectangles_shelves[i][1]]) for i in range(len(parallelograms))]
    
    #Compute the coordinates of the left lower vertex of each parallelogram in the packing.
    coordinates_parallelograms = [(w_max + sum(a for a,b,c in parallelograms_shelves_ordered[map_parallelograms_shelves[i][0]][:map_parallelograms_shelves[i][1]]),sum(heights_shelves[:map_parallelograms_shelves[i][0]])) for i in range(len(parallelograms))]
    
    #Compute the coordinates of all vertices of each parallelogram in the packing.
    packed_parallelograms = []
    packed_polygons = []
    
    for i in range(len(parallelograms)):
        x_0 = coordinates_parallelograms[i][0]
        y_0 = coordinates_parallelograms[i][1]
        base = parallelograms[i][0]
        height = parallelograms[i][1]
        wside = parallelograms[i][2]
        packed_parallelograms += [[(x_0,y_0),(x_0+base,y_0),(x_0+wside,y_0+height),(x_0+wside+base,y_0+height)]]
        
        packed_polygon = [(x_0 - delta[i] + polygons[i][j][0],y_0 + polygons[i][j][1]) for j in range(len(polygons[i]))]
        packed_polygons += [packed_polygon]
    
    #Compute bounds on the maximum width and the height of the packing.
    width = (c+2)*w_max
    height = sum(heights_shelves)
    
    output = (packed_polygons, packed_parallelograms, width, height)
    
    if return_shelf_lines:
        # Define the shelf and side lines for visualization purposes
        shelf_lines = [[(0,sum(heights_shelves[:i])),(width,sum(heights_shelves[:i]))] for i in range(len(heights_shelves)-1)]
        side_lines = [[(w_max,0),(w_max,height)],[((c+1)*w_max,0),((c+1)*w_max,height)]]
        
        lines = shelf_lines + side_lines
        output = output + (lines,)
    
    if return_rectangles_packing:
        output = output + (rectangles_shelves, heights_shelves)
    
    return output

def left_bottom_adjust_polygon(polygon):
    min_x = min(polygon,key=lambda i:i[0])[0]
    min_y = min(polygon,key=lambda i:i[1])[1]
    
    return [(w-min_x,h-min_y) for w,h in polygon]