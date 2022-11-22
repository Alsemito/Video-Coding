import PySimpleGUI as sg
import ffmpeg

# Got almost all the ideas in the code from the following site
# https://realpython.com/pysimplegui-python/

# Sets a dark blue theme for the window
sg.theme("DarkBlue")

# Frame in which we obtain the file
obtain_file = [
    [sg.In(size=(25, 1), enable_events=True, key="-VIDEO-"),
     sg.FileBrowse(),
     sg.Button("Submit", key="Submit")
     ],
]

# Frame where we have all the buttons for our resolutions
resolution_button_list = [
    [
        sg.Button("160x120p", key="160p"),
        sg.Button("360x240p", key="360p"),
        sg.Button("480p", key="480p"),
        sg.Button("720p", key="720p"),
    ],
]

# Frame where we have all the buttons for our codecs
codec_button_list = [
    [
        sg.Button("VP8", key="-VP8-"),
        sg.Button("VP9", key="-VP9-"),
        sg.Button("H.265", key="-H.265-"),
        sg.Button("AV1", key="-AV1-"),
    ],
]

# Create the layout of our window, with all the frames previously defined
layout = [
    [sg.Frame("Chose file", obtain_file)],
    [sg.Frame("Chose a resolution", resolution_button_list)],
    [sg.Frame("Chose a video codec", codec_button_list)],
    [sg.Button("Exit", key="-EXIT-")],
]

# Create the window
window = sg.Window('Video converter', layout, size=(400, 220), resizable=True)

while True:  # Event Loop
    event, values = window.Read()

    try:
        # Function calls depending on the triggered event
        if event == sg.WIN_CLOSED or event == "-EXIT-":
            break
        elif event == "Submit":     # A submit is necessary in order to perform the transformations
            video = values["-VIDEO-"]
        elif event == "160p":
            ffmpeg.input(video).filter("scale", 160, 120).output("Output_160x120p.mp4", acodec="ac3").run()
        elif event == "360p":
            ffmpeg.input(video).filter("scale", 360, 240).output("Output_360x240p.mp4", acodec="mp3").run()
        elif event == "480p":
            ffmpeg.input(video).filter("scale", 640, 480).output("Output_480p.mp4", acodec="ac3").run()
        elif event == "720p":
            ffmpeg.input(video).filter("scale", 1280, 720).output("Output_720p.mp4", acodec="ac3").run()
        elif event == "-VP8-":
            ffmpeg.input(video).output('BBB_vp8.mkv', vcodec='libvpx', acodec="libvorbis").run()
        elif event == "-VP9-":
            ffmpeg.input(video).output('BBB_vp8.mkv', vcodec='libvpx-vp9', acodec="libvorbis").run()
        elif event == "-H.265-":
            ffmpeg.input(video).output('BBB_vp8.mkv', vcodec='libx265 ', acodec="ac3").run()
        elif event == "AV1":
            ffmpeg.input(video).output('BBB_vp8.mkv', vcodec='libaom-av1 ', acodec="ac3").run()


    except:
        print("We've got an error! Please check that the video was entered correctly")
        pass

window.close()
