import imageio  # The python library for reading and writing images. See: http://imageio.github.io/.
import sys

# Create the name of the new gif, by concatenating the current name with the gif filetype.
def getFileName(filePath):
    print("Getting file name from path.")
    splittedPath = filePath.split('/')              # Split the path.
    completeFile = splittedPath[-1]                     # Get the last element. This is the destination.
    splittedFile = completeFile.split('.')              # Split the filename. We get the name at 0 and the type at 1.
    return splittedFile

# Check if the filetype of the provided file is supported.
def validFileType(fileType):
    return fileType == 'mp4'   # Currently only mp4 is supported.

# Create the name of the new gif, by concatenating the current name with the gif filetype.
def makeGifName(fileName):
    return fileName + '.gif'

# Calculate a specific frame for a given time.
def calcFrame(time, fps):  
    return time * fps

# Actually create the gif.
def generateGif(reader, writer, begin, end):
    print("Converting the file to a gif.")
    for frame in range(begin, end):
        writer.append_data(reader.get_data(frame))      # Get the correct frame and write this to the gif file.

    writer.close()      # Close the writer and reader.
    reader.close()
    print ("Finished converting!")

# The function that controls the flow of the script. This gets called with the arguments provided by the user.
def makeGif(args):
    filePath = args[1]
    begin = int(args[2])
    end = int(args[3])
    splittedFile = getFileName(filePath)
    fileName = splittedFile[0]
    fileType = splittedFile[1]

    if validFileType(fileType):
        gifName = makeGifName(fileName)
        reader = imageio.get_reader(filePath)
        writer = imageio.get_writer(gifName)
        metaData = reader.get_meta_data()
        fps = metaData['fps']
        duration = metaData['duration']
        maxFrame = calcFrame(duration, fps)
        begin = int(calcFrame(begin, fps))
        end = int(calcFrame(end, fps)) 

        if begin <= end and end <= maxFrame:
            generateGif(reader, writer, begin, end)
        elif begin > end:
            print("Your begin time was greater than the end. Please try again.")
        else:
            print("Your end time exceeded the total duration of the video. Please retry for an earlier end.")

makeGif(sys.argv)