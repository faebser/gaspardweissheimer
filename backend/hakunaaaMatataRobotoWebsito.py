# -*- coding: utf-8 -*-
import pystache
import logging as log
import markdown2 as markdown
from bs4 import BeautifulSoup as soup
from os import path, walk, remove, makedirs, listdir
from shutil import copytree
import json
import codecs

from classes.config import Config, ImageSize
from classes.entry import Entry
from classes.imageHandling import fromJsonToImage




def iterateOverPosterImages(projectName, currentProjectPath, entry, imageList):
    iterateOverImages(projectName, currentProjectPath, entry, 'posterImage', imageList)


def iterateOverOverviewImages(projectName, currentProjectPath, entry, imageList):
    iterateOverImages(projectName, currentProjectPath, entry, 'overviewImage', imageList)


def iterateOverImages(projectName, currentProjectPath, entry, nodeName, imageList):
    for element, value in imageList.iteritems():
        results = fromJsonToImage(element, value, log, projectName, currentProjectPath, config)
        for imageSize, imagePath in results.iteritems():
            if 'overviewImage' in nodeName:
                entry.addOverViewImage(imageSize, imagePath)
            elif 'posterImage' in nodeName:
                entry.addPosterImage(imageSize, imagePath)
            else:
                entry.addImage(results.index(imageSize), {imageSize, imagePath})


def iterateOverAllImages(projectName, currentProjectPath, entry, imageList, blockList):
    # if imageList ist Path
    if isinstance(imageList, (unicode, str)):
        imagePath = imageList
        imageSizes = config.getAllImageSizes()
        imageList = []
        for subdir, dirs, files in walk(path.join(currentProjectPath, imagePath)):
            for image in files:
                if not image in blockList:
                    imageList.append({imagePath + image: imageSizes})
                else:
                    log.debug("image already used: " + str(image))
    for imageObject in imageList:
        index = imageList.index(imageObject)
        for element, value in imageObject.iteritems():
            #fromJsonToImage(jsonFileName, imageSizes, log, projectName, projectPath, config):
            results = fromJsonToImage(element, value, log, projectName, currentProjectPath, config)
            if index is 0:
                entryData = {}
            else:
                entryData = {'class': 'ajax'}
            for imageSize, imagePath in results.iteritems():
                entryData[imageSize] = imagePath
            entry.addImage(index, entryData)

def buildBlockingList(posterImages, overviewImages):
    returnList = [path.split(key)[1] for key in posterImages.keys()] + [path.split(key)[1] for key in overviewImages.keys()]
    return returnList


def main():

    # paths
    currentPath = path.dirname(path.realpath(__file__))
    config.addPath("templatePath", path.join(currentPath, "templates"))
    config.addPath("partialsPath", path.join(currentPath, "templates", "partials"))
    config.addPath("contentPath", path.join(currentPath, "content"))
    config.addPath("website", path.join(currentPath, "website"))
    config.addPath("images", path.join(config.getPath("website"), 'img'))
    config.addPath("css", path.join(config.getPath("website"), 'css'))
    config.addPath("overview", path.join(config.getPath("contentPath"), 'overview'))
    config.addPath("pages", path.join(config.getPath("contentPath"), 'pages'))
    config.addPath("promoted", path.join(config.getPath("contentPath"), 'promoted_stuff'))

    log.debug("-- paths --")
    log.debug("currentPath: " + currentPath)
    log.debug("templatePath: " + config.getPath("templatePath"))
    log.debug("partialsPath: " + config.getPath("partialsPath"))
    log.debug("contentPath: " + config.getPath("contentPath"))

    configJsonFile = json.loads(open(path.join(currentPath, "config.json")).read())
    config.addImageSizes(configJsonFile["imageSizes"])
    config.addRowTypes(configJsonFile["rowTypes"])

    # partials
    partials = {"entry-1": open(path.join(config.getPath("partialsPath"), "partial-entry-1.html")).read(),
                "entry-2": open(path.join(config.getPath("partialsPath"), "partial-entry-2.html")).read(),
                "entry-3": open(path.join(config.getPath("partialsPath"), "partial-entry-3.html")).read(),
                "nav": open(path.join(config.getPath("partialsPath"), "nav.html")).read()}

    # pystache renderer init
    renderer = pystache.Renderer(search_dirs=config.getPath("templatePath"), file_extension="html", partials=partials)

    # load templates
    renderer.load_template("overviewRow")
    renderer.load_template("promoEntryAndPage")
    renderer.load_template("backgrounds")
    renderer.load_template("skeleton")
    renderer.load_template("page")

    # add removal of website dir
    if path.exists(config.getPath("website")):
        log.error("Please remove website-folder")
        exit(1)

    #load promoted content
    promotedDirs = listdir(config.getPath('promoted'))
    promotedDirs.sort()
    log.debug("list of dirs: " + str(promotedDirs))

    htmlContent = {
        'promo': '',
        'overview': ''
    }
    cssContent = ''

    """TODO: add colors to css"""

    for currentDir in promotedDirs:
        if currentDir.startswith("."):
            pass
        else:
            projectName = currentDir
            currentProjectPath = path.join(config.getPath('promoted'), projectName)
            try:
                currentJsonFile = json.loads(open(path.join(currentProjectPath, 'data.json')).read())
            except ValueError:
                log.exception("Error while reading json-file: " + path.join(currentProjectPath, 'data.json'))
                exit(1)
            currentEntry = Entry()
            currentEntry.simpleFillWithDict(currentJsonFile)
            iterateOverPosterImages(projectName, currentProjectPath, currentEntry, currentJsonFile['posterImage'])
            iterateOverOverviewImages(projectName, currentProjectPath, currentEntry, currentJsonFile['overviewImage'])
            iterateOverAllImages(projectName, currentProjectPath, currentEntry, currentJsonFile['images'], buildBlockingList(currentJsonFile['posterImage'], currentJsonFile['overviewImage']))
            htmlContent['promo'] += renderer.render_name('promoEntryAndPage', currentEntry)
            cssContent += renderer.render_name('backgrounds', currentEntry)
            #log.debug("css: " + cssContent)
            #log.debug("content: " + htmlContent)

    makedirs(config.getPath('css'), 0755)
    cssBackgroundsFile = codecs.open(path.join(config.getPath('css'), 'backgrounds.css'), 'w+', encoding='utf-8')
    cssBackgroundsFile.write(cssContent)
    cssBackgroundsFile.close()

    #load overview content
    overviewJsonFile = json.loads(open(path.join(config.getPath('overview'), 'overview.json')).read())
    for row in overviewJsonFile['rows']:
        templateContent = {}
        templateContent['type'] = config.getRowTypeOrNone(row['type'])
        if templateContent['type'] is None:
            log.error("Invalid Type with value: " + row['type'] + " in overview.json")
        else:
            for index, entry in enumerate(row['entries'], 1):
                log.debug("entry and index: " + str(index) + " / " + str(entry))
                try:
                    currentJsonFile = json.loads(open(path.join(config.getPath('overview'), entry, 'data.json')).read())
                except ValueError:
                    log.exception("Error while reading json-file: " + path.join(config.getPath('overview'), entry, 'data.json'))
                    exit(1)
                currentProjectPath = path.join(config.getPath('overview'), entry)
                projectName = entry
                overviewEntry = Entry()
                overviewEntry.simpleFillWithDict(currentJsonFile)
                iterateOverPosterImages(projectName, currentProjectPath, overviewEntry, currentJsonFile['posterImage'])
                iterateOverOverviewImages(projectName, currentProjectPath, overviewEntry, currentJsonFile['overviewImage'])
                iterateOverAllImages(projectName, currentProjectPath, overviewEntry, currentJsonFile['images'], buildBlockingList(currentJsonFile['posterImage'], currentJsonFile['overviewImage']))
                templateContent['entry-' + str(index)] = overviewEntry
                with codecs.open(path.join(config.getPath("website"), overviewEntry.getId() + ".html"), 'w+', encoding='utf-8') as indexFile:
                    indexFile.write(renderer.render_name('skeleton', {"promo": renderer.render_name('promoEntryAndPage', overviewEntry)}))
            htmlContent['overview'] += renderer.render_name('overviewRow', templateContent)

                #generate page for each
    log.debug(htmlContent['overview'])
    with codecs.open(path.join(config.getPath("website"), 'index.html'), 'w+', encoding='utf-8') as indexFile:
        indexFile.write(renderer.render_name('skeleton', htmlContent))

    #pages
    pagesDir = listdir(config.getPath('pages'))
    pagesDir.sort()
    for currentDir in pagesDir:
        if currentDir.startswith('.'):
            pass
        else:
            pageJson = json.loads(open(path.join(config.getPath('pages'), currentDir, 'data.json')).read())
            with codecs.open(path.join(config.getPath('pages'), currentDir, pageJson['text']), 'r', encoding='utf-8') as mdFile:
                page = {
                    'name': currentDir,
                    'title': pageJson['title'],
                    'text': unicode(markdown.markdown(mdFile.read()))
                }
                with codecs.open(path.join(config.getPath("website"), page['name'].lower() + ".html"), 'w+', encoding='utf-8') as indexFile:
                    indexFile.write(renderer.render_name('page', page))
    # build nav

# loading config and make it globally available
config = Config()
#logging
log.basicConfig(format='%(levelname)s: %(message)s', level=log.DEBUG)

if __name__ == "__main__":
    log.debug("main called")
    main()

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

