#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 10 15:18:40 2023

@author: sisuter
"""

def order_by_height(rectangles):
    rectangles.sort(reverse=True)


def nfdh(rectangles,stripwidth=1,return_map=False):
    rectangles_sorted = sorted(rectangles,key = lambda i:i[1],reverse=True)
    if return_map == True:
        rectangles_height_order = sorted(range(len(rectangles)),key = lambda i:rectangles[i][1],reverse=True)
        rectangles_height_map = sorted(range(len(rectangles)),key = lambda i: rectangles_height_order[i])
        
    #do nf
    S = [[rectangles_sorted[0]]]
    w_S = [rectangles_sorted[0][0]]
    h_S = [rectangles_sorted[0][1]]
    rectangles_map_for_sorted = [(0,0)]
    for i in range(1,len(rectangles_sorted)):
        if w_S[-1] + rectangles_sorted[i][0] <= stripwidth:
            S[-1].append(rectangles_sorted[i])
            w_S[-1] += rectangles_sorted[i][0]
        else:
            S.append([rectangles_sorted[i]])
            w_S.append(rectangles_sorted[i][0])
            h_S.append(rectangles_sorted[i][1])
        if return_map == True:
            rectangles_map_for_sorted.append((len(S)-1,len(S[-1])-1))
    if return_map == True:
        rectangles_map = [rectangles_map_for_sorted[rectangles_height_map[i]] for i in range(len(rectangles))]
        return S, h_S, rectangles_map
    return S, h_S

def ffdh(rectangles,stripwidth=1,return_map=False):
    rectangles_sorted = sorted(rectangles,key = lambda i:i[1],reverse=True)
    if return_map == True:
        rectangles_height_order = sorted(range(len(rectangles)),key = lambda i:rectangles[i][1],reverse=True)
        rectangles_height_map = sorted(range(len(rectangles)),key = lambda i: rectangles_height_order[i])
        
    #do ff
    S = [[rectangles_sorted[0]]]
    w_S = [rectangles_sorted[0][0]]
    h_S = [rectangles_sorted[0][1]]
    rectangles_map_for_sorted = [(0,0)]
    for i in range(1,len(rectangles_sorted)):
        fit_in = False
        for j in range(len(S)):
            if w_S[j] + rectangles_sorted[i][0] <= stripwidth:
                S[j].append(rectangles_sorted[i])
                w_S[j] += rectangles_sorted[i][0]
                fit_in = True
                if fit_in == True and return_map == True:
                    rectangles_map_for_sorted.append((j,len(S[j])-1))
                break
        if fit_in == True:
            continue
        else:
            S.append([rectangles_sorted[i]])
            w_S.append(rectangles_sorted[i][0])
            h_S.append(rectangles_sorted[i][1])
            if return_map == True:
                rectangles_map_for_sorted.append((len(S)-1,0))
                
    if return_map == True:
        rectangles_map = [rectangles_map_for_sorted[rectangles_height_map[i]] for i in range(len(rectangles))]
        return S, h_S, rectangles_map
    return S, h_S

def calc_coords_of_shelf_packing(shelves,shelf_heights):
    rectangles_placed = []
    H = 0
    for i in range(len(shelves)):
        W = 0
        for j in range(len(shelves[i])):
            rectangles_placed += [((W,H),shelves[i][j][0],shelves[i][j][1])]
            W += shelves[i][j][0]
        H += shelf_heights[i]
    return rectangles_placed


"""
rectangles = [
    (1,2),
    (4,1),
    (2,1),
    (1,3),
    (3,1),
    (1,2),
    (3,1),
    (1,2),
    (3,1),
    (1,2),
    (2,1),
    (2,2),
    (1,2),
    (2,2),
    (1,4),
    (2,1)]

S_nfdh,h_S_nfdh = nfdh(rectangles,stripwidth=4)
S_ffdh,h_S2_ffdh = ffdh(rectangles,stripwidth=4)

rectangles_placed_nfdh = calc_coords_of_shelf_packing(S_nfdh,h_S_nfdh)
rectangles_placed_ffdh = calc_coords_of_shelf_packing(S_nfdh,h_S_nfdh)
"""