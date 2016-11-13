import cv2
import numpy as np
from PIL import Image, ImageDraw

def get_box(size, loc):
  sides = [
  [[loc[i]+dr[i] for i in range (0,3)] for dr in [[0,0,0],[size,0,0],[size,size,0],[0,size,0]]],
  [[loc[i]+dr[i] for i in range (0,3)] for dr in [[0,0,0],[size,0,0],[size,0,size],[0,0,size]]],
  [[loc[i]+dr[i] for i in range (0,3)] for dr in [[0,0,0],[0,0,size],[0,size,size],[0,size,0]]],
  [[loc[i]+dr[i] for i in range (0,3)] for dr in [[0,size,0],[size,size,0],[size,size,size],[0,size,size]]],
  [[loc[i]+dr[i] for i in range (0,3)] for dr in [[size,0,0],[size,size,0],[size,size,size],[size,0,size]]],
  [[loc[i]+dr[i] for i in range (0,3)] for dr in [[0,0,size],[0,size,size],[size,size,size],[size,0,size]]]
  ]

  return [np.array(side) for side in sides]

#Takes in three sizes - one for the width, other for length.
def get_rect(size, loc):
  sides = [
  [[loc[i]+dr[i] for i in range (0,3)] for dr in [[0,0,0],[size[0],0,0],[size[0],size[1],0],[0,size[1],0]]],
  [[loc[i]+dr[i] for i in range (0,3)] for dr in [[0,0,0],[size[0],0,0],[size[0],0,size[2]],[0,0,size[2]]]],
  [[loc[i]+dr[i] for i in range (0,3)] for dr in [[0,0,0],[0,0,size[2]],[0,size[1],size[2]],[0,size[1],0]]],
  [[loc[i]+dr[i] for i in range (0,3)] for dr in [[0,size[1],0],[size[0],size[1],0],[size[0],size[1],size[2]],[0,size[1],size[2]]]],
  [[loc[i]+dr[i] for i in range (0,3)] for dr in [[size[0],0,0],[size[0],size[1],0],[size[0],size[1],size[2]],[size[0],0,size[2]]]],
  [[loc[i]+dr[i] for i in range (0,3)] for dr in [[0,0,size[2]],[0,size[1],size[2]],[size[0],size[1],size[2]],[size[0],0,size[2]]]]
  ]

  return [np.array(side) for side in sides]


def draw_polygons(drawer, polygons):
  w = drawer.im.size[0]
  h = drawer.im.size[1]
  for t in polygons:
    if t[2]:
      t[0] = t[0] + [t[0][0]]
      drawer.line(map(lambda p: (p[0]+w/2,h/2-p[1]),t[0]),fill=t[1],width=4)
    else:
      drawer.polygon(map(lambda p: (p[0]+w/2,h/2-p[1]),t[0]), fill=t[1])

def local_coord(M, points):
  inv = np.linalg.inv(M)
  aug = np.concatenate((points, np.ones((len(points),1))), axis=1)
  return np.dot(aug,inv)[:,:-1]

def project(local_coord, fov):
  return np.apply_along_axis(lambda r: fov*r/-r[-1], 1, local_coord)[:,:-1]

def get_local_proj(M,points,fov):
  local = local_coord(M, points)
  return project(local,fov)


#Box: size
#Rect: l, w, h
def draw_from_file(drawer, filename, fov):
  f = open(filename).readlines()
  camera = np.matrix([map(float, t[1:-1].split(",")) for t in f[0].strip().split(" ")])
  M = np.concatenate((camera, np.array([[0,0,0,1]]).T), axis=1)

  polygons = []
  for line in f[1:]:
    arr = line.strip().split(" ")
    if line[0] == "#":
      continue

    if arr[0] == "box":
      size = float(arr[1])
      loc = map(float,arr[2][1:-1].split(","))
      color = arr[3]
      wireframe = int(arr[4])

      print size
      print loc
      print color
      print wireframe


      sides = get_box(size,loc)
      for side in sides:
        proj = get_local_proj(M,side,fov)
        polygons.append([map(tuple, np.array(proj)),color,wireframe])
    elif arr[0] == "rect":

      size1 = float(arr[1].split(",")[0])
      size2 = float(arr[1].split(",")[1])
      size3 = float(arr[1].split(",")[2])
      loc = map(float,arr[2][1:-1].split(","))
      color = arr[3]
      wireframe = int(arr[4])

      print size
      print loc
      print color
      print wireframe


      sides = get_rect((size1,size2,size3),loc)
      for side in sides:
        proj = get_local_proj(M,side,fov)
        polygons.append([map(tuple, np.array(proj)),color,wireframe])

    else:
      points = np.array([map(float, t[1:-1].split(",")) for t in arr[0:3]])
      color = arr[3]
      wireframe = float(arr[4])

      proj = get_local_proj(M,points,fov)
      polygons.append([map(tuple, np.array(proj)),color,wireframe])


  draw_polygons(drawer, polygons)

#Okay we are going to generalize this function to work for prisms in general, and then cubes will be easily covered as well.
def draw_from_model(drawer, camera, model, fov):
    M = np.concatenate(
        (camera, np.array([[0, 0, 0, 1]]).T), axis=1
    )

    polygons = []
    for box in model:
      #Legacy handler
      try:
        b = len(box[0])
      except:
        box[0] = (box[0],box[0],box[0])
      #Now for the box rendering
      #print box[0]
      size = [float(box[0][0]),float(box[0][1]),float(box[0][2])]
      loc = box[1]
      color = box[2]
      wireframe = float(box[3])

      sides = get_rect((size[0],size[1],size[2]), loc)
      for side in sides:
          proj = get_local_proj(M, side, fov)
          polygons.append([
              map(tuple, np.array(proj)), color, wireframe
          ])
    draw_polygons(drawer, polygons)


if __name__ == '__main__':
    mode = "RGB"
    size = (768, 768)
    color = "#ffffff"
    fov = 200

    im = Image.new(mode, size, color)
    draw = ImageDraw.Draw(im)

    draw_from_file(draw, '../data/room.txt', fov)
    gray = cv2.cvtColor(np.array(im), cv2.COLOR_RGB2GRAY)
    gray = np.float32(gray)
    corners = cv2.goodFeaturesToTrack(gray, 30, 0.01, 10)
    corners = [c[0] for c in np.int0(corners)]
    for c in corners:
        draw.rectangle(
            [c[0]-5, c[1]-5, c[0]+5, c[1]+5],
            fill=(0, 255, 0)
        )
    im.show()
