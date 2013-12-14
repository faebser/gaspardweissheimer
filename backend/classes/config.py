class Config(object):
    imageSizes = {}
    paths = {}

    def addPath(self, name, path):
        self.paths[name] = path

    def getPath(self, name):
        return self.paths[name]

    def addImageSizes(self, json):
        for element, value in json.iteritems():
            if value[0] in 'width':
                height = None
                width = value[1]
            else:
                height = value[1]
                width = None
            self.imageSizes[element] = ImageSize(height, width)
        return None

    def getAllImageSizes(self):
        return self.imageSizes.keys()

    def getImageSizeOrNone(self, name):
        if name in self.imageSizes:
            return self.imageSizes[name]
        else:
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