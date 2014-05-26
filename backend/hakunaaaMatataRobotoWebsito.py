# -*- coding: utf-8 -*-
import pystache
import logging as log
import markdown2 as markdown
from bs4 import BeautifulSoup as Soup
from os import path, walk, remove, makedirs, listdir
from shutil import copytree, copyfile
import json
from multiprocessing import Pool
from multiprocessing.dummy import Pool as ThreadPool
import codecs
from scss import Scss
from scss import config as scssconifg
from classes.config import Config, ImageSize
from classes.entry import Entry
from classes.imageHandling import fromJsonToImage, multiThreadedFromJsonToImage
import time


def iterateOverPosterImages(projectName, currentProjectPath, imageList):
    returning = iterateOverImages(projectName, currentProjectPath, imageList)
    for element, value in returning.iteritems():
        returning[str(element)]['path'] = '../' + value['path']
    return returning


def iterateOverOverviewImages(projectName, currentProjectPath, imageList):
    return iterateOverImages(projectName, currentProjectPath, imageList)


def iterateOverImages(projectName, currentProjectPath, imageList):
    pool = ThreadPool(config.threads)
    #build list
    threadList = []
    for element, value in imageList.iteritems():
        threadList.append([element, value, log, projectName, currentProjectPath, config])
    results = pool.map(multiThreadedFromJsonToImage, threadList)
    pool.close()
    return results[0] # ugly hack, watch out

def fromPythonToJson(imageObject):
    returnObject = {}
    for element, value in imageObject.iteritems():
        if element == 'normal' or element == 'class':
            returnObject[element] = value
        else:
            returnObject[element] = json.dumps(value)
    return returnObject

def iterateOverAllImages(projectName, currentProjectPath, imageList, blockList):
    # if imageList ist Path
    pool = ThreadPool(config.threads)
    #build list
    threadList = []
    if isinstance(imageList, (unicode, str)):
        imagePath = imageList
        imageSizes = config.getAllImageSizes()
        imageList = []
        for subdir, dirs, files in walk(path.join(currentProjectPath, imagePath)):
            for image in files:
                if not image in blockList and not path.basename(image).startswith('.'):
                    imageList.append({imagePath + image: imageSizes})
                else:
                    log.debug("image already used: " + str(image))
    for imageObject in imageList:
        for element, value in imageObject.iteritems():
            threadList.append([element, value, log, projectName, currentProjectPath, config])
    results = pool.map(multiThreadedFromJsonToImage, threadList)
    pool.close()

    #run json on python objects
    returnList = []
    for index, imageObject in enumerate(results):
        #imageSize, imagePath
        if index is not 0:
            imageObject['class'] = 'ajax'
        returnList.append(fromPythonToJson(imageObject))
    return returnList


def buildBlockingList(posterImages, overviewImages):
    returnList = [path.split(key)[1] for key in posterImages.keys()] + [path.split(key)[1] for key in overviewImages.keys()]
    return returnList


def main():
    # time it
    starttime = time.time()
    # paths
    config = Config()
    global config
    currentPath = path.dirname(path.realpath(__file__))
    config.addPath("templatePath", path.join(currentPath, "templates"))
    config.addPath("partialsPath", path.join(currentPath, "templates", "partials"))
    config.addPath("contentPath", path.join(currentPath, "content"))
    config.addPath("website", path.join(currentPath, "website"))
    config.addPath("images", path.join(config.getPath("website"), 'img'))
    config.addPath("css", path.join(config.getPath("website"), 'css'))
    config.addPath("js", path.join(config.getPath("website"), 'js'))
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
    config.threads = configJsonFile['threads']

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
    renderer.load_template("pageColor")

    # add removal of website dir
    if path.exists(config.getPath("website")):
        log.error("Please remove website-folder")
        exit(1)
    else:
        makedirs(config.getPath('website'), 0755)

    # copy stuff over
    copytree('../js', config.getPath('js'))
    copytree('../css', config.getPath('css'))

    #load promoted content
    promotedDirs = listdir(config.getPath('promoted'))
    promotedDirs.sort()
    log.debug("list of dirs: " + str(promotedDirs))

    htmlContent = {
        'promo': '',
        'overview': '',
        'bodyId': 'home',
        'nav': [
            {
                'link': 'someJsCode',
                'name': 'Arbeiten'
            }
        ]
    }
    promoAmount = 1  # add one for overview
    cssContent = ''
    pages = []


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
            currentEntry.setId(projectName)
            currentEntry.addClass('promo')
            if promoAmount is 1:
                currentEntry.addClass('active')
            currentEntry.posterImage = iterateOverPosterImages(projectName, currentProjectPath, currentJsonFile['posterImage'])
            currentEntry.overViewImage = iterateOverOverviewImages(projectName, currentProjectPath, currentJsonFile['overviewImage'])
            currentEntry.images = iterateOverAllImages(projectName, currentProjectPath, currentJsonFile['images'], buildBlockingList(currentJsonFile['posterImage'], currentJsonFile['overviewImage']))
            htmlContent['promo'] += renderer.render_name('promoEntryAndPage', currentEntry)
            cssContent += renderer.render_name('backgrounds', currentEntry)
            promoAmount += 1
    cssBackgroundsFile = codecs.open(path.join(config.getPath('css'), 'backgrounds.scss'), 'w+', encoding='utf-8')
    cssBackgroundsFile.write(cssContent)
    cssBackgroundsFile.close()

    #load overview content
    overviewJsonFile = json.loads(open(path.join(config.getPath('overview'), 'overview.json')).read())
    for row in overviewJsonFile['rows']:
        templateContent = {'type': config.getRowTypeOrNone(row['type'])}
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
                templateContent['entry-' + str(index)] = Entry()
                templateContent['entry-' + str(index)].simpleFillWithDict(currentJsonFile)
                templateContent['entry-' + str(index)].setId(projectName)
                templateContent['entry-' + str(index)].addClass('promo')
                templateContent['entry-' + str(index)].addClass('active')
                templateContent['entry-' + str(index)].posterImage = iterateOverPosterImages(projectName, currentProjectPath, currentJsonFile['posterImage'])
                templateContent['entry-' + str(index)].overViewImage = iterateOverOverviewImages(projectName, currentProjectPath, currentJsonFile['overviewImage'])
                templateContent['entry-' + str(index)].images = iterateOverAllImages(projectName, currentProjectPath, currentJsonFile['images'], buildBlockingList(currentJsonFile['posterImage'], currentJsonFile['overviewImage']))
                templateContent['entry-' + str(index)].path = templateContent['entry-' + str(index)].getId() + ".html"
                with codecs.open(path.join(config.getPath("website"), templateContent['entry-' + str(index)].getId() + ".html"), 'w+', encoding='utf-8') as indexFile:
                    indexFile.write(renderer.render_name('skeleton', {
                            "promo": renderer.render_name('promoEntryAndPage', templateContent['entry-' + str(index)]),
                            "bodyId": 'page',
                            "pageTitle": templateContent['entry-' + str(index)].title
                    }))
            htmlContent['overview'] += renderer.render_name('overviewRow', templateContent)

    #pages - rewrite
    pagesDir = listdir(config.getPath('pages'))
    pageColorContent = ''
    pagesDir.sort()
    makedirs(path.join(config.getPath('images'), 'pages'), 0755)
    for currentDir in pagesDir:
        if currentDir.startswith('.'):
            pass
        else:
            pageJson = json.loads(open(path.join(config.getPath('pages'), currentDir, 'data.json')).read())
            with codecs.open(path.join(config.getPath('pages'), currentDir, pageJson['text']), 'r', encoding='utf-8') as mdFile:
                page = {
                    'name': currentDir,
                    'title': pageJson['title'],
                    'text': unicode(markdown.markdown(mdFile.read())),
                    'id': pageJson['title'].lower(),
                    'color': pageJson.get('color', '#72898F')
                }
                htmlContent['nav'].append({
                    'link': page['name'] + ".html",
                    'name': page['title']
                })
                pageColorContent += renderer.render_name('pageColor', page)
                with codecs.open(path.join(config.getPath("website"), page['name'].lower() + ".html"), 'w+', encoding='utf-8') as indexFile:
                    rendered_page = Soup(renderer.render_name('page', page))
                    makedirs(path.join(config.getPath('images'), 'pages', currentDir), 0755)
                    targetPath = path.join(config.getPath('images'), 'pages', currentDir)
                    img = rendered_page.find_all('img')
                    for tag in img:
                        # get path and copy file to new destination
                        # change path to new destination
                        copyfile(path.join(config.getPath('pages'), currentDir, tag['src']), path.join(targetPath, tag['src']))
                        tag['src'] = path.relpath(path.join(targetPath, tag['src']), config.getPath("website"))
                    a = rendered_page.find_all('a')
                    for tag in a:
                        try:
                            if not tag['href'].startswith(('http', 'mailto',)) and tag['href'].endswith(('pdf', )):
                                copyfile(path.join(config.getPath('pages'), currentDir, tag['href']), path.join(targetPath, tag['href']))
                                tag['href'] = path.relpath(path.join(targetPath, tag['href']), config.getPath("website"))
                        except KeyError:
                            pass
                    indexFile.write(rendered_page.prettify())
    # add colors from pages to template
    cssPageColorsFile = codecs.open(path.join(config.getPath('css'), 'pageColor.scss'), 'w+', encoding='utf-8')
    cssPageColorsFile.write(pageColorContent)
    cssPageColorsFile.close()

    # generate index page with content from overview and promoted
    with codecs.open(path.join(config.getPath("website"), 'index.html'), 'w+', encoding='utf-8') as indexFile:
        indexFile.write(renderer.render_name('skeleton', htmlContent))
    # parse main.scss into main.css
    if path.exists(path.join(config.getPath('css'), 'main.css')):
        remove(path.join(config.getPath('css'), 'main.css'))
    with codecs.open(path.join(config.getPath("css"), 'main.css'), 'w+', encoding='utf-8') as mainCssFile:
        scssconifg.LOAD_PATHS = config.getPath('css')
        compiler = Scss(scss_opts=dict(compress=True), scss_vars={
            '$mainWidth': str(promoAmount * 100) + '%',
            '$promoWidth': str(100 / float(promoAmount)) + '%'
        })
        mainCssFile.write(compiler.compile(codecs.open(path.join(config.getPath('css'), 'main.scss'), 'r', encoding='utf-8').read()))

    endtime = time.time()
    duration = endtime-starttime

    log.info("generated in: " + str(duration / 60) + " minutes")


# loading config and make it globally available
config = Config()
#logging
log.basicConfig(format='%(levelname)s: %(message)s', level=log.DEBUG)

if __name__ == "__main__":
    main()
