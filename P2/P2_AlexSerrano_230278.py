import os
import sys
import subprocess


def extract_codec_info(inPath: str):
    info = int(input("\nSelect the information that you want to extract:\n"
                     "1 - Video codec(s)\n"
                     "2 - Audio codec(s)\n"
                     "3 - General information in the container\n"))
    if info == 1:
        # Extract only information about the video codec
        os.system("ffprobe " + inPath + " 2>&1 >/dev/null | grep Stream.*Video")
    elif info == 2:
        # Extract only the information about the audio codec
        os.system("ffprobe " + inPath + " 2>&1 >/dev/null | grep Stream.*Audio")
    else:
        # Extract the information about the whole container
        os.system("ffprobe " + inPath)
    return -1


def create_new_container(inPath: str):
    # First of all, cut the video to 1 minute and save it
    os.system("ffmpeg -i " + inPath + " -ss 0 -t 60 -c copy -map 0 1min_aux.mp4")

    # Extract the audio in .mp3 and .aac
    os.system("ffmpeg -i 1min_aux.mp4 -q:a 0 -map a 1min_audio.mp3")
    os.system("ffmpeg -i 1min_aux.mp4 -q:a 0 -map a 1min_audio_aux.aac")
    os.system("ffmpeg -i 1min_audio_aux.aac -ss 0 -t 60 -c copy 1min_audio.aac")
    os.remove("1min_audio_aux.aac")

    # Remove audio codec from the original 1-minute video and remove such video
    os.system("ffmpeg -i 1min_aux.mp4 -c copy -an 1min.mp4")
    os.remove("1min_aux.mp4")

    # We are now set with a video file without audio, and two audio files. Let us proceed to wrap them all up
    # os.system("ffmpeg -i 1min.mp4 -i 1min_audio.mp3 -i 1min_audio.aac -c:v copy -c:a copy -f mp4 newContainer.mp4")
    os.system("ffmpeg -i 1min.mp4 -i 1min_audio.mp3 -i 1min_audio.aac -codec copy newContainer.mp4")


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
                                   ""))
            case 1:
                user_in1 = str(input("\nEnter the path of the video file (container) with its extension (e.g. .mp4): "))
                extract_codec_info(user_in1)
                option = 0

            case 2:
                user_in1 = str(input("\nEnter the path of the video file (container) with its extension (e.g. .mp4): "))
                create_new_container(user_in1)
                option = 0
