import pystache
import logging as log
import markdown2 as markdown
from bs4 import BeautifulSoup as soup
from os import path, walk, remove, makedirs, listdir
from shutil import copytree
import json
from classes.config import Config, ImageSize
from classes.entry import Entry
from classes.imageHandling import fromJsonToImage
from PIL import Image, ImageOps

#logging
log.basicConfig(format='%(levelname)s: %(message)s', level=log.DEBUG)

# loading config
config = Config()

# paths
currentPath = path.dirname(path.realpath(__file__))
config.addPath("templatePath", path.join(currentPath, "templates"))
config.addPath("partialsPath", path.join(currentPath, "templates", "partials"))
config.addPath("contentPath", path.join(currentPath, "content"))
config.addPath("website", path.join(currentPath, "website"))
config.addPath("images", path.join(config.getPath("website"), 'img'))
config.addPath("overview", path.join(config.getPath("contentPath"), 'overview'))
config.addPath("pages", path.join(config.getPath("contentPath"), 'pages'))
config.addPath("promoted", path.join(config.getPath("contentPath"), 'promoted_stuff'))

log.debug("-- paths --")
log.debug("currentPath: " + currentPath)
log.debug("templatePath: " + config.getPath("templatePath"))
log.debug("partialsPath: " + config.getPath("partialsPath"))
log.debug("contentPath: " + config.getPath("contentPath"))

def iterateOverPosterImages(projectName, currentProjectPath, entry):
    pass

def iterateOverOverviewImages(projectName, currentProjectPath, entry):
    pass

def iterateOverAllImages(projectName, currentProjectPath, entry):
    pass

def iterateOverImages(projectname, currentProjectPath, entry, nodeName):
    pass

#add image sizes
configJsonFile = json.loads(open(path.join(currentPath, "config.json")).read())
config.addImageSizes(configJsonFile["imageSizes"])

#load content
promotedDirs = listdir(config.getPath('promoted'))
log.debug("list of dirs: " + str(promotedDirs))

for currentDir in promotedDirs:
    projectName = currentDir
    currentProjectPath = path.join(config.getPath('promoted'), projectName)
    currentJsonFile = json.loads(open(path.join(currentProjectPath, 'data.json')).read())
    currentEntry = Entry()
    currentEntry.simpleFillWithDict(currentJsonFile)


projectName = "01_projekt1"
currentProjectPath = path.join(config.getPath("contentPath"), "promoted_stuff", projectName)
contentJsonFile = json.loads(open(path.join(currentProjectPath, "data.json")).read())
testEntry = Entry()
testEntry.simpleFillWithDict(contentJsonFile)
# get pictures

for element, value in contentJsonFile['posterImage'].iteritems():
    results = fromJsonToImage(element, value, config.getPath("images"), log, config, projectName, currentProjectPath)
    for imageSize, imagePath in results.iteritems():
        testEntry.addPosterImage(imageSize, imagePath)

for element, value in contentJsonFile['overviewImage'].iteritems():
    results = fromJsonToImage(element, value, config.getPath("images"), log, config, projectName, currentProjectPath)
    for imageSize, imagePath in results.iteritems():
        testEntry.addOverViewImage(imageSize, imagePath)

for object in contentJsonFile['images']:
    index = contentJsonFile['images'].index(object)
    for element, value in object.iteritems():
        results = fromJsonToImage(element, value, config.getPath("images"), log, config, projectName, currentProjectPath)
        for imageSize, imagePath in results.iteritems():
            pass
            testEntry.addImage(index, {imageSize, imagePath})

#log.debug(contentJsonFile['posterImage'])
#log.debug(contentJsonFile['overviewImage'])

#get all content from promoted stuff and input into the template
#get all content from overview and generate pages
#get all content from pages and generate pages


# partials
partials = {"entry-1": open(path.join(config.getPath("partialsPath"), "partial-entry-1.html")).read(),
            "entry-2": open(path.join(config.getPath("partialsPath"), "partial-entry-2.html")).read(),
            "entry-3": open(path.join(config.getPath("partialsPath"), "partial-entry-3.html")).read()}

# pystache renderer init
renderer = pystache.Renderer(search_dirs=config.getPath("templatePath"), file_extension="html", partials=partials)

# load templates
renderer.load_template("overviewRow")
renderer.load_template("promoEntryAndPage")

# find out how json with python works - done
# find out how image manip in python works
# define sizes of the images, put them in a folder and remember the path
# write the path into the template and also make some css templates
# write all the css templates into main.css
# grab the data, build object, push them through the template
# add the returned thing to the skeleton

