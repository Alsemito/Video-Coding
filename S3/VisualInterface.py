import PySimpleGUI as sg
import ffmpeg

# Got almost all the ideas in the code from the following site
# https://realpython.com/pysimplegui-python/

sg.theme("DarkBlue")


obtain_file = [
    [sg.In(size=(25, 1), enable_events=True, key="-VIDEO-"),
     sg.FileBrowse(),
     sg.Button("Submit")
     ],
]

resolution_button_list = [
    [
        sg.Button("160x120p", key="160p"),
        sg.Button("360x240p", key="360p"),
        sg.Button("480p", key="480p"),
        sg.Button("720p", key="720p"),
    ],
]

codec_button_list = [
    [
        sg.Button("VP8", key="-VP8-"),
        sg.Button("VP9", key="-VP9-"),
        sg.Button("H.265", key="-H.265-"),
        sg.Button("AV1", key="-AV1-"),
    ],
]

layout = [
    [sg.Frame("Chose file", obtain_file)],
    [sg.Frame("Chose a resolution", resolution_button_list)],
    [sg.Frame("Chose a video codec", codec_button_list)],
    [sg.Button("Exit", key="-EXIT-")],
]


def _160p():
    ffmpeg.input(video).filter("scale", 160, 120).output("Output_160x120p.mp4").run()


window = sg.Window('Video converter', layout, size=(400, 250), resizable=True)

while True:  # Event Loop
    event, values = window.Read()

    if event == sg.WIN_CLOSED or event == "-EXIT-":
        window.Close()
    elif event == "Submit":
        video = values["-VIDEO-"]
    elif event == "160p":
        _160p()

