from PIL import Image, ImageOps, ImageDraw
from os import path
from datetime import datetime
import base64

folderAbs = path.dirname(path.abspath(__file__))


class ImageWorker:

    def __init__(self, controller):
        self.dt = datetime.now()
        self.controller = controller

    def createAvatar(self, inImg):
        size = (64, 64)
        mask = Image.new('L', size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0) + size, fill=255)
        im = Image.open(inImg)
        output = ImageOps.fit(im, mask.size, centering=(0.5, 0.5))
        output.putalpha(mask)
        imgName = '{}.png'.format(self.controller.username)
        imgPath = path.join(folderAbs, 'avatars', imgName)
        output.save(imgPath)
        return imgPath

    def createListAvatar(self, contact, folderPath, inImg, defaultImg):
        if not inImg:
            return defaultImg
        size = (32, 32)
        mask = Image.new('L', size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0) + size, fill=255)
        im = Image.open(inImg)
        output = ImageOps.fit(im, mask.size, centering=(0.5, 0.5))
        output.putalpha(mask)
        imgName = '{}.png'.format(contact)
        imgPath = folderPath + imgName
        output.save(imgPath)
        return imgPath

    def convertFromBytesToString(self, image):
        with open(image, "rb") as imgBytes:
            imgString = base64.b64encode(imgBytes.read()).decode()
            return imgString


if __name__ == '__main__':
    dt = datetime.now()
    imgName = 'default_profile.png'
    imgPath = path.join(folderAbs, 'avatars', imgName)
    a = ImageWorker()
    print(a.convertFromBytesToString(imgPath))
