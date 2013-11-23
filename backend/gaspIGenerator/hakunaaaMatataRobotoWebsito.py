import pystache
import os.path as path

currentDir = path.dirname(path.realpath(__file__))
templateDir = path.join(currentDir, "..", "templates")
partialsDir = path.join(currentDir, "..", "templates", "partials")
contentDir = path.join(currentDir, "..", "content")