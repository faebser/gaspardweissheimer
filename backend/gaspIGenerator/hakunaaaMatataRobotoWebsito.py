import pystache
import logging as log
import markdown2 as markdown
from bs4 import BeautifulSoup as soup
from os import path, walk, remove
from shutil import copytree

#logging
log.basicConfig(format='%(levelname)s: %(message)s', level=log.DEBUG)

# basic vars
currentPath = path.dirname(path.realpath(__file__))
templatePath = path.join(currentPath, "..", "templates")
partialsPath = path.join(currentPath, "..", "templates", "partials")
contentPath = path.join(currentPath, "..", "content")

#partials
partials = {"entry-1" : open(path.join(partialsPath, "partial-entry-1.html")).read(), "entry-2" : open(path.join(partialsPath, "partial-entry-2.html")).read(), "entry-3" : open(path.join(partialsPath, "partial-entry-3.html")).read()}

#pystache renderer init
renderer = pystache.Renderer(search_dirs=templatePath, file_extension="html", partials=partials)

#load templates
renderer.load_template("overviewRow.html")
renderer.load_template("promoEntryAndPage.html")

#find out how json with python works
#find out how image manip in python works
#define sizes of the images, put them in a folder and remember the path
#write the path into the template and also make some css templates
#write all the css templates into main.css
#grad the data, build object, push the through the template
#add the returned thing to the skeleton