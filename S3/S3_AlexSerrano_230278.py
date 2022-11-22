import os
import sys


def video_scaler(inPath: str):
    # Resizes the input video to all the resolutions needed
    os.system("ffmpeg -i " + inPath + " -vf scale=1280:720 -c:a copy BBB_720p.mp4")
    os.system("ffmpeg -i " + inPath + " -vf scale=640:480 -c:a copy BBB_480p.mp4")
    os.system("ffmpeg -i " + inPath + " -vf scale=360:240 -c:a copy BBB_360x240p.mp4")
    os.system("ffmpeg -i " + inPath + " -vf scale=160:120 -c:a copy BBB_160x120p.mp4")

    return -1


def video_converter(inPath: str):
    # Converts the input video to all the codecs needed
    os.system("ffmpeg -i " + inPath + " -c:v libvpx -c:a libvorbis vp8.webm")  # VP8
    os.system("ffmpeg -i " + inPath + " -c:v libvpx-vp9 -c:a libvorbis vp9.webm")  # VP9
    os.system("ffmpeg -i " + inPath + " -c:v libx265 -c:a ac3 -b:a 256k h265.mp4")  # H.265
    os.system("ffmpeg -i " + inPath + " -c:v libaom-av1 -c:a ac3 -b:a 256k av1.mkv")  # AV1


def create4video():
    # Creates the video with the 4 videos so that we can compare them
    os.system("ffmpeg -i vp8.webm -i vp9.webm -filter_complex hstack output.mp4")
    os.system("ffmpeg -i h265.mp4 -i av1.mkv -filter_complex hstack output2.mp4")
    os.system("ffmpeg -i output.mp4 -i output2.mp4 -filter_complex vstack 4stack.mp4")
    os.remove("output.mp4")
    os.remove("output2.mp4")


loop = 1
if __name__ == '__main__':
    option = 0
    while loop != 0:
        match option:
            # The user is allowed to navigate through all the exercises without the need of the code
            case 0:
                option = int(input('\n0 - Navigate by typing the number of the exercise:\n'
                                   '1 - Resize the input video to 720p, 480p, 360x240 and 160x120\n'
                                   '2 - Convert to different video codecs\n'
                                   '3 - Create the video with 4 videos\n'
                                   '4 - Execute the Visual Interface\n'
                                   '5 -  Exit\n'
                                   ''))
            # Cases 1 to 3 are to get the "mandanga" in order to create the videos for the first part of the seminar
            case 1:
                user_in1 = str(input("Enter the name of the video (with its extension, e.g. .mp4): "))
                video_scaler(user_in1)
                option = 0

            case 2:
                user_in2 = str(input("Enter the name of the video (with its extension, e.g. .mp4): "))
                video_converter(user_in2)
                option = 0

            case 3:
                create4video()
                option = 0

            # Case 4 is to call the visual interface
            case 4:
                import VisualInterface
                option = 0

            case default:
                sys.exit()

