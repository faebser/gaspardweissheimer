# -*- coding: utf-8 -*-

class Entry(object):

    title = ""
    subtitle = ""
    text = ""
    cssId = ""
    posterImage = {}
    overViewImage = {}
    images = []
    cssTitle = ""
    classes = []

    def __init__(self):
        self.posterImage.clear()
        self.overViewImage.clear()
        self.images = []
        self.classes = []

    def __str__(self):
        return str(self.images)

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
        self.images.insert(index, data)

    def getImageAt(self, index):
        return self.images[index]

    def setId(self, cssId):
        """
        @param cssId: str
        @return: void
        """
        self.cssId = cssId.lower().lstrip('1234567890_').replace(' ', '_')
        pass

    def getId(self):
        return self.cssId

    def addClass(self, cssClass):
        self.classes.append(cssClass)

    def simpleFillWithDict(self, jsonDict):
        if 'title' in jsonDict:
            self.setTitle(jsonDict['title'])
        if 'subtitle' in jsonDict:
            self.setSubtitle(jsonDict['subtitle'])
        if 'text' in jsonDict:
            self.setText(jsonDict['text'])