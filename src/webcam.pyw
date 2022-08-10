# Import required Libraries
from tkinter import *
from PIL import Image, ImageTk
import cv2
import time
import numpy as np
from idlelib.tooltip import Hovertip
import tkinter
import PIL
import tkinter.filedialog
import os
import subprocess
import multiprocessing 


subprocess.Popen(["pyw", "daemon.pyw"], shell=True)



def task():
    while True:
          try:
                f = open("proc_run.txt", "r")
          except:
                time.sleep(0.01)
                f = open("proc_run.txt", "r")
          if f.read() == "true":
                break
          elif f.read() == "":
                print("nothing")
          else:
                print("not yet")
    f.close()
    root.destroy()


root = tkinter.Tk()
root.title("Loading....")

label = tkinter.Label(root, text="""Loading BackDrop, do not close this window.
This window is just loading, not freezing. Do not close this window.""", font=("Verdana", 15))
label.pack()

root.geometry("700x50")

root.after(100, task)
root.mainloop()

print("Main loop is now over and we can do other stuff.")

# Create an instance of TKinter Window or frame
win = tkinter.Tk()
win.configure(background="grey9")
# Set the size of the window
win.geometry("1200x700")

f = open("preview_condition.txt", "w")
f.write("save")
f.close()

f = open("segmentation.txt", "w")
f.write("true")
f.close()
        
# Create a Label to capture the Video frames
label =Label(win)
label.grid(row=0, column=0)

global top1, top2
top, top2 = 1, 2

def change_pic():

    global top
    top = top + 1
    
    global photo1
    if top % 2 == 0:

        try:
            f = open("preview_condition.txt", "w")
        except:
            time.sleep(0.1)
            f = open("preview_condition.txt", "w")
        f.write("stop")
        f.close()
        photo1 = ImageTk.PhotoImage(Image.open("Untitled-2--1-.png"))

    else:

        try:
            f = open("preview_condition.txt", "w")
        except:
            time.sleep(0.1)
            f = open("preview_condition.txt", "w")
            
            
        f.write("save")
        f.close()
        photo1 = ImageTk.PhotoImage(Image.open("Webp.net-resizeimage.png"))
        
    button.configure(image=photo1)


def change_pic2():

    global top2
    top2 = top2 + 1
    if top2 % 2 == 0:

        try:
            f = open("segmentation.txt", "w")
        except:
            time.sleep(0.1)
            f = open("segmentation.txt", "w")
        f.write("true")
        f.close()
        img3 = ImageTk.PhotoImage(Image.open("Untitled(8).png"))

        button2.grid(row=4, column=3)
        
    else:

        f = open("segmentation.txt", "w")
        f.write("false")
        f.close()
        img3 = ImageTk.PhotoImage(Image.open("Untitled(7).png"))
        
        button2.grid_forget()
    button3.configure(image=img3)
    button3.image = img3
    
button = Button(win, text="Click me!", command=lambda:change_pic())
img = PhotoImage(file="Webp.net-resizeimage.png") # make sure to add "/" not "\"
button.config(image=img)
myTip = Hovertip(button,'Be sure to turn off the preview after \npreviewing, for better performance!', hover_delay=50)
button.grid(row=0, column=3, sticky = W, padx = 100, pady = 100)

def openfile():
    g = tkinter.filedialog.askopenfilename(
    parent=win,
    title='Select a file...',
    filetypes=[("Images", "*.png *.jpg *.jpeg *.jp2 .webm")])

    backgroundimg = cv2.imread(g)
    cv2.imwrite("background.png", backgroundimg)

button2 = Button(win, text="Click me!", command=lambda:openfile())
img2 = PhotoImage(file="Untitled(6).png") # make sure to add "/" not "\"
button2.config(image=img2)
button2.grid(row=4, column=3)

button3 = Button(win, text="Click me!", command=lambda:change_pic2())
img3 = PhotoImage(file="Untitled(8).png") # make sure to add "/" not "\"
button3.config(image=img3)
button3.grid(row=4, column=0)


# Define function to show frame
def show_frames():

    

    if top % 2 == 0:

        imge = cv2.imread('jPLF6hO95Il9jSnB-croppedNsGME-jpg.jpg', 0)
        imge = cv2.cvtColor(imge, cv2.COLOR_BGR2RGB)

    else:

        try:
            imge = cv2.imread("preview.png")
            imge = cv2.cvtColor(imge, cv2.COLOR_BGR2RGB)
        except:
            try:
                time.sleep(0.1)
                imge = cv2.imread("preview.png")
                imge = cv2.cvtColor(imge, cv2.COLOR_BGR2RGB)
            except:
                try:
                    time.sleep(0.1)
                    imge = cv2.imread("preview.png")
                    imge = cv2.cvtColor(imge, cv2.COLOR_BGR2RGB)
                except:
                    time.sleep(0.1)
                    imge = cv2.imread("preview.png")
                    imge = cv2.cvtColor(imge, cv2.COLOR_BGR2RGB)
    
    imge = cv2.resize(imge, (700, 394))
    imge = cv2.cvtColor(imge, cv2.COLOR_BGR2RGB)
    
    imge = np.asarray(imge)
    img = Image.fromarray(imge)
    imgtk = ImageTk.PhotoImage(image = img)
    label.imgtk = imgtk
    label.configure(image=imgtk)

    label.after(5, show_frames)

    
show_frames()
win.mainloop()

os.system("taskkill /IM pyw.exe /F")
os.system("pkill -9 pyw")
os.system("pkill -9 python")

f = open("proc_run.txt", "w")
f.write("false")
