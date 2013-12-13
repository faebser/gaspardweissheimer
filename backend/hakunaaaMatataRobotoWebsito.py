import pystache
import logging as log
import markdown2 as markdown
from bs4 import BeautifulSoup as soup
from os import path, walk, remove
from shutil import copytree
import json
from classes.config import Config
from classes.entry import Entry

#logging
log.basicConfig(format='%(levelname)s: %(message)s', level=log.DEBUG)

# loading config
config = Config()

# paths
currentPath = path.dirname(path.realpath(__file__))
config.addPath("templatePath", path.join(currentPath, "templates"))
config.addPath("partialsPath", path.join(currentPath, "templates", "partials"))
config.addPath("contentPath", path.join(currentPath, "content"))

log.debug("-- paths --")
log.debug("currentPath: " + currentPath)
log.debug("templatePath: " + config.getPath("templatePath"))
log.debug("partialsPath: " + config.getPath("partialsPath"))
log.debug("contentPath: " + config.getPath("contentPath"))

#add image sizes
configJsonFile = json.loads(open(path.join(currentPath, "config.json")).read())
config.addImageSizes(configJsonFile["imageSizes"])

#load content
currentProjectPath = path.join(config.getPath("contentPath"), "promoted_stuff", "01_projekt1")
contentJsonFile = json.loads(open(path.join(currentProjectPath, "data.json")).read())
testEntry = Entry()
testEntry.simpleFillWithDict(contentJsonFile)

log.debug(str(Entry))

# partials
partials = {"entry-1": open(path.join(config.getPath("partialsPath"), "partial-entry-1.html")).read(), "entry-2": open(path.join(config.getPath("partialsPath"), "partial-entry-2.html")).read(), "entry-3": open(path.join(config.getPath("partialsPath"), "partial-entry-3.html")).read()}

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