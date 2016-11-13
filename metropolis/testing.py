from PIL import Image, ImageEnhance

def filter(pixel):
  r = pixel[0]
  g = pixel[1]
  b = pixel[2]


  if min(r,g,b) > 100:
    return (255,255,255) #white
  elif r > 100:
    return (255,0,0)
  else:
    return p


im = Image.open("blue.JPG")
im.show()

col = ImageEnhance.Color(im)
im = col.enhance(3)

im = im.resize((400,300))

for i in range (0,400):
  for j in range(0,300):
    p = im.getpixel((i,j))
    im.putpixel((i,j), filter(p))

im.save('test-real.bmp')