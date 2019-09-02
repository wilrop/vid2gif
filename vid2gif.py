import imageio  # The python library for reading and writing images. See: http://imageio.github.io/.
import sys


# Create the name of the new gif, by concatenating the current name with the gif filetype.
def get_filename(file_path):
    print("Getting file name from path.")
    split_path = file_path.split('/')              # Split the path.
    complete_file = split_path[-1]                     # Get the last element. This is the destination.
    split_file = complete_file.split('.')              # Split the filename. We get the name at 0 and the type at 1.
    return split_file


# Check if the filetype of the provided file is supported.
def valid_file_type(file_type):
    return file_type == 'mp4'   # Currently only mp4 is supported.


# Create the name of the new gif, by concatenating the current name with the gif filetype.
def make_gif_name(filename):
    return filename + '.gif'


# Calculate a specific frame for a given time.
def calc_frame(time, fps):
    return time * fps


# Actually create the gif.
def generate_gif(reader, writer, begin, end):
    print("Converting the file to a gif.")
    for frame in range(begin, end):
        writer.append_data(reader.get_data(frame))      # Get the correct frame and write this to the gif file.

    writer.close()      # Close the writer and reader.
    reader.close()
    print("Finished converting!")


# The function that controls the flow of the script. This gets called with the arguments provided by the user.
def make_gif(args):
    file_path = args[1]
    begin = int(args[2])
    end = int(args[3])
    split_file = get_filename(file_path)
    filename = split_file[0]
    file_type = split_file[1]

    if valid_file_type(file_type):
        gif_name = make_gif_name(filename)
        reader = imageio.get_reader(file_path)
        writer = imageio.get_writer(gif_name)
        meta_data = reader.get_meta_data()
        fps = meta_data['fps']
        duration = meta_data['duration']
        max_frame = calc_frame(duration, fps)
        begin = int(calc_frame(begin, fps))
        end = int(calc_frame(end, fps))

        if begin <= end and end <= max_frame:
            generate_gif(reader, writer, begin, end)
        elif begin > end:
            print("Your begin time was greater than the end. Please try again.")
        else:
            print("Your end time exceeded the total duration of the video. Please retry for an earlier end.")


make_gif(sys.argv)
