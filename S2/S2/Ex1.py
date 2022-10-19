import os


def cutN_video(n1: int, n2: int):
    os.system("ffmpeg -i BBB.mp4 -ss " + str(n1) + " -t " + str(n2) + " -async 1 cut.mp4")
    return


# Press the green button in the gutter to run the script.
loop = 1
if __name__ == '__main__':
    option = 0
    while loop != 0:
        match option:
            case 0:
                option = input(int('0 - Start\n'
                                   '1 - Cut N seconds from a video\n'
                                   ''))

            case 1:
                user_in1 = input()

    cutN_video(3, 3)
