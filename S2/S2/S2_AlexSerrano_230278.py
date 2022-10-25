import os
import sys
import subprocess


def cutN_video(inPath: str, n1: int, n2: int, outPath: str):
    # Command to cut the specified video. n1 is the second (s) from the original video that is going to be the start
    # of the new one, and n2 is the length of the new video
    os.system("ffmpeg -i " + inPath + " -ss " + str(n1) + " -t " + str(n2) + " -async 1 " + outPath)
    return


def extractYUV(inPath: str):
    # Command to extract the histogram of the video in YUV values. Using subprocess as I couldn't find one using
    # os that worked for windows. We are using colorchannelmixer to apply some transparency to the histogram
    subprocess.call(["ffmpeg", "-i", inPath, "-vf", "split=2[a][b],[b]histogram, scale=100:230," "format=yuva444p ,"
                                                    "colorchannelmixer=aa=0.7[hh], [a][hh]overlay", "histogram.mp4"])
    return -1


def video_scaler(inPath: str):
    # Allow the user to select the resolution
    choice = int(input("1 - 720p\n"
                       "2 - 480p\n"
                       "3 - 360x240\n"
                       "4 - 160x120\n"
                       ""))
    # Apply only one at a time so that the process is not always resizing 4 videos
    if choice == 1:
        os.system("ffmpeg -i " + inPath + " -vf scale=1280:720 output_720p.mp4")
    elif choice == 2:
        os.system("ffmpeg -i " + inPath + " -vf scale=640:480 output_480p.mp4")
    elif choice == 3:
        os.system("ffmpeg -i " + inPath + " -vf scale=360:240 output_360x240p.mp4")
    elif choice == 4:
        os.system("ffmpeg -i " + inPath + " -vf scale=160:120 output_160x120p.mp4")
    else:
        print("Select a correct option")
    return -1


def stereo_mono(inPath: str):
    # Same as before, allow the user to select which process he/she wants to take
    choice = int(input("1 - From mono to stereo\n"
                       "2 - From stereo to mono\n"
                       ""))
    if choice == 1:
        os.system("ffmpeg -i " + inPath + " -ac 2 output_stereo.mp4")
    elif choice == 2:
        os.system("ffmpeg -i " + inPath + " -ac 1 output_mono.mp4")
    else:
        print("Select a correct option")
    return -1


loop = 1
if __name__ == '__main__':
    option = 0
    while loop != 0:
        # Start a loop until the user decides to end it
        match option:
            # The user is allowed to navigate through all the exercises without the need of the code
            case 0:
                option = int(input('0 - Navigate by typing the number of the exercise:\n'
                                   '1 - Cut N seconds from an input video\n'
                                   '2 - Extract the YUV values from an mp4 video\n'
                                   '3 - Resize the input video to 720p, 480p, 360x240 and 160x120\n'
                                   '4 - Convert the video output audio from mono to stereo or vice versa\n'
                                   '5 - Exit\n'
                                   ''))
            case 1:
                # In order for this to work with another video, the path in the cutN_video function needs to change
                user_in1 = str(input("Enter the name of the video (with its extension, e.g. .mp4): "))
                user_in2 = int(
                    input(str("Enter a value (in seconds) from the original file to start the new clip from: ")))
                user_in3 = int(input(str("Select the wanted length of the video (in seconds): ")))
                user_in4 = str(input(str("How do you wanna call the output file (don't forget the extension!)? ")))

                cutN_video(user_in1, user_in2, user_in3, user_in4)
                print('File saved in the same directory as the original one')
                option = 0

            case 2:
                user_in1 = str(input("Enter the name of the video (with its extension, i.e. .mp4): "))
                extractYUV(user_in1)
                print('File saved in the same directory as the original one')
                option = 0

            case 3:
                user_in1 = str(input("Enter the name of the video (with its extension, i.e. .mp4): "))
                video_scaler(user_in1)
                print('File saved in the same directory as the original one')
                option = 0

            case 4:
                user_in1 = str(input("Enter the name of the video (with its extension, i.e. .mp4): "))
                stereo_mono(user_in1)
                print('File saved in the same directory as the original one')
                option = 0

            case default:
                sys.exit()
