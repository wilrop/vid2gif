import argparse
import imageio  # The python library for reading and writing images. See: http://imageio.github.io/.
import sys
from os import path


# Check if the filetype of the provided file is supported.
def valid_file_type(file_type):
    return file_type == 'mp4'   # Currently only mp4 is supported.


# Create the name of the new gif, by concatenating the current name with the gif filetype.
def make_gif_path(filename, save_to):
    gif_path = filename + ".gif"
    if save_to:
        gif_path = path.join(save_to, gif_path)

    return gif_path


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


# The function that controls the flow of the script.
def make_gif(args):
    file_path = args.file_path
    begin = args.begin
    end = args.end
    split_filename = path.basename(file_path).split(".")  # Take the filename and split it.
    filename = split_filename[0]
    file_type = split_filename[1]

    if valid_file_type(file_type):
        gif_path = make_gif_path(filename, args.save_to)
        reader = imageio.get_reader(file_path)
        writer = imageio.get_writer(gif_path, format="gif")

        meta_data = reader.get_meta_data()
        fps = meta_data['fps']
        duration = meta_data['duration']

        max_frame = calc_frame(duration, fps)
        begin = int(calc_frame(begin, fps))
        end = int(calc_frame(end, fps))

        if begin <= end <= max_frame:
            generate_gif(reader, writer, begin, end)
            print("Finished converting!")
        elif begin > end:
            print("Your begin time was greater than the end. Please try again.")
        else:
            print("Your end time exceeded the total duration of the video. Please retry for an earlier end.")
    else:
        print("The file type is not currently supported. Try a different file please!")


if __name__ == "__main__":
    print("Beginning conversion")
    parser = argparse.ArgumentParser()
    parser.add_argument("file_path", help="The path to the file you want to convert")
    parser.add_argument("begin", help="The beginning timestamp for the new GIF", type=int)
    parser.add_argument("end", help="The ending timestamp for the new GIF", type=int)
    parser.add_argument("--save_to", help="Path to the location where the GIF will be saved")
    args = parser.parse_args()

    make_gif(args)

