import imageio  # The python library for reading and writing images. See: http://imageio.github.io/.
import sys

# Get the name for the new gif from the name of the current file.
def getFileName(filePath):
    print("Getting file name from path.")
    splittedPath = filePath.split('/')              # Split the path.
    completeFile = splittedPath[-1]                 # Get the last element. This is the destination.
    fileName = completeFile.split('.')[0]           # Split the filename. We get the name at 0 and the type at 1.
    gifFile = fileName + '.gif'                     # Combine the name with .gif and return this.
    return gifFile

def makeGif(reader, writer, begin, end):
    print("Converting the file to a gif.")
    for frame in range(begin, end):
        writer.append_data(reader.get_data(frame))

    writer.close()
    reader.close()
    print ("Finished converting!")


# Calculate a specific frame for a given time.
def calcFrame(time, fps):  
    return time * fps

args = sys.argv

filePath = args[1]
begin = int(args[2])
end = int(args[3])
gifFile = getFileName(filePath)

reader = imageio.get_reader(filePath)
writer = imageio.get_writer(gifFile)
metaData = reader.get_meta_data()
fps = metaData['fps']
begin = int(calcFrame(begin, fps))
end = int(calcFrame(end, fps))
makeGif(reader, writer, begin, end)









