import cv2
import os
import hashlib
from tkinter import Tk, Label, Button, Entry, StringVar, filedialog

def generate_key(passcode):
    # Use a hash function to generate a key from the passcode
    hash_object = hashlib.md5(passcode.encode())
    key = hash_object.hexdigest()
    
    # You can adjust the hash function or use a different one based on your requirements
    return key

def encrypt(img, msg, key):
    d = {}
    m, n, z = 0, 0, 0

    for i in range(255):
        d[chr(i)] = i

    for i in range(len(msg)):
        img[n, m, z] = d[msg[i]]
        n = n + 1
        m = m + 1
        z = (z + 1) % 3

def decrypt(img, key):
    c = {}
    m, n, z = 0, 0, 0
    message = ""

    for i in range(255):
        c[i] = chr(i)

    for i in range(len(key)):
        message = message + c[img[n, m, z]]
        n = n + 1
        m = m + 1
        z = (z + 1) % 3

    return message

def browse_image():
    global img_path
    img_path = filedialog.askopenfilename()
    image_label.config(text="Image Path: " + img_path)

def encrypt_image():
    global img_path
    img = cv2.imread(img_path)
    msg = message_entry.get()
    passcode = password_entry.get()

    key = generate_key(passcode)

    encrypt(img, msg, key)

    cv2.imwrite("encryptedImage.jpg", img)
    os.system("start encryptedImage.jpg")

def decrypt_message():
    global img_path
    img = cv2.imread(img_path)
    passcode = password_entry.get()

    decrypted_msg = decrypt(img, generate_key(passcode))
    decrypted_label.config(text="Decrypted message: " + decrypted_msg)

root = Tk()
root.title("Raghav's Steganography Tool")

img_path = ""

image_label = Label(root, text="Image Path:")
image_label.pack()

browse_button = Button(root, text="Browse Image", command=browse_image)
browse_button.pack()

message_label = Label(root, text="Enter secret message:")
message_label.pack()

message_entry = Entry(root)
message_entry.pack()

password_label = Label(root, text="Enter a passcode:")
password_label.pack()

password_entry = Entry(root, show="*")
password_entry.pack()

encrypt_button = Button(root, text="Encrypt", command=encrypt_image)
encrypt_button.pack()

decrypt_button = Button(root, text="Decrypt", command=decrypt_message)
decrypt_button.pack()

decrypted_label = Label(root, text="")
decrypted_label.pack()

root.mainloop()
