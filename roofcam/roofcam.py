import os, fnmatch, math
from PIL import Image, ImageFilter, ImageStat, ImageOps, ImageEnhance
import numpy


def brightness(im_file):
    im = im_file.convert('L')
    stat = ImageStat.Stat(im)
    return stat.mean[0]


def brightness2(im_file):
    im = im_file.convert('L')
    stat = ImageStat.Stat(im)
    return stat.rms[0]


def brightness3(im_file):
    stat = ImageStat.Stat(im_file)
    r, g, b = stat.mean
    return math.sqrt(0.241 * (r ** 2) + 0.691 * (g ** 2) + 0.068 * (b ** 2))


def is_day(image):
    bright = brightness(image)
    return bright > 100


def get_water_region(image):
    box = (400, 320, 640, 360)  # Left, Top, Right, Bottom
    return image.crop(box)


# region.show()

# dir = os.path.abspath(".")
# for file in os.listdir(dir):
#     if fnmatch.fnmatch(file, "*snapshot*"):
#         filename = os.path.join(dir, file)
#         im = Image.open(filename)
#         region = get_water_region(im)
#         bright = brightness3(region)
#         if is_day(bright):
#             print file, "->", bright



dir = os.path.abspath(".")
files = fnmatch.filter(os.listdir(dir), "*snapshot*")

# water
# files = ["snapshot-2017-02-17_09-10-05.jpg", "snapshot-2017-02-19_12-00-05.jpg", "snapshot-2017-02-18_09-10-05.jpg"]
files = ["snapshot-2017-02-18_15-00-05.jpg", "snapshot-2017-02-18_15-10-05.jpg", "snapshot-2017-02-18_13-50-05.jpg",
         "snapshot-2017-02-18_10-00-05.jpg"]
for file in files:
    im = Image.open(file)
    region = get_water_region(im)
    if not is_day(region):
        print file, "-> NIGHT"
        continue
    # region.show()
    region = ImageOps.invert(region)
    region = ImageEnhance.Contrast(region).enhance(2)
    region = region.convert('L')
    region = region.point(lambda x: 0 if x < 175 else 255, '1')

    black = 0
    white = 0
    for pixel in region.getdata():
        if pixel == 0:
            black += 1
        else:
            white += 1
    # image = image.convert('1')
    region.show()
    result = "WATER" if white > 850 else "DRY"

    print file, "->", "black=", black, "white=", white, "==>", result
    # print file, "->", brightness(region)
    # print file, "->", brightness2(region)
    # print file, "->", brightness3(region)
