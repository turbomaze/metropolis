from PIL import Image, ImageEnhance

def clean(im):
  if im.width < im.height:
    im = im.rotate(-90)
  col = ImageEnhance.Color(im)
  im = col.enhance(3)

  im = im.resize((400,300))

  for i in range (0,400):
    for j in range(0,300):
      p = im.getpixel((i,j))
      im.putpixel((i,j), collapse(p))

  return im


def collapse(pixel):
  r = pixel[0]
  g = pixel[1]
  b = pixel[2]


  if max(r,b,g) < 120:
    return (0,0,0) #black
  elif r > 100 and max(g,b) < 80:
    return (255,0,0) #red
  else:
    return (255,255,255) #white