from PIL import Image, ImageOps, ImageDraw


def upload_avatar_local(image):
    pass


def upload_avatar_remote(image):
    pass


def create_avatar(inImg, outImg):
    size = (64, 64)
    mask = Image.new('L', size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0) + size, fill=255)
    im = Image.open(inImg)
    output = ImageOps.fit(im, mask.size, centering=(0.5, 0.5))
    output.putalpha(mask)
    imgPath = '{}.png'.format(outImg)
    output.save(imgPath)


if __name__ == "__main__":
    create_avatar('man_photo.jpeg', 'output')