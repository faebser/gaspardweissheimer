import pystache
import os

templateFile = open("order50-25-25.html").read()
partials = {"entry-1" : open("partial-entry-1.html").read(), "entry-2" : open("partial-entry-2.html").read(), "entry-3" : open("partial-entry-3.html").read()}
data = {"entry-1" : {"title" : "test"}}

renderer = pystache.Renderer(search_dirs=os.path.dirname(os.path.realpath(__file__)), file_extension="html", partials=partials)
renderer.load_template("order50-25-25")
#renderer.load_partial("partial-entry-1")

print(renderer.render_name("order50-25-25", data))
