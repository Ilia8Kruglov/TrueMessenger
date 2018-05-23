from os import listdir
from os.path import abspath, join, isdir, isfile
from PIL import Image

size = 32, 32

file = '/Users/semeandr/PycharmProjects/Messanger/ClientRepo/ui/images/icons/list_default_image.png'
im = Image.open(file)
out = im.resize(size, Image.ANTIALIAS)
out.save(file)
print("Saving ", file)

