from PIL import Image,ImageDraw
import utils


mode = "RGB"
size = (200,200)
color = "#ffffff"

im = Image.new(mode,size,color)
draw = ImageDraw.Draw(im)

utils.draw_from_file(draw,"triangles.txt")

im.show()