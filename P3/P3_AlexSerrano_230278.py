import os
import sys


def hls_container(inPath: str):
    # Creates the HLS container following this page https://ottverse.com/hls-packaging-using-ffmpeg-live-vod/
    os.system('ffmpeg -i ' + inPath + ' \
              -filter_complex \
              "[0:v]split=3[v1][v2][v3]; \
              [v1]copy[v1out]; [v2]scale=w=1280:h=720[v2out]; [v3]scale=w=640:h=480[v3out]" \
              -map [v1out] -c:v:0 libx264 -x264-params "nal-hrd=cbr:force-cfr=1" \
              -b:v:0 5M -maxrate:v:0 5M -minrate:v:0 5M -bufsize:v:0 10M -preset slow \
              -g 48 -sc_threshold 0 -keyint_min 48 \
              -map [v2out] -c:v:1 libx264 -x264-params "nal-hrd=cbr:force-cfr=1" \
              -b:v:1 3M -maxrate:v:1 3M -minrate:v:1 3M -bufsize:v:1 3M -preset \
              slow -g 48 -sc_threshold 0 -keyint_min 48 \
              -map [v3out] -c:v:2 libx264 -x264-params "nal-hrd=cbr:force-cfr=1" '
              '-b:v:2 1M -maxrate:v:2 1M -minrate:v:2 1M -bufsize:v:2 1M '
              '-preset slow -g 48 -sc_threshold 0 -keyint_min 48 \
              -map a:0 -c:a:0 ac3 -b:a:0 96k -ac 2 \
              -map a:0 -c:a:1 ac3 -b:a:1 96k -ac 2 \
              -map a:0 -c:a:2 ac3 -b:a:2 48k -ac 2 \
              -f hls \
              -hls_time 10 \
              -hls_playlist_type vod \
              -hls_flags independent_segments \
              -hls_segment_type mpegts \
              -hls_segment_filename stream_%v/data%02d.ts \
              -master_pl_name master.m3u8 \
              -var_stream_map "v:0,a:0 v:1,a:1 v:2,a:2" stream_%v.m3u8')


def info(inPath:str):
    # Show video information to check if the video needs to be segmented or not
    os.system("mp4info " + inPath)


def fragment(inPath:str):
    # Fragment the video so that we can create the MPD file
    os.system("mp4fragment --fragment-duration 2000 " + inPath + " fragmented_video.mp4")



def mpd():
    # Create the encrypted MPD file (We are just doing it for the BBB video in this case)
    os.system("mp4dash --mpd-name myvideo.mpd --encryption-key=" 
              "121a0fca0f1b475b8910297fa8e0a07e:a0a1a2a3a4a5a6a7a8a9aaabacadaeaf "
              "--use-segment-timeline BBB_1080p_frag.mp4 BBB_720p_frag.mp4 BBB_360p_frag.mp4")



def live_stream(inPath: str):
    os.system("ffmpeg -re -i " + inPath + " -c copy -f mpegts udp://192.168.2.10:1234")


loop = 1
if __name__ == '__main__':
    option = 0
    while loop != 0:
        # Start a loop until the user decides to end it
        match option:
            # The user is allowed to navigate through all the exercises without the need of the code
            case 0:
                option = int(input('\n0 - Navigate by typing the number of the exercise:\n'
                                   '1 - Create an HLS transport stream container\n'
                                   '2 - Display the information of your video (maybe to see if it needs fragmentation)\n'
                                   '3 - Fragment your video\n'
                                   '4 - Create the encrypted MPD file\n'
                                   '5 - Livestream your video\n'
                                   '6 - Exit\n'))

            case 1:
                user_in1 = str(input("Enter the name of the video (with its extension, e.g. .mp4): "))
                hls_container(user_in1)
                option = 0

            case 2:
                user_in2 = str(input("Enter the name of the video (with its extension, e.g. .mp4): "))
                info(user_in2)
                option = 0

            case 3:
                user_in3 = str(input("Enter the name of the video (with its extension, e.g. .mp4): "))
                fragment(user_in3)
                option = 0

            case 4:
                mpd()
                option = 0

            case 5:
                user_in5 = str(input("Enter the name of the video (with its extension, e.g. .mp4): "))
                live_stream(user_in5)
                option = 0

            case default:
                sys.exit()

