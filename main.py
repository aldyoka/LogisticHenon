import enkrip_dekrip
import numpy as np
from PIL import Image, ImageTk
import tkinter as tk
from tkinter.filedialog import askopenfile
import time


def create_image(pixel, width, height, ket, path):
    pixel = pixel.reshape(height, width, 4)
    array = np.array(pixel, dtype=np.uint8)
    new_image = Image.fromarray(array)
    name_image = "".join(path.split(".")[:-1])

    if ket == 0:
        new_image.save(name_image + "-enc.png")
        path_new = name_image + "-enc.png"
        show_hasil(path_new)
    elif ket == 1:
        new_image.save(name_image + "-dec.png")
        path_new = name_image + "-dec.png"
        show_hasil(path_new)


def get_pixel(path, pil, publik_key, private_key):
    img = Image.open(path, 'r')
    width, height = img.size
    array_pixel = np.array(list(img.getdata()))
    start_time = time.time()

    if img.mode == 'RGB':
        array_pixel = np.insert(array_pixel, 3, 255, axis=1)

    size = array_pixel.size

    if pil == 1:
        # ------------------------------enkripsi 1------------------------------------------------------
        cipher_pixel = enkrip_dekrip.enkripsi_1(publik_key, private_key, size, array_pixel)
        # maximum key falue adalah 10^-16
        create_image(cipher_pixel, width, height, 0, path)
        print("--- %s seconds ---" % (time.time() - start_time))

    elif pil == 2:
        # -------------------------------dekripsi 2-------------------------------------------------------
        plain_pixel = enkrip_dekrip.dekripsi_2(publik_key, private_key, size, array_pixel)
        create_image(plain_pixel, width, height, 1, path)
        print("--- %s seconds ---" % (time.time() - start_time))


# ============================================= GUI ===============================================
root = tk.Tk()
root.geometry('+%d+%d' % (350, 10))

header = tk.Frame(root, width=900, height=250, bg="#6AF2F0")
header.grid(columnspan=3, rowspan=2, row=0)

body = tk.Frame(root, width=900, height=75, bg="#6AF2F0")
body.grid(columnspan=3, rowspan=2, row=3)

# input pin
text2 = tk.Label(root, text="silahkan masukan pin anda maximal 16 :", font=("Century Gothic", 11), bg="#6AF2F0")
text2.grid(column=0, row=3, sticky=tk.SW, padx=10, pady=0)
entry_key = tk.Entry(root, width=50)
entry_key.grid(column=0, row=4, sticky=tk.NW, padx=10, pady=0)

main_content = tk.Frame(root, width=900, height=350, bg="#04D4F0")
main_content.grid(columnspan=3, rowspan=2, row=5)


def open_image():
    button_text.set("Loading....")
    img = askopenfile(parent=root, mode="rb", title="pilih file gambar", filetypes=[("Image file", "*.png *.jpg")])
    if img:
        file = Image.open(img)
        if int(file.size[1]) > 512 or int(file.size[1]) > 512:
            warn_window(1, 0, 0, 0, 0)

        else:
            file = file.resize((int(file.size[0] * 0.5), int(file.size[1] * 0.5)))
            file = ImageTk.PhotoImage(file)
            file_label = tk.Label(image=file, bg="white")
            file_label.image = file
            file_label.grid(row=5, column=0, rowspan=2)

            button_text.set("Browse")
            path = img.name

            button_text_1 = tk.StringVar()
            button_btn_1 = tk.Button(root, textvariable=button_text_1, font=("Century Gothic", 12),
                                     command=lambda: input_key(path, 1), bg="#059DC0", fg="#6AF2F0", height=1, width=15)
            button_text_1.set("Enkripsi")
            button_btn_1.grid(rowspan=2, column=1, row=3)

            button_text_2 = tk.StringVar()
            button_btn_2 = tk.Button(root, textvariable=button_text_2, font=("Century Gothic", 12),
                                     command=lambda: input_key(path, 2), bg="#059DC0", fg="#6AF2F0", height=1, width=15)
            button_text_2.set("Dekripsi")
            button_btn_2.grid(rowspan=2, column=2, row=3)


def warn_window(status, path, pilihan, publik_key, private_key):
    warn = tk.Tk()
    warn.geometry("300x100")
    if status == 1:
        warn_label = tk.Label(warn, text="Eror, file terlalu besar !", font=("Century Gothic", 14))
        warn_label.pack(pady=20)
        button_text.set("Browse")
    elif status == 2:
        warn_label = tk.Label(warn, text="kunci anda melebihi 16 character !", font=("Century Gothic", 14))
        warn_label.pack(pady=20)
    elif status == 3:
        warn_label = tk.Label(warn, text="kunci anda kosong !", font=("Century Gothic", 14))
        warn_label.pack(pady=20)
    else:
        warn_label = tk.Label(warn, text="Proses, jangan close aplikasi.", font=("Century Gothic", 14))
        warn_label.pack(pady=20)
        get_pixel(path, pilihan, publik_key, private_key)


def show_hasil(path):
    file = Image.open(path)
    file = file.resize((int(file.size[0] * 0.5), int(file.size[1] * 0.5)))
    file = ImageTk.PhotoImage(file)
    file_label = tk.Label(image=file, bg="#20bebe")
    file_label.image = file
    file_label.grid(row=5, column=2, rowspan=2)


def input_key(path, pilihan):
    enter_key = entry_key.get()
    list_of_key = []
    for i in enter_key:
        list_of_key.append(ord(i))
    publik_key = sum(list_of_key)
    publik_key = float(publik_key)
    publik_key = publik_key / pow(10, 16)

    if publik_key >= 1:
        warn_window(2, 0, 0, 0, 0)

    elif publik_key == 0:
        warn_window(3, 0, 0, 0, 0)

    elif publik_key < 1:

        x = publik_key
        private_key = 0
        for i in range(5):
            private_key = 3.65 * x * (1 - x)
            x = private_key

        # print('%.16f' % publik_key, '%.16f' % private_key)
        warn_window(4, path, pilihan, publik_key, private_key)
        # get_pixel(path, pilihan, publik_key, private_key)


def display_logo(url, row, column):
    img = Image.open(url)
    # resize image
    img = img.resize((int(img.size[0] / 1.5), int(img.size[1] / 1.5)))
    img = ImageTk.PhotoImage(img)
    img_label = tk.Label(image=img, bg="#6AF2F0")
    img_label.image = img
    img_label.grid(column=column, row=row, rowspan=2, sticky=tk.NW, padx=20, pady=40)


display_logo('logo.png', 0, 0)

instructions = tk.Label(root, text="Silahkan masukan gambar anda", font=("Century Gothic", 10), bg="#6AF2F0")
instructions.grid(column=2, row=0, sticky=tk.SE, padx=50, pady=5)

button_text = tk.StringVar()
button_btn = tk.Button(root, textvariable=button_text, command=lambda: open_image(), font=("Century Gothic", 14),
                       bg="#059DC0", fg="white", height=1, width=15)
button_text.set("Browse")
button_btn.grid(column=2, row=1, sticky=tk.NE, padx=75)

root.mainloop()
