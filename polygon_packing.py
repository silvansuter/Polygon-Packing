#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 10 16:18:30 2023

@author: sisuter
"""


import numpy as np
from algorithms_ffdh_nfdh import *
from rectangle_bin_plotter import *
import random
import numpy as np
from fractions import Fraction

def compute_polygon_width(polygon, return_vertices=False):
    min_vert = min(polygon,key=lambda i:i[0])
    max_vert = max(polygon,key = lambda i:i[0])
    
    if return_vertices == True:
        return max_vert[0] - min_vert[0], min_vert, max_vert
    else:
        return max_vert[0] - min_vert[0]

def compute_polygon_height(polygon, return_vertices=False):
    min_vert = min(polygon,key=lambda i:i[1])
    max_vert = max(polygon,key = lambda i:i[1])
        
    if return_vertices == True:
        return max_vert[1] - min_vert[1], min_vert, max_vert
    else:
        return max_vert[1] - min_vert[1]
    
def compute_max_min_vertices_wrt_vector(polygon,vector):
    min_vert = min(polygon,key=lambda i: np.dot(vector,i))
    max_vert = max(polygon,key=lambda i: np.dot(vector,i))
    
    return min_vert, max_vert

def compute_bounding_parallelogram(polygon):
    #needs polygons to be leftadjusted and bottomadjusted!
    height, min_h_vert, max_h_vert = compute_polygon_height(polygon, return_vertices=True)
    spine = ([min_h_vert,max_h_vert])
    wside = spine[1][0] - spine[0][0]
    normal_to_spine = ([max_h_vert[1]-min_h_vert[1],min_h_vert[0]-max_h_vert[0]])
    
    leftest_wrt_spine, rightest_wrt_spine = compute_max_min_vertices_wrt_vector(polygon,normal_to_spine)
    right_lower_point = (rightest_wrt_spine[0] - wside*rightest_wrt_spine[1]/height,0)
    left_lower_point = (leftest_wrt_spine[0] -  wside*leftest_wrt_spine[1]/height,0)
    
    base = right_lower_point[0] - left_lower_point[0]
    width, min_w_vert, max_w_vert = compute_polygon_width(polygon,return_vertices=True)
    
    if base >= width:
        return (width,height,0), 0
    
    else:
        return (base,height,wside), left_lower_point[0]

def ordering_parallelograms_by_slope(parallelograms,return_map = False):
    parallelograms_sorted = sorted(parallelograms,key = lambda i:i[2]/i[1],reverse=False)
    if return_map == True:
        parallelograms_order = sorted(range(len(parallelograms)),key = lambda i:parallelograms[i][2]/parallelograms[i][1],reverse=False)
        parallelograms_map = sorted(range(len(parallelograms)),key = lambda i:parallelograms_order[i])
        return parallelograms_sorted, parallelograms_map
    return parallelograms_sorted

def polygon_packing(polygons,c=3,rectangle_strip_packing_algorithm="ffdh",return_shelf_lines=False,return_rectangles_packing = False):
    #Polygons need to be left- and bottom-adjusted.
    
    #Compute the bounding parallelogram of each polygon and compute w_max, the maximum width of any polygon.
    parallelograms = []
    delta = []
    w_max = 0
    for polygon in polygons:
        parallelogram, delta_i = compute_bounding_parallelogram(polygon)
        parallelograms += [parallelogram]
        delta += [delta_i]     #delta_i is the location of the left lower corner of the parallelogram with respect to (0,0) in the coordinate system of the polygon
        w = compute_polygon_width(polygon)
        if w > w_max:
            w_max = w
    
    stripwidth = c*w_max    
    
    #For each Polygon q=(base,height,wside), define a rectangle r=(base,height)
    rectangles = [[parallelogram[0],parallelogram[1]] for parallelogram in parallelograms]
    
    #Pack rectangles with FFDH or NFDH
    if rectangle_strip_packing_algorithm == "ffdh":
        rectangles_shelves, heights_shelves, map_rectangles_shelves = ffdh(rectangles, stripwidth=stripwidth, return_map=True)
    elif rectangle_strip_packing_algorithm == "nfdh":
        rectangles_shelves, heights_shelves, map_rectangles_shelves = nfdh(rectangles, stripwidth=stripwidth, return_map=True)
    else:
        print("Rectangle Strip Packing Algorithm \"",rectangle_strip_packing_algorithm,"\" is not supported.") 
        return None
    
    #Compute the shelves with the parallelograms and add a construct a map that, for any gives parallelogram, outpus its shelf number and the how manyeth polygon it is in that shelf.
    parallelograms_shelves = [[0]*len(shelf) for shelf in rectangles_shelves]
    for i in range(len(polygons)):
        parallelograms_shelves[map_rectangles_shelves[i][0]][map_rectangles_shelves[i][1]] = parallelograms[i]
    
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
    
    shelf_lines = [[(0,sum(heights_shelves[:i])),(width,sum(heights_shelves[:i]))] for i in range(len(heights_shelves)-1)]
    side_lines = [[(w_max,0),(w_max,height)],[((c+1)*w_max,0),((c+1)*w_max,height)]]
    
    lines = shelf_lines + side_lines
        
    if return_shelf_lines == True:
        return packed_polygons, packed_parallelograms, width, height, lines
    
    if return_rectangles_packing == True:
        return packed_polygons, packed_parallelograms, width, height, rectangles_shelves, heights_shelves
    
    return packed_polygons, packed_parallelograms, width, height

def left_bottom_adjust_polygon(polygon):
    min_x = min(polygon,key=lambda i:i[0])[0]
    min_y = min(polygon,key=lambda i:i[1])[1]
    
    return [(w-min_x,h-min_y) for w,h in polygon]

"""
#a first test set
polygons = [[(0,1),(1,0),(3,2),(3,4)],[(0,3),(1,0),(3,1),(2,4)],[(0,4),(1,0),(3,2),(3,3)],[(0,2),(2,5),(1,0)],[(0,5),(1,2),(2,4),(3,0)]]

packed_parallelograms = polygon_packing(polygons)[0]

visualize_polygons(packed_parallelograms,figure_size = (5,5), binsize = (20,20))
"""

"""
#a random testset of 6-gons
N=200
random_polygons = [[(0,random.random()),(random.random(),0),(random.random(),random.random()),(random.random(),random.random()),(random.random(),random.random()),(random.random(),random.random())] for i in range(N)]

packed_random_polygons, packed_random_polygons_bounding_parallelograms, width, height = polygon_packing(random_polygons,c=7)

visualize_polygons(packed_random_polygons, bounding_parallelograms = packed_random_polygons_bounding_parallelograms, figure_size = (20,20), binsize = (width,height))
"""

"""
#a random testset of 6-gons, but with integer coords
#TODO...
N=300
random_polygons = [[(0,random.randint(1,1000)/1000),(random.randint(1,1000)/1000,0),(random.randint(1,1000)/1000,random.randint(1,1000)/1000),(random.randint(1,1000)/1000,random.randint(1,1000)/1000),(random.randint(1,1000)/1000,random.randint(1,1000)/1000),(random.randint(1,1000)/1000,random.randint(1,1000)/1000)] for i in range(N)]

packed_random_polygons, packed_random_polygons_bounding_parallelograms, width, height = polygon_packing(random_polygons,c=7)

visualize_polygons(packed_random_polygons, bounding_parallelograms = packed_random_polygons_bounding_parallelograms, figure_size = (40,40), binsize = (width,height))
"""

"""
#trying it with exponentials
N=300
random_polygons = [[(0,np.random.exponential()),(np.random.exponential(),0),(np.random.exponential(),np.random.exponential()),(np.random.exponential(),np.random.exponential()),(np.random.exponential(),np.random.exponential()),(np.random.exponential(),np.random.exponential())] for i in range(N)]

packed_random_polygons, packed_random_polygons_bounding_parallelograms, width, height = polygon_packing(random_polygons,c=7)

visualize_polygons(packed_random_polygons, bounding_parallelograms = packed_random_polygons_bounding_parallelograms, figure_size = (60,60), binsize = (width,height))
"""

"""
#trying the same with fractions
N=300
random_polygons = [[(0,Fraction(random.randint(1,100),100*random.randint(1,10))),(Fraction(random.randint(1,100),100*random.randint(1,10)),0),(Fraction(random.randint(1,100),100*random.randint(1,10)),Fraction(random.randint(1,100),100*random.randint(1,10))),(Fraction(random.randint(1,100),100*random.randint(1,10)),Fraction(random.randint(1,100),100*random.randint(1,10))),(Fraction(random.randint(1,100),100*random.randint(1,10)),Fraction(random.randint(1,100),100*random.randint(1,10))),(Fraction(random.randint(1,100),100*random.randint(1,10)),Fraction(random.randint(1,100),100*random.randint(1,10)))] for i in range(N)]

packed_random_polygons, packed_random_polygons_bounding_parallelograms, width, height = polygon_packing(random_polygons,c=7)

width = float(width)
height = float(height)

print("random_polygons",random_polygons[0])
print("packed_random_polygons",packed_random_polygons[0])
print("packed_random_polygons_bounding_parallelograms",packed_random_polygons_bounding_parallelograms[0])

visualize_polygons(packed_random_polygons, bounding_parallelograms = packed_random_polygons_bounding_parallelograms, figure_size = (200,200), binsize = (width,height))
"""

"""
#trying the same with fractions
N=200
random_polygons = [[(Fraction(random.randint(1,100),100*random.randint(1,10)),Fraction(random.randint(1,100),100*random.randint(1,10))),(Fraction(random.randint(1,100),100*random.randint(1,10)),Fraction(random.randint(1,100),100*random.randint(1,10))),(Fraction(random.randint(1,100),100*random.randint(1,10)),Fraction(random.randint(1,100),100*random.randint(1,10))),(Fraction(random.randint(1,100),100*random.randint(1,10)),Fraction(random.randint(1,100),100*random.randint(1,10))),(Fraction(random.randint(1,100),100*random.randint(1,10)),Fraction(random.randint(1,100),100*random.randint(1,10))),(Fraction(random.randint(1,100),100*random.randint(1,10)),Fraction(random.randint(1,100),100*random.randint(1,10)))] for i in range(N)]

random_polygons = [left_bottom_adjust_polygon(polygon) for polygon in random_polygons]

packed_random_polygons, packed_random_polygons_bounding_parallelograms, width, height, shelf_lines = polygon_packing(random_polygons,c=7,rectangle_strip_packing_algorithm="ffdh",return_shelf_lines=True)

width = float(width)
height = float(height)

visualize_polygons(packed_random_polygons, bounding_parallelograms = packed_random_polygons_bounding_parallelograms, figure_size = (200,200), binsize = (width,height),lines=shelf_lines)
"""

"""
#new
N=300
c=15

random_polygons = [[(random.random(),random.random()) for j in range(random.randint(3,7))] for i in range(N)]

random_polygons = [left_bottom_adjust_polygon(polygon) for polygon in random_polygons]

packed_random_polygons, packed_random_polygons_bounding_parallelograms, width, height, shelf_lines = polygon_packing(random_polygons,c=c,rectangle_strip_packing_algorithm="ffdh",return_shelf_lines=True)

width = float(width)
height = float(height)

visualize_polygons(packed_random_polygons, bounding_parallelograms = packed_random_polygons_bounding_parallelograms, figure_size = (200,200), binsize = (width,height))
"""