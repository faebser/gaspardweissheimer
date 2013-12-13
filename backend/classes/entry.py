class Entry(object):
    title = ""
    subtitle = ""
    text = ""
    posterImage = {}
    overViewImage = {}
    images = {}

    def __init__(self):
        pass

    def setTitle(self, title):
        self.title = title

    def getTitle(self):
        return self.title

    def setSubtitle(self, subtitle):
        self.subtitle = subtitle

    def getSubtitle(self):
        return self.subtitle

    def setText(self, text):
        self.text = text

    def getText(self):
        return self.text

    def addPosterImage(self, imageSize, path):
        self.posterImage[imageSize] = path

    def getPosterImage(self, imageSize):
        return self.posterImage[imageSize]

    def addOverViewImage(self, imageSize, path):
        self.overViewImage[imageSize] = path

    def addImage(self, index, data):
        self.images[index] = data

    def getImageAt(self, index):
        return self.images[index]

    def simpleFillWithDict(self, jsonDict):
        if 'title' in jsonDict:
            self.setTitle(jsonDict['title'])
        if 'subtitle' in jsonDict:
            self.setSubtitle(jsonDict['subtitle'])
        if 'text' in jsonDict:
            self.setText(jsonDict['text'])