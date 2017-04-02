from PIL import Image, ImageStat, ImageOps, ImageEnhance


def brightness(im_file):
    im = im_file.convert('L')
    stat = ImageStat.Stat(im)
    return stat.mean[0]


def is_day(image):
    bright = brightness(image)
    return bright > 100


def get_water_region(image):
    box = (400, 320, 640, 360)  # Left, Top, Right, Bottom
    return image.crop(box)


def classify_wet_or_dry(file):
    im = Image.open(file)
    region = get_water_region(im)
    if not is_day(region):
        print file, "-> NIGHT"
        return
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
    # region.show()
    result = "WATER" if white > 850 else "DRY"

    print file, "->", "black=", black, "white=", white, "==>", result
    im.close()
    # print file, "->", brightness(region)
    # print file, "->", brightness2(region)
    # print file, "->", brightness3(region)