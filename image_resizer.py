import PIL
import os
from PIL import Image

basewidth = 300
img = Image.open(os.path.join('res', 'letterX3.png'))
wpercent = (basewidth / float(img.size[0]))
hsize = int((float(img.size[1]) * float(wpercent)))
img = img.resize((basewidth, hsize), PIL.Image.ANTIALIAS)
img.save('letterX2.png')