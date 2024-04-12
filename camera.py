import cv2
import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk
from datetime import datetime
from tkinter import messagebox, filedialog

root = tk.Tk()
root.title("Pycam")
root.geometry("1280x1024")
root.configure(background="sky blue")

destPath = StringVar()
imagepath = StringVar()
cap = cv2.VideoCapture(0)
width, height = 640, 480
cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

def createwidgets():
    feedlabel = Label(root, bg="steelblue", fg="white", text="Webcam Feed", font=('comic sans ms', 20))
    feedlabel.grid(row=1, column=1, padx=10, pady=10, columnspan=2)

    global cameralabel
    cameralabel = Label(root, bg="steelblue", borderwidth=3, relief=GROOVE)
    cameralabel.grid(row=2, column=1, padx=10, pady=10, columnspan=2)

    saveEntry = Entry(root, width=55, textvariable=destPath)
    saveEntry.grid(row=3, column=1, padx=10, pady=10)

    browseBtn = Button(root, text="Browse", width=10, command=destBrowse)
    browseBtn.grid(row=3, column=2, padx=10, pady=10)

    captureBtn = Button(root, text="Capture", command=capture, bg="lightblue", font=("comic sans ms", 15), width=20)
    captureBtn.grid(row=4, column=1, padx=10, pady=10)

    global cameraBtn
    cameraBtn = Button(root, text="Stop Camera", command=stopcam, bg="lightblue")
    cameraBtn.grid(row=4, column=2, padx=10, pady=10)

    previewlabel = Label(root, text="Image Preview", bg="steelblue", fg="white", font=("comic sans ms", 20))
    previewlabel.grid(row=1, column=4, padx=10, pady=10, columnspan=2)

    global imagelabel
    imagelabel = Label(root, bg="steelblue", borderwidth=3, relief=GROOVE)
    imagelabel.grid(row=2, column=4, padx=10, pady=20, columnspan=2)

    openImageEntry = Entry(root, width=55, textvariable=imagepath)
    openImageEntry.grid(row=3, column=4, padx=10, pady=10)

    openImageBtn = Button(root, width=10, text="Browse", command=imagebrowse)
    openImageBtn.grid(row=3, column=5, padx=10, pady=10)

    startcam()  # Automatically start the camera feed

def showfeed():
    ret, frame = cap.read()

    if ret:
        frame = cv2.flip(frame, 1)
        cv2.putText(frame, datetime.now().strftime('%d/%m/%y %H:%M:%S'), (20, 30), cv2.FONT_HERSHEY_DUPLEX, 0.5, (0, 255, 255))
        cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)

        img = Image.fromarray(cv2image)
        imgtk = ImageTk.PhotoImage(image=img)
        cameralabel.imgtk = imgtk
        cameralabel.configure(image=imgtk)
        cameralabel.after(10, showfeed)

def destBrowse():
    destDir = filedialog.askdirectory(initialdir="Your directory path")
    destPath.set(destDir)

def capture():
    if destPath.get() != "":
        imageName = datetime.now().strftime('%d-%m-%y %H-%M-%S') + ".jpg"
        imagePath = destPath.get() + '/' + imageName

        ret, frame = cap.read()
        cv2.putText(frame, datetime.now().strftime('%d/%m/%y %H:%M:%S'), (20, 30), cv2.FONT_HERSHEY_DUPLEX, 0.5, (0, 255, 255))

        success = cv2.imwrite(imagePath, frame)
        if success:
            messagebox.showinfo("Success", "Image saved at " + imagePath)

            # Display captured image in imagelabel
            savedimg = Image.open(imagePath)
            savedimg = ImageTk.PhotoImage(savedimg)
            imagelabel.configure(image=savedimg)
            imagelabel.image = savedimg
    else:
        messagebox.showerror("Error", "You need to select a directory!")

def stopcam():
    global cameraBtn
    if cap.isOpened():
        cap.release()
    cameraBtn.config(text="Start Camera", command=startcam)
    cameralabel.config(text="Off Camera", font=("comic sans ms", 70))

def startcam():
    global cameraBtn
    cap.open(0)  # Re-open the camera
    cameraBtn.config(text="Stop Camera", command=stopcam)
    cameralabel.config(text="")  # Clear camera label text
    showfeed()  # Start showing the webcam feed

def imagebrowse():
    opendir = filedialog.askopenfilename(initialdir="Your directory path")
    imagepath.set(opendir)

    imageview = Image.open(opendir)
    imageresize = imageview.resize((640, 480), Image.ANTIALIAS)
    imagedisplay = ImageTk.PhotoImage(imageresize)
    imagelabel.configure(image=imagedisplay)
    imagelabel.image = imagedisplay

createwidgets()
root.mainloop()