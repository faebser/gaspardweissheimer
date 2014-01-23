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


# functions depending on global config object. Pretty ugly, I know
def iterateOverPosterImages(projectName, currentProjectPath, entry, jsonFile):
    iterateOverImages(projectName, currentProjectPath, entry, 'posterImage', jsonFile)


def iterateOverOverviewImages(projectName, currentProjectPath, entry, jsonFile):
    iterateOverImages(projectName, currentProjectPath, entry, 'overviewImage', jsonFile)


def iterateOverImages(projectName, currentProjectPath, entry, nodeName, jsonFile):
    log.debug("values: " + str(jsonFile[nodeName]))
    for element, value in jsonFile[nodeName].iteritems():
        results = fromJsonToImage(element, value, config.getPath("images"), log, config, projectName, currentProjectPath)
        for imageSize, imagePath in results.iteritems():
            entry.addPosterImage(imageSize, imagePath)


def iterateOverAllImages(projectName, currentProjectPath, entry, jsonFile):
    for imageObject in jsonFile['images']:
        index = jsonFile['images'].index(imageObject)
        for element, value in imageObject.iteritems():
            results = fromJsonToImage(element, value, config.getPath("images"), log, config, projectName, currentProjectPath)
            if index is 0:
                entryData = {}
            else:
                entryData = {'class': 'ajax'}
            for imageSize, imagePath in results.iteritems():
                entryData[imageSize] = imagePath
            entry.addImage(index, entryData)

# main starts here
configJsonFile = json.loads(open(path.join(currentPath, "config.json")).read())
config.addImageSizes(configJsonFile["imageSizes"])
config.addRowTypes(configJsonFile["rowTypes"])

# partials
partials = {"entry-1": open(path.join(config.getPath("partialsPath"), "partial-entry-1.html")).read(),
            "entry-2": open(path.join(config.getPath("partialsPath"), "partial-entry-2.html")).read(),
            "entry-3": open(path.join(config.getPath("partialsPath"), "partial-entry-3.html")).read()}

# pystache renderer init
renderer = pystache.Renderer(search_dirs=config.getPath("templatePath"), file_extension="html", partials=partials)

# load templates
renderer.load_template("overviewRow")
renderer.load_template("promoEntryAndPage")
renderer.load_template("backgrounds")
#renderer.load_template("skeleton")

#load promoted content
promotedDirs = listdir(config.getPath('promoted'))
promotedDirs.sort()
log.debug("list of dirs: " + str(promotedDirs))

htmlContent = ''
cssContent = ''

for currentDir in promotedDirs:
    if currentDir.startswith("."):
        pass
    else:
        projectName = currentDir
        currentProjectPath = path.join(config.getPath('promoted'), projectName)
        currentJsonFile = json.loads(open(path.join(currentProjectPath, 'data.json')).read())
        currentEntry = Entry()
        currentEntry.simpleFillWithDict(currentJsonFile)
        currentEntry.setId(currentJsonFile['title'])
        iterateOverPosterImages(projectName, currentProjectPath, currentEntry, currentJsonFile)
        iterateOverOverviewImages(projectName, currentProjectPath, currentEntry, currentJsonFile)
        #iterateOverAllImages(projectName, currentProjectPath, currentEntry, currentJsonFile)
        #log.debug(currentEntry)
        htmlContent += renderer.render_name('promoEntryAndPage', currentEntry)
        cssContent += renderer.render_name('backgrounds', currentEntry)
        #log.debug("css: " + cssContent)
        log.debug("content: " + htmlContent)

#load overview content

overviewJsonFile = json.loads(open(path.join(config.getPath('overview'), 'overview.json')).read())

for row in overviewJsonFile['rows']:
    templateContent = {}
    rowType = config.getRowTypeOrNone(row['type'])
    if rowType is None:
        log.error("Invalid Type with value: " + row['type'] + " in overview.json")
        pass
    else:
        for index, entry in enumerate(row['entries']):
            log.debug("entry and index: " + str(index) + " / " + str(entry))
            overviewEntry = Entry()
            overviewEntry.simpleFillWithDict(currentJsonFile)
            overviewEntry.setId(currentJsonFile['title'])
            iterateOverPosterImages(projectName, currentProjectPath, overviewEntry, currentJsonFile)
            iterateOverOverviewImages(projectName, currentProjectPath, overviewEntry, currentJsonFile)
            templateContent['entry-' + str(index)] = overviewEntry





#ouput = renderer

#log.debug(contentJsonFile['posterImage'])
#log.debug(contentJsonFile['overviewImage'])

#get all content from promoted stuff and input into the template
#get all content from overview and generate pages
#get all content from pages and generate pages




# find out how json with python works - done
# find out how image manip in python works
# define sizes of the images, put them in a folder and remember the path
# write the path into the template and also make some css templates
# write all the css templates into main.css
# grab the data, build object, push them through the template
# add the returned thing to the skeleton

