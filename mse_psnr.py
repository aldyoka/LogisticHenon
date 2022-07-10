from math import log10, sqrt
# import cv2
import numpy as np
from PIL import Image

def PSNR(original, compressed):
    mse = np.mean((original - compressed) ** 2)
    print(mse)
    if mse == 0:  # MSE is zero means no noise is present in the signal .
        # Therefore PSNR have no importance.
        return 100
    max_pixel = 255.0
    psnr = 20 * log10(max_pixel / sqrt(mse))
    return psnr


def main():
    img1 = Image.open("images/dumy/astronot.png", 'r')
    print(img1.mode)
    img2 = Image.open("images/dumy/5-astronot.png", 'r')
    print(img2.mode)
    original = np.array(list(img1.getdata()))
    compressed = np.array(list(img2.getdata()))
    # original = cv2.imread("images/olenna.png")
    # compressed = cv2.imread("images/Lenna.png", 1)
    value = PSNR(original, compressed)
    print(f"PSNR value is {value} dB")

main()


# import numpy as np
# import cv2
# import math
#
#
# def pengujian(var1, var2):
#     mse = np.mean((var1 - var2) ** 2)
#     file = open('mse.txt', "w+")
#     file.write(str(mse))
#     file.close()
#     print(mse)
#
#     if mse == 0:
#         psnr = 'inf'
#         file = open('psnr.txt', "w+")
#         file.write(str(psnr))
#         print(psnr)
#     else:
#         psnr = 20 * math.log10(255.0 / math.sqrt(mse))
#         file = open('psnr.txt', "w+")
#         file.write(str(psnr))
#         print(psnr)
#     file.close()
#
#
# img = cv2.imread('images/Lenna.png')
# img1 = cv2.imread('images/Lenna_10.png')
#
# pengujian(img, img1)
