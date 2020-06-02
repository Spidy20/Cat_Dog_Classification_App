from PIL import ImageTk
import PIL.Image
from tkinter import *
import tkinter as tk
from tkinter import filedialog
from skimage.io import imread
from skimage.transform import resize
import skimage,pickle

windo = Tk()
windo.configure(background='white')
windo.title("Animal Classification")
# width  = windo.winfo_screenwidth()
# height = windo.winfo_screenheight()
# windo.geometry(f'{width}x{height}')
windo.geometry('1120x820')
windo.iconbitmap('dog.ico')
windo.resizable(0,0)

#Size for displaying Image
w = 400;h = 280
size = (w, h)

def upload_im():
    try:
        global im,resized,cp,path,display,imageFrame,dn1
        imageFrame = tk.Frame(windo)
        imageFrame.place(x=535, y=160)
        path = filedialog.askopenfilename()
        im = PIL.Image.open(path)
        resized = im.resize(size, PIL.Image.ANTIALIAS)
        tkimage = ImageTk.PhotoImage(resized)
        display = tk.Label(imageFrame)
        display.imgtk = tkimage
        display.configure(image=tkimage)
        display.grid()
        dn1 = tk.Label(windo, text='Original\ud83d\ude80 Image ', width=20, height=1, fg="white", bg="firebrick1",
                       font=('times', 22, ' bold '))
        dn1.place(x=570, y=120)
        cp = tk.Button(windo, text='Predict\ud83d\ude80 Animal', bg="midnightblue", fg="white", width=20,
                       height=1, font=('times', 22, 'italic bold '),command = prediction,activebackground = 'yellow')
        cp.place(x=570, y=450)
    except Exception as e:
        print(e)
        noti = tk.Label(windo, text = 'Please upload an Image\ud83d\ude80 File', width=33, height=2, fg="white", bg="midnightblue",
                            font=('times', 23, ' bold '))
        noti.place(x=454, y=540)
        windo.after(5000, destroy_widget, noti)

def destroy_widget(widget):
    widget.destroy()

def prediction():
    windo.after(2000, destroy_widget, cp)
    def load_image(im_file):
        dimension = (104, 104)
        flat_data = []
        img = skimage.io.imread(im_file)
        img_resized = resize(img, dimension, anti_aliasing=True, mode='reflect')
        flat_data.append(img_resized.flatten())
        return flat_data
    img = load_image(path)
    try:
        with open('classifier.pkl', 'rb') as f:
            clf = pickle.load(f)
            pred = clf.predict(img)
            print(pred)
    except Exception as e:
        print(e)
        noti = tk.Label(windo, text = 'Model not Found', width=33, height=2, fg="white", bg="midnightblue",
                            font=('times', 23, ' bold '))
        noti.place(x=454, y=580)
        windo.after(5000, destroy_widget, noti)
    labels = ['Cat','Dog']
    s = [str(i) for i in pred]
    a = int("".join(s))
    lab = str("Predicted Animal is:  "+ labels[a])
    pred1 = tk.Label(windo, text=lab, width=33, height=2, fg="white",
                    bg="firebrick1",
                    font=('times', 23, ' bold '))
    pred1.place(x=454, y=540)
    windo.after(7000, destroy_widget, pred1)
    windo.after(7000, destroy_widget, display)
    windo.after(7000, destroy_widget, imageFrame)
    windo.after(7000, destroy_widget, dn1)

ri = PIL.Image.open('ml.png')
ri =ri.resize((321,263), PIL.Image.ANTIALIAS)
sad_img = ImageTk.PhotoImage(ri)
panel4 = Label(windo, image=sad_img,bg = 'white')
panel4.pack()
panel4.place(x=20, y=170)

up = tk.Button(windo,text = 'Upload\ud83d\ude80 Image',bg="spring green", fg="black", width=20,
                   height=1, font=('times', 22, 'italic bold '),command = upload_im, activebackground = 'yellow')
up.place(x=20, y=440)

pred = tk.Label(windo, text="Animal Classification", width=30, height=2, fg='black',bg="spring green",
                font=('times', 25, ' bold '))
pred.place(x=254, y=20)

windo.mainloop()