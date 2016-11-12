from PIL import Image,ImageDraw
import numpy as np

def draw_box(drawer, size, loc, color):
  vertices = [map(lambda i:loc[i]+dr[i],[0,1,2]) for dr in 
  [(0,0,0),(0,0,size),(0,size,0),(size,0,0),(0,size,size),(size,0,size),(size,size,0),(size,size,size)]]

  sides = [
  [[(0,0,0),(0,0,size),(0,size,size),(0,size,0)],color,0],
  [[(0,0,0),(size,0,0),(size,size,0),(0,size,0)],color,0]]

  draw_polygons(drawer,sides)

def draw_polygons(drawer, polygons):
  w = drawer.im.size[0]
  h = drawer.im.size[1]
  for t in polygons:
    if t[2]:
      drawer.polygon(map(lambda p: (p[0]+w/2,h/2-p[1]),t[0]),outline=t[1])
    else:
      drawer.polygon(map(lambda p: (p[0]+w/2,h/2-p[1]),t[0]),fill=t[1])

def local_coord(M, points):
  inv = np.linalg.inv(M)
  aug = np.concatenate((points, np.ones((len(points),1))), axis=1)
  return np.dot(aug,inv)[:,:-1]

def project(local_coord, fov):
  return np.apply_along_axis(lambda r: fov*r/-r[-1], 1, local_coord)[:,:-1]


def draw_from_file(drawer, filename):
  triangles = []
  f = open(filename).readlines()
  camera = np.matrix([map(int, t[1:-1].split(",")) for t in f[0].strip().split(" ")])
  M = np.concatenate((camera, np.array([[0,0,0,1]]).T), axis=1)
  print M

  print 'Triangles'

  triangles = []
  for line in f[1:]:
    arr = line.strip().split(" ")
    points = np.array([map(int, t[1:-1].split(",")) for t in arr[0:3]])
    color = arr[3]
    wireframe = int(arr[4])

    local = local_coord(M, points)
    proj = project(local,200)
    print proj
    triangles.append([map(tuple, np.array(proj)),color,wireframe])

  draw_polygons(drawer, triangles)



#MAIN
#######################################33
mode = "RGB"
size = (512,512)
color = "#ffffff"

im = Image.new(mode,size,color)
draw = ImageDraw.Draw(im)

draw_from_file(draw,"triangles.txt")

draw_box(draw, 10, (0,0,0), "#333333")
im.show()