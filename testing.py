# %%
from plotting import *
from rectangle_packing import *
from polygon_packing import *

import matplotlib.pyplot as plt
from matplotlib.path import Path
import numpy as np

# %%
#nfdh ffdh algo demonstration and differences (for presentation)

rectangles = [(5,3),(3.9,2.7),(2,2.3),(4.1,2),(8,1)]

S_nfdh,h_S_nfdh,rect_map = nfdh(rectangles,stripwidth=8,return_map=True)
rectangles_placed_nfdh = calc_coords_of_shelf_packing(S_nfdh,h_S_nfdh)
#plot_rectangles(rectangles_placed_nfdh, figure_size = (5,5), binsize = (8,8.7))

rectangles_it = [rectangles[:i] for i in range(1,6)]

S_nfdh_it = []
h_S_nfdh_it = []
S_ffdh_it = []
h_S_ffdh_it = []

for i in range(5):
    S_nfdh,h_S_nfdh,rect_map = nfdh(rectangles_it[i],stripwidth=8,return_map=True)
    S_ffdh,h_S_ffdh = ffdh(rectangles_it[i],stripwidth=8)
    S_nfdh_it.append(S_nfdh)
    h_S_nfdh_it.append(h_S_nfdh)
    S_ffdh_it.append(S_ffdh)
    h_S_ffdh_it.append(h_S_ffdh)

rectangles_placed_nfdh_it = [0]*5
rectangles_placed_ffdh_it = [0]*5

for i in range(5):
    rectangles_placed_nfdh_it[i] = calc_coords_of_shelf_packing(S_nfdh_it[i],h_S_nfdh_it[i])
    rectangles_placed_ffdh_it[i] = calc_coords_of_shelf_packing(S_ffdh_it[i],h_S_ffdh_it[i])

for i in range(5):
    plot_rectangles(rectangles_placed_nfdh_it[i], size_scaling = 5, binsize = (8,8.7))
    
for i in range(5):
    plot_rectangles(rectangles_placed_ffdh_it[i], size_scaling = 5, binsize = (8,8.7))
# %%
# Vanishing rectangles (for presentation)
rectangles = [(5,3),(3.9,2.7),(2,2.3),(4.1,2),(8,1)]

rectangles_placement = [((0.1,0.1),5,3),((0.1,3.6),3.9,2.7),((0.1,0.1+3.5+2.7+0.5),2,2.3),((0.1,0.1+3.5+2.7+1+2.3),4.1,2),((0.1,0.1+3.5+2.7+1.5+2.3+2),8,1)]

rectangles_placements = [rectangles_placement[i:] for i in range(len(rectangles_placement))]

lines = [[[(0.1,0.1),5,0], [(5.1,0.1),0,3], [(0.1,3.1),5,0], [(0.1,0.1),0,3]],
         [[(0.1,0.6+3),3.9,0], [(0.1,0.6+3),0,2.7], [(0.1,0.6+3+2.7),3.9,0], [(0.1+3.9,0.6+3),0,2.7]],
         [[(0.1,1.1+3+2.7),2,0], [(0.1,1.1+3+2.7),0,2.3], [(0.1,1.1+3+2.7+2.3),2,0], [(0.1+2,1.1+3+2.7),0,2.3]],
         [[(0.1,1.6+3+2.7+2.3),4.1,0], [(0.1,1.6+3+2.7+2.3),0,2], [(0.1,1.6+3+2.7+2.3+2),4.1,0], [(0.1+4.1,1.6+3+2.7+2.3),0,2]],
         [[(0.1,2.1+3+2.7+2.3+2),8,0], [(0.1,2.1+3+2.7+2.3+2),0,1], [(0.1,2.1+3+2.7+2.3+2+1),8,0], [(0.1+8,2.1+3+2.7+2.3+2),0,1]]]

for i in range(len(rectangles_placements)):
    plot_rectangles(rectangles_placements[i], size_scaling = 5, binsize = (8.2,3.5+2.7+1.5+2.3+2+1+0.2))
    plot_rectangles(rectangles_placements[i], size_scaling = 5, binsize = (8.2,3.5+2.7+1.5+2.3+2+1+0.2), cuts=lines[i])



plot_rectangles([], figure_size = (5,5), binsize = (8.2,3.5+2.7+1.5+2.3+2+1+0.2))

plot_rectangles([], figure_size= (5,5), binsize = (8,8.7))
# %%
# A polygon in its bounding rectangle
N=1

polygon = [(2,0),(5,3),(4,6),(0,5),(0.25,2.25),(4.75,5.25)]
polygons = [polygon]

polygon_packed, parallelogram_packed, width, height = polygon_packing(polygons,c=1,rectangle_strip_packing_algorithm="ffdh")

height=height+4

polygon_packed = [[(polygoni[i][0],polygoni[i][1]+2) for i in range(len(polygoni))] for polygoni in polygon_packed]
parallelogram_packed = [[(polygoni[i][0],polygoni[i][1]+2) for i in range(len(polygoni))] for polygoni in parallelogram_packed]

visualize_polygons(polygon_packed, bounding_parallelograms = parallelogram_packed, figure_size = (200,200), binsize = (width,height))
# %%
#Plot intervals (for presentation):
rectangles = [((0,0),c,d) for ((a,b),c,d) in [((0,0),1,1/20),
                 ((0,1/20),1/2,4/5),((1/2,1/20),1/4,11/16),((3/4,1/20),1/8,5/8),((7/8,1/20),1/8,5/8),
                 ((0,4/5+1/20),9/16,1/2),((9/16,11/16+1/20),1/4,1/2),((7/8,1/20+5/8),1/8,7/8),
                 ((0,1/20+4/5+1/2),3/5,2/5),((0,2/5+1/20+4/5+1/2),2/5,3/5),((3/5,1/20+5/8+7/8),2/5,3/5),((2/5,3/5+1/20+5/8+7/8),3/5,2/5)]]



w= 1/8

for i in range(len(rectangles)):
    rectangles[i] = ((w,0),rectangles[i][1],rectangles[i][2])
    w += rectangles[i][1] + 1/8

plot_rectangles(rectangles,showticks=False,binsize=(w,1))

bp_items = [(rectangles[i][0][0],rectangles[i][1]) for i in range(len(rectangles))]

visualize_1d(bp_items, binsize=w)

bp1 = [(0,1)]
bp2 = [(0,0.6),(0.6,0.4)]
bp3 = [(0,0.6),(0.6,0.4)]
bp4 = [(0,0.5625),(0.5625,0.25),(0.5625+0.25,0.125)]
bp5 = [(0,0.5),(0.5,0.25),(0.75,0.125),(0.875,0.125)]


visualize_1d(bp1, binsize=1, plot_interval=True, remove_frame=True)
visualize_1d(bp2, binsize=1, plot_interval=True, remove_frame=True)
visualize_1d(bp3, binsize=1, plot_interval=True, remove_frame=True)
visualize_1d(bp4, binsize=1, plot_interval=True, remove_frame=True)
visualize_1d(bp5, binsize=1, plot_interval=True, remove_frame=True)
# %%
# Plot some example rectangle packings and polygons (for presentation)

rectangles1 = [((0,0),3/5,2/5),((3/5,0),2/5,3/5),((2/5,3/5),3/5,2/5),((0,2/5),2/5,3/5)]

rectangles2 = [((0,0),1/2,4/5),((1/2,0),1/4,11/16),((3/4,0),1/8,5/8),((7/8,0),1/8,5/8),((0,4/5),1,1/20)]

rectangles3 = [((0,1/4),1/4,1/2),((1/4,0),9/16,1/2),((7/8,0),1/8,7/8)]

plot_rectangles(rectangles1,showticks=False)
plot_rectangles(rectangles2,showticks=False)
plot_rectangles(rectangles3,showticks=False)

strip_packing = [((0,0),1,1/20),
                 ((0,1/20),1/2,4/5),((1/2,1/20),1/4,11/16),((3/4,1/20),1/8,5/8),((7/8,1/20),1/8,5/8),
                 ((0,4/5+1/20),9/16,1/2),((9/16,11/16+1/20),1/4,1/2),((7/8,1/20+5/8),1/8,7/8),
                 ((0,1/20+4/5+1/2),3/5,2/5),((0,2/5+1/20+4/5+1/2),2/5,3/5),((3/5,1/20+5/8+7/8),2/5,3/5),((2/5,3/5+1/20+5/8+7/8),3/5,2/5)]

plot_rectangles(strip_packing,showticks=False,binsize=(1,2.6))

area_min = [((0,0),1/2,4/5),((1/2,0),1/4,11/16),((3/4,0),1/8,5/8),((7/8,0),1/8,5/8),
            ((1,0),2/5,3/5),
            ((0,4/5),2/5,3/5),((2/5,4/5),3/5,2/5),((1,7/8),3/5,2/5),
            ((3/2,0),1/8,7/8),
            ((1/2,11/16),1,1/20),
            ((3/2+1/8,0),9/16,1/2),((3/2+1/8,1/2),1/4,1/2)]

plot_rectangles(area_min,showticks=False,binsize=(3/2+1/8+9/16,7/5))

def random_polygon(rectangle):
    (x, y), w, h = rectangle
    vertices = np.random.rand(4, 2)
    vertices[:, 0] *= w
    vertices[:, 1] *= h
    vertices[:, 0] += x
    vertices[:, 1] += y
    return vertices

# generate a random polygon for each rectangle
polygons_area_min = [random_polygon(rect) for rect in area_min]

# adjust the vertices of each polygon so that it touches all four sides of its rectangle
for i, rect in enumerate(area_min):
    (x, y), w, h = rect
    polygon = polygons_area_min[i]
    # left edge
    polygon[np.argmin(polygon[:, 0]), 0] = x
    # right edge
    polygon[np.argmax(polygon[:, 0]), 0] = x + w
    # bottom edge
    polygon[np.argmin(polygon[:, 1]), 1] = y
    # top edge
    polygon[np.argmax(polygon[:, 1]), 1] = y + h

    
visualize_polygons(polygons_area_min, binsize = (3/2+1/8+9/16,7/5))

polygons_bp1_nrs = [6,4,7,5]
polygons_bp1 = [[(a - area_min[polygons_bp1_nrs[i]][0][0] + rectangles1[i][0][0],b - area_min[polygons_bp1_nrs[i]][0][1] + rectangles1[i][0][1]) for (a,b) in polygons_area_min[polygons_bp1_nrs[i]]] for i in range(len(polygons_bp1_nrs))]
visualize_polygons(polygons_bp1)

polygons_bp2_nrs = [0,1,2,3,9]
polygons_bp2 = [[(a - area_min[polygons_bp2_nrs[i]][0][0] + rectangles2[i][0][0],b - area_min[polygons_bp2_nrs[i]][0][1] + rectangles2[i][0][1]) for (a,b) in polygons_area_min[polygons_bp2_nrs[i]]] for i in range(len(polygons_bp2_nrs))]
visualize_polygons(polygons_bp2)

polygons_bp3_nrs = [11,10,8]
polygons_bp3 = [[(a - area_min[polygons_bp3_nrs[i]][0][0] + rectangles3[i][0][0],b - area_min[polygons_bp3_nrs[i]][0][1] + rectangles3[i][0][1]) for (a,b) in polygons_area_min[polygons_bp3_nrs[i]]] for i in range(len(polygons_bp3_nrs))]
visualize_polygons(polygons_bp3)

#polygons_bp1 = [polygons_area_min[6],polygons_area_min[4],polygons_area_min[7],polygons_area_min[5]]
#polygons_bp2 = [polygons_area_min[0],polygons_area_min[1],polygons_area_min[2],polygons_area_min[3],polygons_area_min[9]]
#polygons_bp3 = [polygons_area_min[8],polygons_area_min[10],polygons_area_min[11]]

polygons_sp_nrs = [9,0,1,2,3,10,11,8,6,4,5,7]
polygons_sp = [[(a - area_min[polygons_sp_nrs[i]][0][0] + strip_packing[i][0][0],b - area_min[polygons_sp_nrs[i]][0][1] + strip_packing[i][0][1]) for (a,b) in polygons_area_min[polygons_sp_nrs[i]]] for i in range(len(polygons_sp_nrs))]
visualize_polygons(polygons_sp, binsize=(1,2.6))

#polygons_sp = [polygons_area_min[9],polygons_area_min[0],polygons_area_min[1],polygons_area_min[2],polygons_area_min[3],polygons_area_min[10],polygons_area_min[11],polygons_area_min[8],polygons_area_min[6],polygons_area_min[4],polygons_area_min[5],polygons_area_min[7]]
# %%
# A demonstration of the algorithm

N = 10
c = 4
d = 2#horizontal dist btwn polys
h = 1.5 #vertical dist btwn polys

#polygons:

polygons1 = [[(random.random(),random.random()) for j in range(random.randint(3,7))] for i in range(N)]
polygons2 = [[(random.random(),random.random()) for j in range(random.randint(3,7))] for i in range(N)]

polygons1 = [left_bottom_adjust_polygon(polygon) for polygon in polygons1]
polygons2 = [left_bottom_adjust_polygon(polygon) for polygon in polygons2]

#good example polygons1 = [[(0.0682616260192791, 0.0), (0.6277010177290963, 0.9113619559391828), (0.0, 0.5186622530597763)], [(0.31365183931877605, 0.0), (0.0, 0.13755604127842713), (0.4345781774871207, 0.6789356276185061), (0.2932220503089378, 0.5328343627807964)], [(0.4304040697006484, 0.9035177441462792), (0.0, 0.6842913404074804), (0.36821618336425355, 0.7844626606389811), (0.33025738481877154, 0.6861965543765075), (0.04695426755347554, 0.6065901452892588), (0.7382130183057866, 0.0), (0.07451833184468415, 0.698209296262137)], [(0.1591510292470555, 0.7369286401906034), (0.5648831434019963, 0.2076311194416236), (0.0, 0.0), (0.8374107516096795, 0.5902291788142738), (0.5547412046518954, 0.5178149505497495)], [(0.09382095765239518, 0.30858399403260706), (0.8684664944675061, 0.44661384537615545), (0.0, 0.2816229452220702), (0.6432435853785264, 0.0), (0.6999857975659337, 0.2530812014794719), (0.33121442113011723, 0.5038097027232603)], [(0.0, 0.0), (0.34959373822976325, 0.228641625729749), (0.3342539435767541, 0.9026541031996305)], [(0.4923500186379327, 0.0), (0.12888526327484495, 0.09285328421892025), (0.7909534559575293, 0.6879554168669371), (0.7744240295903106, 0.33176308362646023), (0.7385389149642635, 0.6571699947485697), (0.0, 0.3021047567338492), (0.1478091117649497, 0.6775611913348609)], [(0.18693447006173003, 0.7440076701816458), (0.0717862016710481, 0.0), (0.13981109722077312, 0.9502532352219105), (0.0, 0.20738294031684212)], [(0.4243985342069615, 0.5764724396845555), (0.0, 0.0), (0.3739498719842259, 0.7004372329696725), (0.5778791137618707, 0.06490617058408499), (0.4562831140341279, 0.5979803224391623), (0.8546518722022105, 0.6051916548428075)], [(0.6669224141006957, 0.06630073834073136), (0.8713198477304863, 0.7482317245585118), (0.3080625265299679, 0.0), (0.6822692241346293, 0.31892445380796297), (0.0, 0.547050294127981), (0.8149816069169575, 0.03526804151026108)]]
#good example polygons2 = [[(0.0, 0.469534065513757), (0.6028535626240914, 0.0), (0.8743577170964869, 0.4684229597540974), (0.3946744525817216, 0.24924289945858114)], [(0.0, 0.8928324586985776), (0.573913706392391, 0.0014212775183308768), (0.46177090741086535, 0.0), (0.05465214533537943, 0.5365486686167388), (0.02242864381059162, 0.00132505838665109)], [(0.00937559839224078, 0.36287713596810967), (0.0, 0.14610423760240343), (0.9800737755839569, 0.5728634368184138), (0.03447457646494945, 0.40020438074802056), (0.04268670759596238, 0.0)], [(0.5376982009075879, 0.2939500680460605), (0.15480245559256667, 0.4478476926061826), (0.0, 0.0)], [(0.7542444110778797, 0.3092269342439099), (0.3279788134414977, 0.0), (0.0, 0.13726294803021932), (0.6537952249269661, 0.2785252211238286)], [(0.6557031184443545, 0.7733299634400512), (0.5599189280429401, 0.06827998186208462), (0.13380258143277712, 0.8466396646580018), (7.427861169384542e-05, 0.1767135471855238), (0.8457109023759679, 0.0), (0.5283763973989717, 0.17562202142535), (0.0, 0.07980705525829201)], [(0.0, 0.0), (0.4930194727852001, 0.3094412813661007), (0.34545673519218134, 0.5244323328983207), (0.5203464636287558, 0.8588137888716237), (0.16442378832564208, 0.10554127260248025)], [(0.04594948895460815, 0.0), (0.3493864929594467, 0.09157963314342188), (0.027848364793583213, 0.4593026570811932), (0.0, 0.8871004256697629), (0.043594528384697795, 0.6614075476251858), (0.6924468849417806, 0.43389611808288053)], [(0.8140925525345445, 0.0), (0.5320630038017278, 0.10031926347994624), (0.7443497360508512, 0.03154378145185588), (0.36820751279135744, 0.00938910128001924), (0.06470465123711155, 0.588798264958425), (0.0, 0.41614828392595404)], [(0.4521916604239721, 0.558731644726873), (0.0, 0.10149704518404801), (0.19862485280604547, 0.8678508296430112), (0.16156400520656777, 0.0)]]

polygons = polygons1 + polygons2

polygons_to_visualize1 = [[(a+i*d+1,b+1*h) for (a,b) in polygons1[i]] for i in range(len(polygons1))]
polygons_to_visualize2 = [[(a+i*d+1,b) for (a,b) in polygons2[i]] for i in range(len(polygons2))]

polygons_to_visualize = polygons_to_visualize1 + polygons_to_visualize2

visualize_polygons(polygons_to_visualize,binsize=(1+(N-1)*d+2,1+h))

#parallelograms:

parallelograms1 = []
parallelograms2 = []

for polygon in polygons1:
    parallelogram, delta_i = compute_bounding_parallelogram(polygon)
    parallelograms1 += [parallelogram]

for polygon in polygons2:
    parallelogram, delta_i = compute_bounding_parallelogram(polygon)
    parallelograms2 += [parallelogram]

parallelograms_to_visualize1 = []
parallelograms_to_visualize2 = []

for i in range(len(parallelograms1)):
    x_0 = i*d+1
    y_0 = 1*h
    base = parallelograms1[i][0]
    height = parallelograms1[i][1]
    wside = parallelograms1[i][2]
    parallelograms_to_visualize1 += [[(x_0,y_0),(x_0+base,y_0),(x_0+wside,y_0+height),(x_0+wside+base,y_0+height)]]
    
for i in range(len(parallelograms2)):
    x_0 = i*d+1
    y_0 = 0
    base = parallelograms2[i][0]
    height = parallelograms2[i][1]
    wside = parallelograms2[i][2]
    parallelograms_to_visualize2 += [[(x_0,y_0),(x_0+base,y_0),(x_0+wside,y_0+height),(x_0+wside+base,y_0+height)]]

parallelograms_to_visualize = parallelograms_to_visualize1 + parallelograms_to_visualize2

visualize_polygons([],bounding_parallelograms=parallelograms_to_visualize,binsize=(1+(N-1)*d+2,1+h))

#rectangles:
    
rectangles_to_visualize1 = []
rectangles_to_visualize2 = []


for i in range(len(parallelograms1)):
    rectangles_to_visualize1 += [((i*d+1,1*h),parallelograms1[i][0],parallelograms1[i][1])]

for i in range(len(parallelograms2)):
    rectangles_to_visualize2 += [((i*d+1,0),parallelograms2[i][0],parallelograms2[i][1])]

rectangles_to_visualize = rectangles_to_visualize1 + rectangles_to_visualize2

plot_rectangles(rectangles_to_visualize,binsize=(1+(N-1)*d+2,1+h))

#packed_instances


polygons_placement, parallelograms_placement, W, H, rect_shelves, rect_height_shelves = polygon_packing(polygons,return_rectangles_packing=True,c=c)

W = float(W)
H = float(H)

rectangles_placement1 = calc_coords_of_shelf_packing(rect_shelves, rect_height_shelves)
rectangles_placement = [((a0+W/(c+2),a1),a2,a3) for ((a0,a1),a2,a3) in rectangles_placement1] #adjust horizontal loc of pacing

plot_rectangles(rectangles_placement,binsize=(W,H))
visualize_polygons([],bounding_parallelograms=parallelograms_placement,binsize=(W,H))
visualize_polygons(polygons_placement, bounding_parallelograms = parallelograms_placement, binsize = (W,H))

#doing it again, but packing into 4 rows
N = 10
c = 4
d = 1.5#horizontal dist btwn polys
h = 1.2 #vertical dist btwn polys

#good examples:
polygons1 = [[(0.0682616260192791, 0.0), (0.6277010177290963, 0.9113619559391828), (0.0, 0.5186622530597763)], [(0.31365183931877605, 0.0), (0.0, 0.13755604127842713), (0.4345781774871207, 0.6789356276185061), (0.2932220503089378, 0.5328343627807964)], [(0.4304040697006484, 0.9035177441462792), (0.0, 0.6842913404074804), (0.36821618336425355, 0.7844626606389811), (0.33025738481877154, 0.6861965543765075), (0.04695426755347554, 0.6065901452892588), (0.7382130183057866, 0.0), (0.07451833184468415, 0.698209296262137)], [(0.1591510292470555, 0.7369286401906034), (0.5648831434019963, 0.2076311194416236), (0.0, 0.0), (0.8374107516096795, 0.5902291788142738), (0.5547412046518954, 0.5178149505497495)], [(0.09382095765239518, 0.30858399403260706), (0.8684664944675061, 0.44661384537615545), (0.0, 0.2816229452220702), (0.6432435853785264, 0.0), (0.6999857975659337, 0.2530812014794719), (0.33121442113011723, 0.5038097027232603)], [(0.0, 0.0), (0.34959373822976325, 0.228641625729749), (0.3342539435767541, 0.9026541031996305)], [(0.4923500186379327, 0.0), (0.12888526327484495, 0.09285328421892025), (0.7909534559575293, 0.6879554168669371), (0.7744240295903106, 0.33176308362646023), (0.7385389149642635, 0.6571699947485697), (0.0, 0.3021047567338492), (0.1478091117649497, 0.6775611913348609)], [(0.18693447006173003, 0.7440076701816458), (0.0717862016710481, 0.0), (0.13981109722077312, 0.9502532352219105), (0.0, 0.20738294031684212)], [(0.4243985342069615, 0.5764724396845555), (0.0, 0.0), (0.3739498719842259, 0.7004372329696725), (0.5778791137618707, 0.06490617058408499), (0.4562831140341279, 0.5979803224391623), (0.8546518722022105, 0.6051916548428075)], [(0.6669224141006957, 0.06630073834073136), (0.8713198477304863, 0.7482317245585118), (0.3080625265299679, 0.0), (0.6822692241346293, 0.31892445380796297), (0.0, 0.547050294127981), (0.8149816069169575, 0.03526804151026108)]]
polygons3 = [[(0.0, 0.469534065513757), (0.6028535626240914, 0.0), (0.8743577170964869, 0.4684229597540974), (0.3946744525817216, 0.24924289945858114)], [(0.0, 0.8928324586985776), (0.573913706392391, 0.0014212775183308768), (0.46177090741086535, 0.0), (0.05465214533537943, 0.5365486686167388), (0.02242864381059162, 0.00132505838665109)], [(0.00937559839224078, 0.36287713596810967), (0.0, 0.14610423760240343), (0.9800737755839569, 0.5728634368184138), (0.03447457646494945, 0.40020438074802056), (0.04268670759596238, 0.0)], [(0.5376982009075879, 0.2939500680460605), (0.15480245559256667, 0.4478476926061826), (0.0, 0.0)], [(0.7542444110778797, 0.3092269342439099), (0.3279788134414977, 0.0), (0.0, 0.13726294803021932), (0.6537952249269661, 0.2785252211238286)], [(0.6557031184443545, 0.7733299634400512), (0.5599189280429401, 0.06827998186208462), (0.13380258143277712, 0.8466396646580018), (7.427861169384542e-05, 0.1767135471855238), (0.8457109023759679, 0.0), (0.5283763973989717, 0.17562202142535), (0.0, 0.07980705525829201)], [(0.0, 0.0), (0.4930194727852001, 0.3094412813661007), (0.34545673519218134, 0.5244323328983207), (0.5203464636287558, 0.8588137888716237), (0.16442378832564208, 0.10554127260248025)], [(0.04594948895460815, 0.0), (0.3493864929594467, 0.09157963314342188), (0.027848364793583213, 0.4593026570811932), (0.0, 0.8871004256697629), (0.043594528384697795, 0.6614075476251858), (0.6924468849417806, 0.43389611808288053)], [(0.8140925525345445, 0.0), (0.5320630038017278, 0.10031926347994624), (0.7443497360508512, 0.03154378145185588), (0.36820751279135744, 0.00938910128001924), (0.06470465123711155, 0.588798264958425), (0.0, 0.41614828392595404)], [(0.4521916604239721, 0.558731644726873), (0.0, 0.10149704518404801), (0.19862485280604547, 0.8678508296430112), (0.16156400520656777, 0.0)]]

polygons2 = polygons1[5:]
polygons1 = polygons1[:5]
polygons4 = polygons3[5:]
polygons3 = polygons3[:5]

polygons = polygons1 + polygons2 + polygons3 + polygons4

polygons_to_visualize1 = [[(a+i*d+1,b) for (a,b) in polygons1[i]] for i in range(len(polygons1))]
polygons_to_visualize2 = [[(a+i*d+1,b+1*h) for (a,b) in polygons2[i]] for i in range(len(polygons2))]
polygons_to_visualize3 = [[(a+i*d+1,b+2*h) for (a,b) in polygons3[i]] for i in range(len(polygons3))]
polygons_to_visualize4 = [[(a+i*d+1,b+3*h) for (a,b) in polygons4[i]] for i in range(len(polygons4))]



polygons_to_visualize = polygons_to_visualize1 + polygons_to_visualize2 + polygons_to_visualize3 + polygons_to_visualize4

visualize_polygons(polygons_to_visualize,binsize=(1+(N/2-1)*d+2,1+3*h))

visualize_polygons([],binsize=(1+(N/2-1)*d+2,1+3*h))

#parallelograms:

parallelograms1 = []
parallelograms2 = []
parallelograms3 = []
parallelograms4 = []

for polygon in polygons1:
    parallelogram, delta_i = compute_bounding_parallelogram(polygon)
    parallelograms1 += [parallelogram]

for polygon in polygons2:
    parallelogram, delta_i = compute_bounding_parallelogram(polygon)
    parallelograms2 += [parallelogram]
    
for polygon in polygons3:
    parallelogram, delta_i = compute_bounding_parallelogram(polygon)
    parallelograms3 += [parallelogram]
    
for polygon in polygons4:
    parallelogram, delta_i = compute_bounding_parallelogram(polygon)
    parallelograms4 += [parallelogram]

parallelograms_to_visualize1 = []
parallelograms_to_visualize2 = []
parallelograms_to_visualize3 = []
parallelograms_to_visualize4 = []

for i in range(len(parallelograms1)):
    x_0 = i*d+1
    y_0 = 0
    base = parallelograms1[i][0]
    height = parallelograms1[i][1]
    wside = parallelograms1[i][2]
    parallelograms_to_visualize1 += [[(x_0,y_0),(x_0+base,y_0),(x_0+wside,y_0+height),(x_0+wside+base,y_0+height)]]
    
for i in range(len(parallelograms2)):
    x_0 = i*d+1
    y_0 = 1*h
    base = parallelograms2[i][0]
    height = parallelograms2[i][1]
    wside = parallelograms2[i][2]
    parallelograms_to_visualize2 += [[(x_0,y_0),(x_0+base,y_0),(x_0+wside,y_0+height),(x_0+wside+base,y_0+height)]]

for i in range(len(parallelograms3)):
    x_0 = i*d+1
    y_0 = 2*h
    base = parallelograms3[i][0]
    height = parallelograms3[i][1]
    wside = parallelograms3[i][2]
    parallelograms_to_visualize3 += [[(x_0,y_0),(x_0+base,y_0),(x_0+wside,y_0+height),(x_0+wside+base,y_0+height)]]

for i in range(len(parallelograms4)):
    x_0 = i*d+1
    y_0 = 3*h
    base = parallelograms4[i][0]
    height = parallelograms4[i][1]
    wside = parallelograms4[i][2]
    parallelograms_to_visualize4 += [[(x_0,y_0),(x_0+base,y_0),(x_0+wside,y_0+height),(x_0+wside+base,y_0+height)]]


parallelograms_to_visualize = parallelograms_to_visualize1 + parallelograms_to_visualize2 + parallelograms_to_visualize3 + parallelograms_to_visualize4

visualize_polygons([],bounding_parallelograms=parallelograms_to_visualize,binsize=(1+(N/2-1)*d+2,1+3*h))


#rectangles:
    
rectangles_to_visualize1 = []
rectangles_to_visualize2 = []
rectangles_to_visualize3 = []
rectangles_to_visualize4 = []

for i in range(len(parallelograms1)):
    rectangles_to_visualize1 += [((i*d+1,0),parallelograms1[i][0],parallelograms1[i][1])]

for i in range(len(parallelograms2)):
    rectangles_to_visualize2 += [((i*d+1,1*h),parallelograms2[i][0],parallelograms2[i][1])]

for i in range(len(parallelograms2)):
    rectangles_to_visualize3 += [((i*d+1,2*h),parallelograms3[i][0],parallelograms3[i][1])]

for i in range(len(parallelograms2)):
    rectangles_to_visualize4 += [((i*d+1,3*h),parallelograms4[i][0],parallelograms4[i][1])]

rectangles_to_visualize = rectangles_to_visualize1 + rectangles_to_visualize2 + rectangles_to_visualize3 + rectangles_to_visualize4

plot_rectangles(rectangles_to_visualize,binsize=(1+(N/2-1)*d+2,1+3*h))

#packed_instances


polygons_placement, parallelograms_placement, W, H, rect_shelves, rect_height_shelves = polygon_packing(polygons,return_rectangles_packing=True,c=c)

W = float(W)
H = float(H)

rectangles_placement1 = calc_coords_of_shelf_packing(rect_shelves, rect_height_shelves)
rectangles_placement = [((a0+W/(c+2),a1),a2,a3) for ((a0,a1),a2,a3) in rectangles_placement1] #adjust horizontal loc of pacing

plot_rectangles(rectangles_placement,binsize=(W,H))
visualize_polygons([],bounding_parallelograms=parallelograms_placement,binsize=(W,H))
visualize_polygons(polygons_placement, bounding_parallelograms = parallelograms_placement, binsize = (W,H))

visualize_polygons([],binsize=(W,H))
# %%
a_polygon_to_visualize = [[(1,1),(3,1),(2,3),(4,3)]]
visualize_polygons([],bounding_parallelograms=a_polygon_to_visualize,binsize=(5,4))

a_rect_to_visualize = [((1,1),2,2)]
plot_rectangles(a_rect_to_visualize, binsize=(4,4))
# %%
# Problematic polygons for bin packing problem
N = 10

karate_guys = [[(i*0.3/(N),0.3-i*0.3/(N)),((i+1)*0.3/(N),0.3-(i+1)*0.3/(N)),(1-0.3+i*0.3/(N),1-i*0.3/(N))] for i in range(N)]

fan_guys = [[(0,0),(0.7+i/N,1),(0.7+(i+1)/N,1)] for i in range(N)]

visualize_polygons(karate_guys)
visualize_polygons(fan_guys)
# %%
# Our algorithm on a random testset of 6-gons
N=200
random_polygons = [[(0,random.random()),(random.random(),0),(random.random(),random.random()),(random.random(),random.random()),(random.random(),random.random()),(random.random(),random.random())] for i in range(N)]

packed_random_polygons, packed_random_polygons_bounding_parallelograms, width, height = polygon_packing(random_polygons,c=7)

visualize_polygons(packed_random_polygons, bounding_parallelograms = packed_random_polygons_bounding_parallelograms, figure_size = (20,20), binsize = (width,height))
# %%
# Our algorithm on an instance created with exponential distributions
N=300
random_polygons = [[(0,np.random.exponential()),(np.random.exponential(),0),(np.random.exponential(),np.random.exponential()),(np.random.exponential(),np.random.exponential()),(np.random.exponential(),np.random.exponential()),(np.random.exponential(),np.random.exponential())] for i in range(N)]

packed_random_polygons, packed_random_polygons_bounding_parallelograms, width, height = polygon_packing(random_polygons,c=7)

visualize_polygons(packed_random_polygons, bounding_parallelograms = packed_random_polygons_bounding_parallelograms, figure_size = (60,60), binsize = (width,height))
# %%
# Our algorithm on instance with random fractions (nominator and denominator uniformly random integers in [1,100])
N=300
random_polygons = [[(0,Fraction(random.randint(1,100),100*random.randint(1,10))),(Fraction(random.randint(1,100),100*random.randint(1,10)),0),(Fraction(random.randint(1,100),100*random.randint(1,10)),Fraction(random.randint(1,100),100*random.randint(1,10))),(Fraction(random.randint(1,100),100*random.randint(1,10)),Fraction(random.randint(1,100),100*random.randint(1,10))),(Fraction(random.randint(1,100),100*random.randint(1,10)),Fraction(random.randint(1,100),100*random.randint(1,10))),(Fraction(random.randint(1,100),100*random.randint(1,10)),Fraction(random.randint(1,100),100*random.randint(1,10)))] for i in range(N)]

packed_random_polygons, packed_random_polygons_bounding_parallelograms, width, height = polygon_packing(random_polygons,c=7)

width = float(width)
height = float(height)

visualize_polygons(packed_random_polygons, bounding_parallelograms = packed_random_polygons_bounding_parallelograms, figure_size = (200,200), binsize = (width,height))
# %%
# Our algorithm on instance with random fractions (nominator and denominator uniformly random integers in [1,100]), bottom-left adjust them afterwards; visualized shelves
N=300
random_polygons = [[(Fraction(random.randint(1,100),100*random.randint(1,10)),Fraction(random.randint(1,100),100*random.randint(1,10))),(Fraction(random.randint(1,100),100*random.randint(1,10)),Fraction(random.randint(1,100),100*random.randint(1,10))),(Fraction(random.randint(1,100),100*random.randint(1,10)),Fraction(random.randint(1,100),100*random.randint(1,10))),(Fraction(random.randint(1,100),100*random.randint(1,10)),Fraction(random.randint(1,100),100*random.randint(1,10))),(Fraction(random.randint(1,100),100*random.randint(1,10)),Fraction(random.randint(1,100),100*random.randint(1,10))),(Fraction(random.randint(1,100),100*random.randint(1,10)),Fraction(random.randint(1,100),100*random.randint(1,10)))] for i in range(N)]

random_polygons = [left_bottom_adjust_polygon(polygon) for polygon in random_polygons]

packed_random_polygons, packed_random_polygons_bounding_parallelograms, width, height, shelf_lines = polygon_packing(random_polygons,c=7,rectangle_strip_packing_algorithm="ffdh",return_shelf_lines=True)

width = float(width)
height = float(height)

visualize_polygons(packed_random_polygons, bounding_parallelograms = packed_random_polygons_bounding_parallelograms, figure_size = (200,200), binsize = (width,height),lines=shelf_lines)
# %%
# Our algorithms, uniformly random generated polygons
N=300
c=15

random_polygons = [[(random.random(),random.random()) for j in range(random.randint(3,7))] for i in range(N)]

random_polygons = [left_bottom_adjust_polygon(polygon) for polygon in random_polygons]

packed_random_polygons, packed_random_polygons_bounding_parallelograms, width, height, shelf_lines = polygon_packing(random_polygons,c=c,rectangle_strip_packing_algorithm="ffdh",return_shelf_lines=True)

width = float(width)
height = float(height)

visualize_polygons(packed_random_polygons, bounding_parallelograms = packed_random_polygons_bounding_parallelograms, figure_size = (200,200), binsize = (width,height))
#------------
# %%
# Demo of NFDH, FFDH
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
S_ffdh,h_S_ffdh = ffdh(rectangles,stripwidth=4)

rectangles_placed_nfdh = calc_coords_of_shelf_packing(S_nfdh,h_S_nfdh)
rectangles_placed_ffdh = calc_coords_of_shelf_packing(S_nfdh,h_S_nfdh)

plot_rectangles(rectangles_placed_nfdh, binsize=(4,h_S_nfdh))
plot_rectangles(rectangles_placed_ffdh, binsize=(4,h_S_ffdh))
#--------------
# %%
"""
#move_by_lambda
rectangles = [((0,0),6,4),((7,1),4,6),((5,7),6,4),((1,5),4,6),((5,5),2,2)]
pointed_rect = [((1,1),6,4)]
arrows = [(4,3,-1,-1)]

plot_rectangles(rectangles,pointed_rect=pointed_rect,arrows=arrows,showticks=False,binsize=(11,11))
"""
# %%
"""
#non-guillotinable
rectangles = [((0,0),3/5,2/5),((3/5,0),2/5,3/5),((2/5,3/5),3/5,2/5),((0,2/5),2/5,3/5)]

plot_rectangles(rectangles,showticks=False)
"""
# %%
"""
#example 2-stage packing

rectangles = [((0,0),3/5,1/4),((3/5,0),1/3,1/4),((0,1/4),1,1/4),((0,1/2),1/3,1/2),((1/2,0.6),1/4,1/2),((3/4,1/2),1/4,1/2)]

plot_rectangles(rectangles,showticks=False)
"""
# %%
"""
#blocked ring saw cuttable, lambda = 1/12
rectangles = [((0,0),1/2+1/24,1/3+1/24),((1-1/3-1/24,0),1/3+1/24,1/2+1/24),((1-1/2-1/24,1-1/3-1/24),1/2+1/24,1/3+1/24),((0,1-1/2-1/24),1/3+1/24,1/2+1/24)]
plot_rectangles(rectangles,showticks=False)
"""
# %%
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
# %%
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
# %%
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
# %%
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
# %%
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
# %%
"""
#example_polygons

example_polygons = [
    [(0, 0), (0, 1), (1, 1)],
    [(2, 2), (2, 3), (3, 3), (3, 2)],
]

visualize_polygons(example_polygons,binsize = (3,3))
"""
# %%
"""
#problematic_polygon

problematic_polygon = [[(0,2),(1,0),(10,12),(19,19),(17,18)]]

visualize_polygons(problematic_polygon,binsize = (20,20))
"""
# %%
"""
#two polygons

polygons = [[(1,1.5),(2,6.5),(1,4.5),(4,6),(3,5.5)],
            [(2.75,0),(3.75,5),(2.75,3),(5,2)]]

visualize_polygons(polygons,binsize = (7,7))
"""
# %%
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
# %%
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
# %%
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
# %%
"""
#example
intervals = [(1, 1), (2, 3), (6, 2), (8, 1)]  # Example intervals
visualize_1d(intervals)
"""