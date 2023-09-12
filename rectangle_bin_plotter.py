import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Polygon
from scipy.spatial import ConvexHull
import matplotlib


def draw_brace(ax, xspan, yy, text):
    """
    Draws an annotated brace on the provided axes.

    Args:
    - ax (matplotlib.Axes): The axes on which the brace is drawn.
    - xspan (tuple): The starting and ending x-values of the brace.
    - yy (float): The y-value where the brace is centered.
    - text (str): The annotation text displayed above the brace.
    """
    # Extract the minimum and maximum values of the xspan and compute the span width
    xmin, xmax = xspan
    xspan = xmax - xmin
    
    # Get the current axes limits to calculate the relative size of the brace
    ax_xmin, ax_xmax = ax.get_xlim()
    xax_span = ax_xmax - ax_xmin
    ymin, ymax = ax.get_ylim()
    yspan = ymax - ymin
    
    # Set resolution, ensuring it's an odd number for symmetry purposes
    resolution = int(xspan/xax_span*100)*2+1
    
    # Set beta for exponential growth of the brace's curvature
    beta = 300./xax_span # the higher this is, the smaller the radius

    # Create x-values spanning the given range and compute the corresponding y-values for the brace
    x = np.linspace(xmin, xmax, resolution)
    x_half = x[:int(resolution/2)+1]
    y_half_brace = (1/(1.+np.exp(-beta*(x_half-x_half[0])))
                    + 1/(1.+np.exp(-beta*(x_half-x_half[-1]))))
    y = np.concatenate((y_half_brace, y_half_brace[-2::-1]))
    y = yy + (.05*y - .01)*yspan # adjust vertical position

    # Disable autoscaling and plot the brace curve
    ax.autoscale(False)
    ax.plot(x, y, color='black', lw=1)

    # Place the text above the brace
    ax.text((xmax+xmin)/2., yy+.07*yspan, text, ha='center', va='bottom')

def plot_rectangles(rectangles, size_scaling = 1, binsize = (1,1),showticks=False,cuts=[],arrows=[],pointed_rect=[],braces=[]):
    """
    Plots a list of rectangles within a specified bin size.

    Args:
    - rectangles (list): List of rectangles in the form (x, y, width, height).
    - size_scaling (float, optional): Scaling factor for the rectangle size. Defaults to 1.
    - binsize (tuple, optional): Width and height of the bounding bin. Defaults to (1,1).
    - showticks (bool, optional): Whether to show axis ticks. Defaults to False.
    - cuts (list, optional): List of rectangles to highlight as 'cuts'.
    - arrows (list, optional): List of arrows to draw.
    - pointed_rect (list, optional): List of rectangles to highlight with a dashed line.
    - braces (list, optional): List of locations and texts for braces.
    
    Returns:
    - matplotlib.Figure: Figure object for the created plot.
    """
    # Set up the plot
    fig, ax = plt.subplots()
    
    # Scale the axis borders based on the specified binsize
    [x.set_linewidth((2/5*size_scaling)*min(binsize[0], binsize[1])) for x in ax.spines.values()]
    
    # Set the x and y limits of the plot
    ax.set(xlim=(0,binsize[0]),ylim=(0,binsize[1]))
    fig.set_size_inches(size_scaling*binsize[0], size_scaling*binsize[1])
    
    # If showticks is False, remove ticks and labels from the axes
    if not showticks:
        plt.tick_params(
        axis='x',          # changes apply to the x-axis
        which='both',      # both major and minor ticks are affected
        bottom=False,      # ticks along the bottom edge are off
        top=False,         # ticks along the top edge are off
        labelbottom=False) # labels along the bottom edge are off
        
        plt.tick_params(
        axis='y',          # changes apply to the y-axis
        which='both',      # both major and minor ticks are affected
        left=False,        # ticks along the bottom edge are off
        right=False,       # ticks along the top edge are off
        labelleft=False)   # labels along the bottom edge are off
    
    # Plot regular rectangles
    for rect in rectangles:
        ax.add_patch(plt.Rectangle(rect[0],rect[1],rect[2],edgecolor="black",linewidth=(2/5*size_scaling)*min(binsize[0], binsize[1])))
    
    # Plot rectangles with dashed borders
    for rect in pointed_rect:
        ax.add_patch(plt.Rectangle(rect[0],rect[1],rect[2],edgecolor="black",linestyle='--',fill=0,linewidth=(2/5*size_scaling)*min(binsize[0], binsize[1])))
    
    # Plot 'cuts' as red rectangles
    for cut in cuts:
        ax.add_patch(plt.Rectangle(cut[0],cut[1],cut[2],edgecolor="red",linewidth=(size_scaling)*min(binsize[0], binsize[1])))
    
    # Plot arrows
    for arrow in arrows:
        plt.arrow(arrow[0],arrow[1],arrow[2],arrow[3],edgecolor="red",linewidth=(4/5*size_scaling)*min(binsize[0], binsize[1]),head_width=0.3,fill=1,facecolor="red",length_includes_head=True)
    
    # Plot braces using the earlier defined function
    for brace in braces:
        draw_brace(ax,brace[0],brace[1],brace[2])
    
    return fig

def visualize_1d(intervals, h_line_length = 0.05, binsize=1, showticks=False, plot_interval=False, remove_frame=False):
    """
    Visualizes 1D intervals on a line.

    Args:
    - intervals (list): List of intervals in the form (start, length).
    - h_line_length (float, optional): Length of horizontal lines for each interval. Defaults to 0.05.
    - binsize (int, optional): Size of the bin to fit the intervals. Defaults to 1.
    - showticks (bool, optional): Whether to show axis ticks. Defaults to False.
    - plot_interval (bool, optional): Whether to plot the full interval from 0 to binsize. Defaults to False.
    - remove_frame (bool, optional): Whether to remove the frame around the plot. Defaults to False.
    """
    # Create a new figure and axis
    fig, ax = plt.subplots()
    
    # Set the linewidth of the frame based on the bin size
    [x.set_linewidth(binsize) for x in ax.spines.values()]
    
    # Set axis limits
    ax.set(xlim=(0,binsize),ylim=(-0.1,0.1))
    fig.set_size_inches(5*binsize, 5)
    
    # If the full interval from 0 to binsize needs to be plotted
    if plot_interval:
        plt.hlines([0], [0],[binsize],color="black",linewidth=1/2,linestyle="dotted")
        plt.vlines([0], [-0.075],[0.075],color="black")
        plt.vlines([binsize], [-0.075],[0.075],color="black")
        fig.patch.set_visible(False)
    
    # If the frame around the plot needs to be removed
    if remove_frame:
        plt.box(False)
    
    # If axis ticks shouldn't be shown
    if not showticks:
        # Remove x-axis ticks and labels
        plt.tick_params(
        axis='x',          # changes apply to the x-axis
        which='both',      # both major and minor ticks are affected
        bottom=False,      # ticks along the bottom edge are off
        top=False,         # ticks along the top edge are off
        labelbottom=False) # labels along the bottom edge are off
        
        # Remove y-axis ticks and labels
        plt.tick_params(
        axis='y',          # changes apply to the y-axis
        which='both',      # both major and minor ticks are affected
        left=False,        # ticks along the bottom edge are off
        right=False,       # ticks along the top edge are off
        labelleft=False)   # labels along the bottom edge are off
    
    # Get the x values for the start and end of each interval
    x_values = [start for interval in intervals for start in [interval[0], interval[0] + interval[1]]]
    
    # Define the y values for the intervals
    y_values = [0] * len(intervals)
    
    # Get the y values for the top and bottom horizontal lines of each interval
    y_min_values = [y_values[int(i/2)] - h_line_length for i in range(2*len(y_values))]
    y_max_values = [y_values[int(i/2)] + h_line_length for i in range(2*len(y_values))]
    
    # Create the plot
    plt.hlines(y_values, x_values[::2], x_values[1::2])
    plt.vlines(x_values, y_min_values, y_max_values)
    
    # Show the plot
    plt.show()


def resize_rectangles(rectangles,factor):
    """
    Resizes a list of rectangles by a given factor.

    Args:
    - rectangles (list): List of rectangles in the form (x, y, width, height).
    - factor (float): The scaling factor to apply to each rectangle.

    Returns:
    - list: List of resized rectangles.
    """
    # Scale the x,y coordinates and the width,height of each rectangle by the given factor
    return [(tuple(factor*np.array(rectangle[0])),factor*rectangle[1],factor*rectangle[2]) for rectangle in rectangles]


def visualize_polygons(polygons,figure_size = (5,5), binsize = (1,1),showticks=False,bounding_parallelograms = [],lines = [], other_lines = [], lines_black = []):
    """
    Visualizes a list of polygons and additional geometries like (bounding) parallelograms within a specified bin size.

    Args:
    - polygons (list): List of polygons where each polygon is a list of (x, y) points.
    - figure_size (tuple, optional): Width and height of the figure in inches. Defaults to (5,5).
    - binsize (tuple, optional): Width and height of the bounding bin. Defaults to (1,1).
    - showticks (bool, optional): Whether to show axis ticks. Defaults to False.
    - bounding_parallelograms (list, optional): List of parallelograms to plot as bounding shapes.
    - lines (list, optional): List of lines to plot in red.
    - other_lines (list, optional): List of lines to plot in blue.
    - lines_black (list, optional): List of lines to plot in black.
    """
    # Create a new figure and axis
    fig, ax = plt.subplots()
    
    # Set the linewidth of the frame based on the minimum of binsize dimensions
    [x.set_linewidth(2*min(binsize[0], binsize[1])) for x in ax.spines.values()]
    
    # Set axis limits
    ax.set(xlim=(0,binsize[0]),ylim=(0,binsize[1]))
    fig.set_size_inches(5*binsize[0], 5*binsize[1])
    
    # If axis ticks shouldn't be shown
    if not showticks:
        # Remove x-axis ticks and labels
        plt.tick_params(
        axis='x',          # changes apply to the x-axis
        which='both',      # both major and minor ticks are affected
        bottom=False,      # ticks along the bottom edge are off
        top=False,         # ticks along the top edge are off
        labelbottom=False) # labels along the bottom edge are off
        
        # Remove y-axis ticks and labels
        plt.tick_params(
        axis='y',          # changes apply to the y-axis
        which='both',      # both major and minor ticks are affected
        left=False,        # ticks along the bottom edge are off
        right=False,       # ticks along the top edge are off
        labelleft=False)   # labels along the bottom edge are off
    
    """
    x_lines = [[float(line[0][0]),float(line[0][1])] for line in lines]
    y_lines = [[float(line[1][0]),float(line[1][1])] for line in lines]
    
    plt.plot(x_lines,y_lines,color="black")
    """
    
    # Plot the lines in blue
    for line in other_lines:
        a = [float(line[0][0]),float(line[1][0])]
        b = [float(line[0][1]),float(line[1][1])]
        ax.plot(a,b,color="blue",linewidth=(binsize[0]+binsize[1])*1,zorder=3)
    
    # Plot the lines in black
    for line in lines_black:
        a = [float(line[0][0]),float(line[1][0])]
        b = [float(line[0][1]),float(line[1][1])]
        ax.plot(a,b,color="black",linewidth=(binsize[0]+binsize[1])*1,zorder=3)
    
    # Plot the lines in red
    for line in lines:
        a = [float(line[0][0]),float(line[1][0])]
        b = [float(line[0][1]),float(line[1][1])]
        ax.plot(a,b,color="red",linewidth=(binsize[0]+binsize[1])*1,zorder=4)
    
    # Plot the bounding parallelograms in light grey
    for parallelogram in bounding_parallelograms:
        hull = ConvexHull(parallelogram)
        hull_points = [parallelogram[i] for i in hull.vertices]
        x_values = [point[0] for point in hull_points]
        y_values = [point[1] for point in hull_points]
        ax.add_patch(Polygon(xy=list(zip(x_values, y_values)), closed=True, edgecolor='black', facecolor='lightgrey',linewidth=min(binsize[0], binsize[1]),zorder=2))
    
    # Plot the polygons in orange
    for polygon in polygons:
        hull = ConvexHull(polygon)
        hull_points = [polygon[i] for i in hull.vertices]
        x_values = [point[0] for point in hull_points]
        y_values = [point[1] for point in hull_points]
        ax.add_patch(Polygon(xy=list(zip(x_values, y_values)), closed=True, edgecolor='black', facecolor='orange',linewidth=2*min(binsize[0], binsize[1]),joinstyle='bevel',zorder=2))
    
    # Display the plot
    plt.show()

"""
#move_by_lambda
rectangles = [((0,0),6,4),((7,1),4,6),((5,7),6,4),((1,5),4,6),((5,5),2,2)]
pointed_rect = [((1,1),6,4)]
arrows = [(4,3,-1,-1)]

plot_rectangles(rectangles,pointed_rect=pointed_rect,arrows=arrows,showticks=False,binsize=(11,11))
"""

"""
#non-guillotinable
rectangles = [((0,0),3/5,2/5),((3/5,0),2/5,3/5),((2/5,3/5),3/5,2/5),((0,2/5),2/5,3/5)]

plot_rectangles(rectangles,showticks=False)
"""


"""
#example 2-stage packing

rectangles = [((0,0),3/5,1/4),((3/5,0),1/3,1/4),((0,1/4),1,1/4),((0,1/2),1/3,1/2),((1/2,0.6),1/4,1/2),((3/4,1/2),1/4,1/2)]

plot_rectangles(rectangles,showticks=False)
"""

"""
#blocked ring saw cuttable, lambda = 1/12
rectangles = [((0,0),1/2+1/24,1/3+1/24),((1-1/3-1/24,0),1/3+1/24,1/2+1/24),((1-1/2-1/24,1-1/3-1/24),1/2+1/24,1/3+1/24),((0,1-1/2-1/24),1/3+1/24,1/2+1/24)]
plot_rectangles(rectangles,showticks=False)
"""

"""
#example of "allowing corner cuts is more restrictive
rectangles = [
    ((0,0),1,2),
    ((1,0),4,1),
    ((0,2),2,1),
    ((0,3),1,3),
    ((0,6),3,1),
    ((0,7),1,2),
    ((0,9),3,1),
    ((3,1),1,2),
    ((1,3),3,1),
    ((3,5),1,2),
    ((2,7),2,1),
    ((3,8),2,2),
    ((4,3),1,2),
    ((5,2),2,2),
    ((6,4),1,4),
    ((4,6),2,1)]
cuts = [
        ((0,3),5,0),
        ((0,7),5,0),
        ((4,2),0,6)
        ]
plot_rectangles(rectangles,showticks=False,binsize=(7,10),cuts=cuts)
"""

"""
#lambda-saw cutting is less restrictive than guillotine cutting
rectangles=[
    ((0,0),3,3),
    ((3,0),10,2),
    ((0,3),2,10),
    ((3,3),8,8),
    ((11,2),2,11),
    ((2,11),9,2)]
braces = [(0,3),8,"\delta"]
plot_rectangles(rectangles,showticks=False,binsize=(13,13))
"""

"""
#alt_lambda-saw cutting is less restrictive than guillotine cutting
rectangles=[
    ((1,0),10,2),
    ((0,2),2,11),
    ((2,3),9,2),
    ((2,5),8,8),
    ((11,0),2,10),
    ((10,10),3,3)]
plot_rectangles(rectangles,showticks=False,binsize=(13,13))
"""

"""
#alt_lambda-saw cutting is less restrictive than guillotine cutting
rectangles=[
    ((0,0),10,2),
    ((0,2),2,11),
    ((2,3),9,2),
    ((2,5),8,8),
    ((11,3),2,10),
    ((10,0),3,3)]
plot_rectangles(rectangles,showticks=False,binsize=(13,13))
"""

"""

#example lower bound shelf packing for area min
N=7

rectangles = [((0,0),1+1/N,1/N), ((0,1/N),1/N,1)]
               
for i in range(N):
    rectangles.append(((1/N,(1+i)/N),2/3,1/N))
    for j in range(N):
        rectangles.append(((1/N+2/3,(1+i)/N+j/N**2),1/3,1/N**2))

plot_rectangles(rectangles,showticks=False,binsize=(1+1/N,1+1/N))

"""

"""
#example_polygons

example_polygons = [
    [(0, 0), (0, 1), (1, 1)],
    [(2, 2), (2, 3), (3, 3), (3, 2)],
]

visualize_polygons(example_polygons,binsize = (3,3))
"""

"""
#problematic_polygon

problematic_polygon = [[(0,2),(1,0),(10,12),(19,19),(17,18)]]

visualize_polygons(problematic_polygon,binsize = (20,20))
"""

"""
#two polygons

polygons = [[(1,1.5),(2,6.5),(1,4.5),(4,6),(3,5.5)],
            [(2.75,0),(3.75,5),(2.75,3),(5,2)]]

visualize_polygons(polygons,binsize = (7,7))
"""

"""
#three polygons

polygons = [[(1,1.5),(2,6.5),(1,4.5),(4,6),(3,5.5)],
            [(2.75,0),(3.75,5),(2.75,3),(5,2)],
            [(5.25,0.5),(6.25,5.5),(5.25,1.5),(6.75,2.5)]]

spines = [[(1,1.5),(2,6.5)], [(2.75,0),(3.75,5)], [(5.25,0.5),(6.25,5.5)]]

spines2 = [[(0,2),(1,7)], [(6,0),(7,5)]]

middle_line = [[(0,3.5),(7,3.5)]]

visualize_polygons(polygons,binsize = (7,7), lines_black=spines, other_lines = middle_line+spines2)
"""

"""
#example right triangles

def construct_right_triangles(width,height,N,w0=0,h0=0):
    SN = []
    for i in range (1,N+1):
        SN += [[(w0+(N+1-i)/(N+1)*width,h0+i/(N+1)*height),
               (w0+width,h0+i/(N+1)*height),
               (w0+(N+1-i)/(N+1)*width,h0+(i+1)/(N+1)*height)]]
    return SN
"""

"""
width=40
height=20
N=3

example_right_triangles = [[(0,0),(width,0),(0,height)]]

SN1 = construct_right_triangles(width,height,N)

example_right_triangles += SN1

for polygon in SN1:
    SN2 = construct_right_triangles(polygon[1][0]-polygon[0][0],polygon[2][1]-polygon[0][1],N,w0=polygon[0][0],h0=polygon[0][1])
    example_right_triangles += SN2
    for poly2 in SN2:
        SN3 = construct_right_triangles(poly2[1][0]-poly2[0][0],poly2[2][1]-poly2[0][1],N,w0=poly2[0][0],h0=poly2[0][1])
        example_right_triangles += SN3

visualize_polygons(example_right_triangles,binsize=(width,height))
"""

"""
#example
intervals = [(1, 1), (2, 3), (6, 2), (8, 1)]  # Example intervals
visualize_1d(intervals)
"""