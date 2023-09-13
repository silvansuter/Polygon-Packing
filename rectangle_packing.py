def order_by_height(rectangles):
    """
    Sorts the given list of rectangles in descending order by height in-place.

    Args:
    - rectangles (list of tuple): List of rectangles where each rectangle is a tuple (width, height).
    
    Returns:
    - None: Modifies the input list in-place.
    """
    rectangles.sort(reverse=True)

def nfdh(rectangles,stripwidth=1,return_map=False):
    """
    Packs the rectangles using the Next Fit Decreasing Height (NFDH) algorithm, see https://en.wikipedia.org/wiki/Strip_packing_problem.

    Args:
    - rectangles (list of tuple): List of rectangles where each rectangle is a tuple (width, height).
    - stripwidth (int, optional): Maximum width of the strip. Defaults to 1.
    - return_map (bool, optional): Whether to return a map indicating the position of each rectangle. Defaults to False.

    Returns:
    - tuple: Packed shelves of rectangles, heights of each shelf, and optionally a map indicating position of each rectangle.
    """
    # Sort rectangles by height in descending order
    rectangles_sorted = sorted(rectangles,key = lambda i:i[1],reverse=True)
    if return_map:
        # Create a map for the order of rectangles by height
        rectangles_height_order = sorted(range(len(rectangles)),key = lambda i:rectangles[i][1],reverse=True)
        rectangles_height_map = sorted(range(len(rectangles)),key = lambda i: rectangles_height_order[i])
        
    # Initialize shelves and other data structures
    S = [[rectangles_sorted[0]]]
    w_S = [rectangles_sorted[0][0]]
    h_S = [rectangles_sorted[0][1]]
    rectangles_map_for_sorted = [(0,0)]
    for i in range(1,len(rectangles_sorted)):
        # If the rectangle fits in the current shelf, add it
        if w_S[-1] + rectangles_sorted[i][0] <= stripwidth:
            S[-1].append(rectangles_sorted[i])
            w_S[-1] += rectangles_sorted[i][0]
        # Otherwise, start a new shelf
        else:
            S.append([rectangles_sorted[i]])
            w_S.append(rectangles_sorted[i][0])
            h_S.append(rectangles_sorted[i][1])
        # Update rectangle map for sorted list
        if return_map:
            rectangles_map_for_sorted.append((len(S)-1,len(S[-1])-1))
    if return_map:
        rectangles_map = [rectangles_map_for_sorted[rectangles_height_map[i]] for i in range(len(rectangles))]
        return S, h_S, rectangles_map
    return S, h_S

def ffdh(rectangles,stripwidth=1,return_map=False):
    """
    Packs the rectangles using the First Fit Decreasing Height (FFDH) algorithm, see https://en.wikipedia.org/wiki/Strip_packing_problem.

    Args:
    - rectangles (list of tuple): List of rectangles where each rectangle is a tuple (width, height).
    - stripwidth (int, optional): Maximum width of the strip. Defaults to 1.
    - return_map (bool, optional): Whether to return a map indicating the position of each rectangle. Defaults to False.

    Returns:
    - tuple: Packed shelves of rectangles, heights of each shelf, and optionally a map indicating position of each rectangle.
    """
    # Sort rectangles by height in descending order
    rectangles_sorted = sorted(rectangles,key = lambda i:i[1],reverse=True)
    if return_map:
        # Create a map for the order of rectangles by height
        rectangles_height_order = sorted(range(len(rectangles)),key = lambda i:rectangles[i][1],reverse=True)
        rectangles_height_map = sorted(range(len(rectangles)),key = lambda i: rectangles_height_order[i])
        
    # Initialize shelves and other data structures
    S = [[rectangles_sorted[0]]]
    w_S = [rectangles_sorted[0][0]]
    h_S = [rectangles_sorted[0][1]]
    rectangles_map_for_sorted = [(0,0)]
    for i in range(1,len(rectangles_sorted)):
        fit_in = False
        # Iterate over all opened shelves
        for j in range(len(S)):
            # If the rectangle fits in the currently considered shelf, add it
            if w_S[j] + rectangles_sorted[i][0] <= stripwidth:
                S[j].append(rectangles_sorted[i])
                w_S[j] += rectangles_sorted[i][0]
                fit_in = True
                # Update rectangle map for sorted list
                if fit_in and return_map:
                    rectangles_map_for_sorted.append((j,len(S[j])-1))
                break
        if fit_in:
            continue
        # If the rectangle fits into none of the previously opened shelves, start a new one
        else:
            S.append([rectangles_sorted[i]])
            w_S.append(rectangles_sorted[i][0])
            h_S.append(rectangles_sorted[i][1])
            # Update rectangle map for sorted list
            if return_map:
                rectangles_map_for_sorted.append((len(S)-1,0))
    
    if return_map:
        rectangles_map = [rectangles_map_for_sorted[rectangles_height_map[i]] for i in range(len(rectangles))]
        return S, h_S, rectangles_map
    return S, h_S

def calc_coords_of_shelf_packing(shelves,shelf_heights):
    """
    Calculates the coordinates for each rectangle given their shelves and shelf heights.

    Args:
    - shelves (list of list): Packed shelves of rectangles.
    - shelf_heights (list of int): Heights of each shelf.

    Returns:
    - list: List of rectangles with their placement coordinates.
    """
    # Initialize an empty list to store the placed rectangles with their coordinates
    rectangles_placed = []
    
    # Start from the base (H=0) for the first shelf
    H = 0
    
    # Loop through each shelf
    for i in range(len(shelves)):
        # Reset the width (W=0) for every new shelf
        W = 0
        # Loop through each rectangle in the current shelf
        
        for j in range(len(shelves[i])):
            # Append the rectangle with its placement coordinates (bottom-left corner)
            rectangles_placed += [((W,H),shelves[i][j][0],shelves[i][j][1])]
            # Increment the width to fit the left side of the next rectangle in the same shelf
            W += shelves[i][j][0]
            
        # Increment the height to be equal to the height of the bottom of the next shelf (= height at top of the current shelf)
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