import pystache
import logging as log
import markdown2 as markdown
from bs4 import BeautifulSoup as soup
from os import path, walk, remove
from shutil import copytree
import json
from classes.config import Config

#logging
log.basicConfig(format='%(levelname)s: %(message)s', level=log.DEBUG)

# basic vars
currentPath = path.dirname(path.realpath(__file__))
templatePath = path.join(currentPath, "templates")
partialsPath = path.join(currentPath, "templates", "partials")
contentPath = path.join(currentPath, "content")

log.debug("-- paths --")
log.debug("currentPath: " + currentPath)
log.debug("templatePath: " + templatePath)
log.debug("partialsPath: " + partialsPath)
log.debug("contentPath: " + contentPath)


# loading config
config = Config()
configJsonFile = json.loads(open(path.join(currentPath, "config.json")).read())
log.debug("jsonFile: " + str(configJsonFile))
config.addImageSize(configJsonFile["imageSizes"])
log.debug("conifg: " + str(config))

#log.debug("config:" + str(config))


# partials
partials = {"entry-1": open(path.join(partialsPath, "partial-entry-1.html")).read(), "entry-2": open(path.join(partialsPath, "partial-entry-2.html")).read(), "entry-3": open(path.join(partialsPath, "partial-entry-3.html")).read()}

# pystache renderer init
renderer = pystache.Renderer(search_dirs=templatePath, file_extension="html", partials=partials)

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