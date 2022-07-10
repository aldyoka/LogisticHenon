import numpy as np


# ============================================== logistik map ====================================================
def enkripsi_1(key1, key2, size, pixel):
    r = 3.95
    count = 0
    x = key1
    flat_pixel = pixel.ravel()
    array_bantu = []

    for i in range(size):
        array_bantu.append(-1)

    while count in range(size):

        x = r * x * (1 - x)  # logistik Map
        temp = int((x * pow(10, 16)) % size)  # merubah angka menjadi decimal

        if array_bantu[temp] == -1:
            array_bantu[temp] = flat_pixel[count]

        else:
            count -= 1

        count += 1
    cipher_pixel = np.array(list(enkripsi_2(key1, key2, size, array_bantu)))
    cipher_pixel = cipher_pixel.reshape((int(size/4), 4))
    return cipher_pixel


def dekripsi_1(key1, size, flat_pixel):
    r = 3.95
    count = 0
    x = key1
    array_bantu = []
    array_temp = []

    for i in range(size):
        array_bantu.append(-1)

    for i in range(size):
        array_temp.append(-1)

    while count in range(size):

        x = r * x * (1 - x)  # logistik Map
        temp = int((x * pow(10, 16)) % size)  # merubah angka menjadi decimal

        if array_temp[temp] == -1:
            array_bantu[count] = flat_pixel[temp]
            array_temp[temp] = temp
        else:
            count -= 1

        count += 1

    return array_bantu


# ==================================== end logistik map =======================================================

# ==================================== henon map ==============================================================
def enkripsi_2(key1, key2, size, pixel):
    x = key1
    y = key2
    kontrol = []
    array_bantu = []
    count = 0

    for i in range(size):
        array_bantu.append(-1)

    while count in range(size):

        x1 = 1 - 1.4 * x * x + y
        y1 = 0.3 * x

        x = x1
        y = y1

        k1 = int((x1 * pow(10, 16)) % size)
        k2 = int((y1 * pow(10, 16)) % 255)

        if array_bantu[k1] == -1:
            array_bantu[k1] = k2

        else:
            count -= 1

        kontrol.append(k1)
        count += 1

    for i in range(size):
        pixel[i] = pixel[i] ^ array_bantu[i]

    return pixel


def dekripsi_2(key1, key2, size, matrix_pixel):
    x = key1
    y = key2
    pixel = matrix_pixel.ravel()
    kontrol = []
    array_bantu = []
    count = 0

    for i in range(size):
        array_bantu.append(-1)

    while count in range(size):

        x1 = 1 - 1.4 * x * x + y
        y1 = 0.3 * x

        x = x1
        y = y1

        k1 = int((x1 * pow(10, 16)) % size)
        k2 = int((y1 * pow(10, 16)) % 256)

        if array_bantu[k1] == -1:
            array_bantu[k1] = k2

        else:
            count -= 1

        kontrol.append(k1)
        count += 1

    for i in range(size):
        pixel[i] = pixel[i] ^ array_bantu[i]

    plain_pixel = np.array(list(dekripsi_1(key1, size, pixel)))
    plain_pixel = plain_pixel.reshape((int(size/4), 4))
    return plain_pixel
# ==================================== end henon map ==============================================================
