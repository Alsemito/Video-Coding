import os
import sys


def video_scaler(inPath: str):
    # Apply only one at a time so that the process is not always resizing 4 videos

    os.system("ffmpeg -i " + inPath + " -vf scale=1280:720 -c:a copy BBB_720p.mp4")
    os.system("ffmpeg -i " + inPath + " -vf scale=640:480 -c:a copy BBB_480p.mp4")
    os.system("ffmpeg -i " + inPath + " -vf scale=360:240 -c:a copy BBB_360x240p.mp4")
    os.system("ffmpeg -i " + inPath + " -vf scale=160:120 -c:a copy BBB_160x120p.mp4")

    return -1


def video_converter(inPath: str):

    os.system("ffmpeg -i " + inPath + " -c:v libvpx -b:v 1M -c:a libvorbis vp8.webm")  # VP8
    os.system("ffmpeg -i " + inPath + " -c:v libvpx-vp9 -b:v 1M -c:a libvorbis vp9.webm")  # VP9
    os.system("ffmpeg -i " + inPath + " -c:v libx265 -crf 26 -preset fast -c:a ac3 -b:a 256k h265.mp4")  # H.265
    os.system("ffmpeg -i " + inPath + " -c:v libaom-av1 -crf 26 -b:v 1M -c:a ac3 -b:a 256k av1.mkv")  # AV1


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
                                   ''))
            case 1:
                user_in1 = str(input("Enter the name of the video (with its extension, e.g. .mp4): "))
                video_scaler(user_in1)
                option = 0

            case 2:
                user_in2 = str(input("Enter the name of the video (with its extension, e.g. .mp4): "))
                video_converter(user_in2)
                option = 0

