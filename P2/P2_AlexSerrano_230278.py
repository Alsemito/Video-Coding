import os
import sys
import subprocess


def extract_codec_info(inPath: str):
    loop1 = 0
    # Loop to be able to select multiple options without the need of entering a new path, when Go back is selected,
    # the function finishes and returns to the main menu
    while loop1 != 1:
        info = int(input("\nSelect the information that you want to extract:\n"
                         "1 - Video codec(s)\n"
                         "2 - Audio codec(s)\n"
                         "3 - General information in the container\n"
                         "4 - Go back\n"))
        if info == 1:
            # Extract only information about the video codec(s)
            os.system("ffprobe " + inPath + " 2>&1 >/dev/null | grep Stream.*Video")
        elif info == 2:
            # Extract only the information about the audio codec(s)
            os.system("ffprobe " + inPath + " 2>&1 >/dev/null | grep Stream.*Audio")
        elif info == 3:
            # Extract the information about the whole container
            os.system("ffprobe " + inPath)
        else:
            loop1 = 1


def create_new_container(inPath: str):
    # First of all, cut the video to 1 minute and save it
    os.system("ffmpeg -i " + inPath + " -ss 0 -t 60 -c copy -map 0 1min_aux.mp4")

    # Extract the audio in .mp3 and .aac
    os.system("ffmpeg -i 1min_aux.mp4 -q:a 0 -map a 1min_audio.mp3")
    os.system("ffmpeg -i 1min_audio.mp3 -c:a aac -b:a 128k 1min_audio.aac")  # We reduced the bitrate to 128kb/s

    # Remove audio codec from the original 1-minute video and remove such video
    os.system("ffmpeg -i 1min_aux.mp4 -c copy -an 1min.mp4")
    os.remove("1min_aux.mp4")

    # We are now set with a video file without audio, and two audio files. Let us proceed to wrap them all up
    os.system("ffmpeg -i 1min.mp4 -i 1min_audio.mp3 -i 1min_audio.aac \
       -map 0 -map 1 -map 2 -codec copy newContainer.mp4")

    # Delete all the extra files once the container has been created
    os.remove("1min.mp4")
    os.remove("1min_audio.aac")
    os.remove("1min_audio.mp3")
    return -1


class Exercise3:
    # Create a class for exercise 3 (as a different approach like stated at the end of the assignment)
    def __init__(self, path_: str, extension_: str, size_: str):
        self.path_ = path_
        self.extension_ = extension_
        self.size_ = size_

    def resize(self):
        # For a video or image the command is the same, so we don't need a subclass for them
        os.system("ffmpeg -i " + self.path_ + " -vf scale=" + self.size_ + " resized_output." + self.extension_)


class Audio(Exercise3):
    # We do need a subclass for an audio file as the command to change the bitrate is different from the one above
    # This part was done just for fun, to be able to "resize" audio files as well
    def resizeAudio(self):
        os.system("ffmpeg -i " + self.path_ + " -codec:a libmp3lame -b:a " + self.size_ + "k resized_output."
                  + self.extension_)


def broadcast_info(inPath: str):
    # Create a text file to parse the information of the codec(s) and extract its name(s)
    txt = open("info.txt", "w")
    subprocess.run("ffprobe -v error -select_streams a -show_entries stream=codec_name -of "
                   "default=noprint_wrappers=1 " + inPath, shell=True, stdout=txt)
    txt.close()

    # Create a list and fill it with such names
    with open("info.txt") as f:
        names = [line.rstrip() for line in f]
    os.remove("info.txt")

    # Modify the list so that we are left with the name only (instead of the previous codec_name=...)
    for i in range(len(names)):
        names[i] = names[i].split("=")[1]

    # Create a list for every broadcast standard with their accepted audio formats
    dvb = ['aac', 'ac3', 'mp3']
    isdb = ['aac']
    atsc = ['ac3']
    dtmb = ['dra', 'aac', 'ac3', 'mp2', 'mp3']
    names_list = ['DVB-T', 'ISDB-T', 'ATSC', 'DTMB']
    stds_list = [dvb, isdb, atsc, dtmb]

    # Now we can finally check in which broadcast standards the video can be in
    print('\nYour video can fit in the following standards:')
    for i in range(len(stds_list)):
        if all(elem in stds_list[i] for elem in names):
            print(names_list[i])
    return -1


# Press the green button in the gutter to run the script.
loop = 1
if __name__ == '__main__':
    option = 0
    while loop != 0:
        match option:
            case 0:
                option = int(input("\nNavigate through the exercises: \n"
                                   "1 - Extract the container's information\n"
                                   "2 - Create a new container\n"
                                   "3 - Resize your file\n"
                                   "4 - Show in which broadcast standard your video can fit, depending on its audio\n"
                                   "5 - Exit\n"
                                   ""))
            case 1:
                user_in1 = str(input("\nEnter the path of the video file (container) with its extension (e.g. .mp4): "))
                extract_codec_info(user_in1)
                option = 0

            case 2:
                user_in2 = str(input("\nEnter the path of the video file (container) with its extension (e.g. .mp4): "))
                create_new_container(user_in2)
                option = 0

            case 3:
                user_in3 = int(input("\nChoose the file you want to resize: \n"
                                     "1 - Image\n"
                                     "2 - Video\n"
                                     "3 - Audio\n"
                                     "4 - Go back\n"))

                if user_in3 == 4:
                    option = 0
                else:
                    path = str(input("\nEnter the path of the image file with its extension (e.g. .png): "))
                    extension = path.split(".")[1]

                    if user_in3 == 1:
                        resolution = str(input("\nEnter the desired size in the format 480:360 (w, h): "))
                        image = Exercise3(path, extension, resolution)
                        image.resize()
                        option = 3

                    elif user_in3 == 2:
                        resolution = str(input("\nEnter the desired resolution (such as 480:360): "))
                        video = Exercise3(path, extension, resolution)
                        video.resize()
                        option = 3

                    elif user_in3 == 3:
                        resolution = str(input("\nThis one is just for fun, enter the desired bitrate (the result "
                                               "will be in kbps, meaning, if you put 128, it means 128kbps): "))
                        audio = Audio(path, extension, resolution)
                        audio.resizeAudio()
                        option = 3

                    else:
                        print("Please select a correct option\n")
                        option = 4

            case 4:
                user_in4 = str(input("\nEnter the path of the video file with its extension (e.g. .mp4): "))
                broadcast_info(user_in4)
                option = 0

            case default:
                sys.exit()
