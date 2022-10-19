from collections import OrderedDict
import numpy as np


# EXERCISE 1
def rgb_yuv(r: float, g: float, b: float):
    # Compute YUV coordinates from the given RGB coordinates
    y = 0.257 * r + 0.504 * g + 0.098 * b + 16
    u = -0.148 * r - 0.291 * g + 0.439 * b + 128
    v = 0.439 * r - 0.368 * g - 0.071 * b + 128

    return y, u, v


def yuv_rgb(y: float, u: float, v: float):
    # Compute RGB coordinates from the given YUV coordinates
    r = 1.164 * (y - 16) + 1.596 * (v - 128)
    g = 1.164 * (y - 16) - 0.813 * (v - 128) - 0.391 * (u - 128)
    b = 1.164 * (y - 16) + 2.018 * (u - 128)

    return r, g, b


# EXERCISE 4
# Code found at https://www.geeksforgeeks.org/run-length-encoding-python/
def run_length(s: list):
    # Generate ordered dictionary of all lower
    # case alphabets, its output will be
    # dict = {'w':0, 'a':0, 'd':0, 'e':0, 'x':0}
    dict = OrderedDict.fromkeys(s, 0)

    # Now iterate through input string to calculate
    # frequency of each character, its output will be
    # dict = {'w':4,'a':3,'d':1,'e':1,'x':6}
    for ch in s:
        dict[ch] += 1

    # now iterate through dictionary to make
    # output string from (key,value) pairs
    output = ''
    for key, value in dict.items():
        output = output + key + str(value)
    return output


# EXERCISE 5
# This function and the next one were done using some help from a GitHub repository that talked
# about the DCT and IDCT in 1D and 2D. I just chose to stick to the 1D version
def dct1D(im):
    n = len(im)
    F = np.zeros(n)
    # Here we just compute the DCT in 1D adapting the 2D formula given in class
    for i in range(n):
        for x in range(n):
            F[i] += im[x] * np.cos((np.pi * (2 * x + 1) * i) / (2 * n))
        if i == 0:
            alpha_i = np.sqrt(1 / n)
        else:
            alpha_i = np.sqrt(2 / n)

        F[i] *= alpha_i

    return F


def idct1D(im):
    n = len(im)
    f = np.zeros(n)
    # Here we just compute the inverse DCT in 1D adapting the 2D formula given in class
    for x in range(n):
        for i in range(n):
            if i == 0:
                alpha_i = np.sqrt(1 / n)
            else:
                alpha_i = np.sqrt(2 / n)
            f[x] += alpha_i * im[i] * np.cos((np.pi * (2 * x + 1) * i) / (2 * n))
    return f


loop = 1
if __name__ == '__main__':
    # Just an interactive main so that is easier to perform all the tasks at once without changing any code
    option = 0
    while loop != 0:
        match option:
            case 0:
                option = int(input('Select an option: \n'
                                   '0 - Start\n'
                                   '1 - RGB to YUV\n'
                                   '2 - YUB to RGB \n'
                                   '3 - Run-length algorithm\n'
                                   '4 - Encode an array using the DCT\n'
                                   '5 - Decode an array using the iDCT\n'
                                   '9 - Exit\n'
                                   ''))
            case 1:
                user_in1 = input('Enter 3 space-separated numbers: ')
                RGB_tuple = tuple(float(item) for item in user_in1.split())
                if len(RGB_tuple) != 3:
                    print('Enter 3 values please')
                else:
                    result1 = rgb_yuv(RGB_tuple[0], RGB_tuple[1], RGB_tuple[2])
                    print('Your RGB coordinates in YUV are: ', result1)
                    option = 0

            case 2:
                user_in2 = input('Enter 3 space-separated numbers: ')
                RGB_tuple = tuple(float(item) for item in user_in2.split())
                if len(RGB_tuple) != 3:
                    print('Enter 3 values please')
                else:
                    result2 = yuv_rgb(RGB_tuple[0], RGB_tuple[1], RGB_tuple[2])
                    print('Your YUV coordinates in RGB are: ', result2)
                    option = 0

            case 3:
                user_in3 = input('Enter a string of characters: ')
                userList = []
                userList[:0] = user_in3
                result3 = run_length(userList)
                print('Your input has been encoded as follows: ', result3)
                option = 0

            case 4:
                user_in4 = input('Enter space-separated numbers: ')
                userList = tuple(float(item) for item in user_in4.split())
                print('Your encoded sequence is: ', dct1D(userList))
                option = 0

            case 5:
                user_in5 = input('Enter space-separated numbers: ')
                userList = tuple(float(item) for item in user_in5.split())
                print('Your decoded sequence is: ', idct1D(userList))
                option = 0

            case 9:
                end = input('Wanna quit? [Y] [N]: ')
                if end == 'Y':
                    loop = 0
                elif end != 'Y' and end != 'N':
                    print('Guess you dont :)')
                    option = 0
                else:
                    option = 0
