from os import path, makedirs
from PIL import Image
from os.path import relpath

def multiThreadedFromJsonToImage(inputVars):
    return fromJsonToImage(inputVars[0], inputVars[1], inputVars[2], inputVars[3], inputVars[4], inputVars[5])

def fromJsonToImage(jsonFileName, imageSizes, log, projectName, projectPath, config):
    fileName, extension = path.splitext(path.basename(jsonFileName))
    pathForImage = path.join(config.getPath('images'), projectName)
    returnDict = {}
    if not path.exists(pathForImage):
        makedirs(pathForImage)
    image = Image.open(path.join(projectPath, jsonFileName))
    imageWidth = image.size[0]
    imageHeight = image.size[1]

    for imageSizeName in imageSizes:
        imageSize = config.getImageSizeOrNone(imageSizeName)
        tempPath = path.join(pathForImage, fileName + "_" + imageSizeName + extension)
        if not path.exists(tempPath):
            if not imageSizeName in imageSizes:
                log.error("imageSize not know: " + imageSizeName)
                exit(1)
            else:
                size = [0, 0]
                if imageSize.height is 0:
                    size[0] = imageSize.width
                    size[1] = int(float(float(imageSize.width) / float(imageWidth)) * imageHeight)
                elif imageSize.width is 0:
                    size[0] = int(float((float(imageSize.height) / float(imageHeight))) * imageWidth)
                    size[1] = imageSize.height
                resizedImage = image.resize(size, Image.ANTIALIAS)
                try:
                    log.info("writing file: " + tempPath)
                    resizedImage.save(tempPath)
                    tempPath = relpath(tempPath, config.getPath("website"))
                    returnDict[imageSizeName] = tempPath
                except KeyError:
                    log.error("file-format unknown in: " + projectPath + " with imageSize " + imageSizeName)
                    pass
                except IOError:
                    log.error("file-format could not be written in: " + projectPath + " with imageSize " + imageSizeName)
        else:
            returnDict[imageSizeName] = tempPath
            #log.debug("file already exists: " + tempPath)
    return returnDict
