class Config(object):
    imageSizes = {}

    def addImageSize(self, json):
        print json
        return None


class ImageSize(object):
    def __init__(self, height, width):
        if height is None:
            self.height = 0
        else:
            self.height = height
        if width is None:
            self.width = 0
        else:
            self.width = width