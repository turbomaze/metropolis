from PIL import Image,ImageDraw
import numpy as np

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

def draw_from_file(drawer, filename, fov):
  f = open(filename).readlines()
  camera = np.matrix([map(float, t[1:-1].split(",")) for t in f[0].strip().split(" ")])
  M = np.concatenate((camera, np.array([[0,0,0,1]]).T), axis=1)

  polygons = []
  for line in f[1:]:
    arr = line.strip().split(" ")

    if arr[0] == "box":
      size = float(arr[1])
      loc = map(float,arr[2][1:-1].split(","))
      color = arr[3]
      wireframe = int(arr[4])

      sides = get_box(size,loc)
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

def draw_from_model(drawer, camera, model, fov):
    M = np.concatenate(
        (camera, np.array([[0, 0, 0, 1]]).T), axis=1
    )

    polygons = []
    for box in model:
        size = float(box[0])
        loc = box[1]
        color = box[2]
        wireframe = float(box[3])

        sides = get_box(size, loc)
        for side in sides:
            proj = get_local_proj(M, side, fov)
            polygons.append([
                map(tuple, np.array(proj)), color, wireframe
            ])
    draw_polygons(drawer, polygons)


if __name__ == '__main__':
    mode = "RGB"
    size = (512, 512)
    color = "#ffffff"
    fov = 200

    im = Image.new(mode, size, color)
    draw = ImageDraw.Draw(im)

    draw_from_file(draw, '../data/room.txt', fov)
    im.show()
