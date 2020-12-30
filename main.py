import face_recognition
import cv2
import pickle
import os
import numpy as np

import tkinter as tk
from tkinter import messagebox
from pathlib import Path

class Yuz_Giris:

    def __init__(kisi):

        try:
            with open(r'C:\Users\barry\PycharmProjects\face_rec\labels.pickle', 'rb') as kisi.f:
                kisi.og_labels = pickle.load(kisi.f)
            print(kisi.og_labels)

        except FileNotFoundError:

            print("Hata, Pickle dosyası yok")


        kisi.current_id = 0

        kisi.labels_ids = {}

        kisi.BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        kisi.image_dir = os.path.join(kisi.BASE_DIR, 'Fotoğraflar')
        for kisi.root, kisi.dirs, kisi.files in os.walk(kisi.image_dir):

            for kisi.file in kisi.files:

                if kisi.file.endswith('png') or kisi.file.endswith('jpg'):

                    kisi.path = os.path.join(kisi.root, kisi.file)
                    kisi.label = os.path.basename(os.path.dirname(kisi.path)).replace(' ', '-').lower()
                    if not kisi.label in kisi.labels_ids:

                        kisi.labels_ids[kisi.label] = kisi.current_id
                        kisi.current_id += 1
                        kisi.id = kisi.labels_ids[kisi.label]

        print(kisi.labels_ids)
        kisi.og_labels = 0
        if kisi.labels_ids != kisi.og_labels:

            with open('labels.pickle', 'wb') as kisi.file:
                pickle.dump(kisi.labels_ids, kisi.file)

            kisi.known_faces = []
            for kisi.i in kisi.labels_ids:

                foto_NO = len([filename for filename in os.listdir('Fotoğraflar/' + kisi.i)
                                if os.path.isfile(os.path.join('Fotoğraflar/' + kisi.i, filename))])
                print(foto_NO)
                for imgNo in range(1, (foto_NO + 1)):
                    kisi.directory = os.path.join(kisi.image_dir, kisi.i, str(imgNo) + '.png')
                    kisi.img = face_recognition.load_image_file(kisi.directory)
                    kisi.img_encoding = face_recognition.face_encodings(kisi.img)[0]
                    kisi.known_faces.append([kisi.i, kisi.img_encoding])
            print(kisi.known_faces)
            #Kontroller için çıktı alıyorum
            print("Foto No su: " + str(len(kisi.known_faces)))
            with open('KnownFace.pickle', 'wb') as kisi.known_faces_file:
                pickle.dump(kisi.known_faces, kisi.known_faces_file)
        else:
            with open(r'CC:\Users\barry\PycharmProjects\face_rec\KnownFace.pickle', 'rb') as kisi.faces_file:
                kisi.known_faces = pickle.load(kisi.faces_file)
            print(kisi.known_faces)


    def ID(kisi):

        kisi.cap = cv2.VideoCapture(0)

        kisi.running = True
        kisi.face_names = []
        while kisi.running == True:

            kisi.ret, kisi.frame = kisi.cap.read()

            kisi.small_frame = cv2.resize(kisi.frame, (0, 0), fx=0.5, fy=0.5)

            kisi.rgb_small_frame = kisi.small_frame[:, :, ::-1]
            if kisi.running:

                kisi.face_locations = face_recognition.face_locations(kisi.frame)

                kisi.face_encodings = face_recognition.face_encodings(kisi.frame, kisi.face_locations)

                kisi.face_names = []

                for kisi.face_encoding in kisi.face_encodings:

                    for kisi.face in kisi.known_faces:

                        kisi.matches = face_recognition.compare_faces([kisi.face[1]], kisi.face_encoding)
                        print(kisi.matches)
                        kisi.name = 'Unknown'

                        kisi.face_distances = face_recognition.face_distance([kisi.face[1]], kisi.face_encoding)

                        kisi.best_match = np.argmin(kisi.face_distances)
                        print(kisi.best_match)
                        print('En iyi eşleşme', kisi.matches[kisi.best_match])
                        if kisi.matches[kisi.best_match] == True:
                            kisi.running = False
                            kisi.face_names.append(kisi.face[0])
                            break
                        next
            print("En iyi eşleşme" + str(kisi.face_names))
            kisi.cap.release()
            cv2.destroyAllWindows()
            break
        return kisi.face_names




def Kayit():
    a=isim.get()
    b=surname.get()
    c=tc.get()
    name.set=(a+"-"+b+"-"+c)
    if not os.path.exists("Fotoğraflar"):
        os.makedirs("Fotoğraflar")

    Path("Fotoğraflar/" + name.get()).mkdir(parents=True, exist_ok=True)

    numberOfFile = len([filename for filename in os.listdir('Fotoğraflar/' + name.get())
                        if os.path.isfile(os.path.join('Fotoğraflar/' + name.get(), filename))])

    numberOfFile += 1

    cam = cv2.VideoCapture(0)

    cv2.namedWindow("test")

    while True:
        ret, frame = cam.read()
        cv2.imshow("test", frame)
        if not ret:
            break
        k = cv2.waitKey(1)

        if k % 256 == 27:

            print("Escape hit, closing...")
            cam.release()
            cv2.destroyAllWindows()
            break
        elif k % 256 == 32:

            img_name = str(numberOfFile) + ".png"
            cv2.imwrite(img_name, frame)
            print("{} written!".format(img_name))
            os.replace(str(numberOfFile) + ".png", "Fotoğraflar/" + name.get().lower() + "/" + str(numberOfFile) + ".png")
            cam.release()
            cv2.destroyAllWindows()
            break
    raiseFrame(loginFrame)



def Giris():
   dfu = Yuz_Giris()

   kamera=cv2.VideoCapture(0)
   while True:
       tf,goruntu=kamera.read()
       cv2.imshow('Görüntü',goruntu)
       if cv2.waitKey(1)==ord('a'):
            break
   kamera.release()
   cv2.destroyAllWindows()
   user = dfu.ID()
   if user == []:
        messagebox.showerror("Alert", "Face Not Recognised")
        return
   a=str(user[0]+"\n"+user[1]+"\n"+user[2])
   print(a)
   loggedInUser.set(a)
   raiseFrame(userMenuFrame)


# Tkinter
root = tk.Tk()
root.geometry("580x275+400+200")
root.title("Yüz Giris Uygulaması")
# Ekranlar
loginFrame = tk.Frame(root)
regFrame = tk.Frame(root)
userMenuFrame = tk.Frame(root)


frameList = [loginFrame, regFrame, userMenuFrame]

for frame in frameList:
    frame.grid(row=1, column=1, sticky='news')
    frame.configure(bg='#031e3b')


def raiseFrame(frame):
    frame.tkraise()


def regFrameRaiseFrame():
    raiseFrame(regFrame)


def logFrameRaiseFrame():
    raiseFrame(loginFrame)


back=tk.PhotoImage(file="back.png.png")
giris=tk.PhotoImage(file="login.png.png")
login=tk.PhotoImage(file="logout.png.png")
yuz=tk.PhotoImage(file="facial-recognition.png.png")
kayit1=tk.PhotoImage(file="register.png")
tik=tk.PhotoImage(file="tick.png.png")



isim=tk.StringVar()
surname=tk.StringVar()
tc=tk. StringVar()
name=tk. StringVar()
#giriş yapan kullanıcıların adını depolamak için

loggedInUser = tk. StringVar()
my_font = Font (family="Times New Roman",weight="bold", slant="italic")

tk.Label (loginFrame, bg="#031e3b").place (x=0, y=0)
tk.Label (loginFrame, image=yuz, bg="#031e3b", font= ("Courier", 60).place (x=210 ,y=0)
xxx=tk.Button(loginFrame, font=("Arial",30), bd=0,image=giris ,command=Giris, bg="#031e3b")
xxx.place (x=400, y=150)

regButton =tk.Button(loginFrame, image=login, command=regFrameRaiseFrame, bd=0 font=("Arial", 30), highlightthickness = 0, bg="#031e3b")
tk.Button (loginFrame, image=login, command=regFrameRaiseFrame, bd=0 font=("Arial", 30), highlightthickness = 0, bg="#031e3b")
regButton.place (x=50, y=150)

tk.Label(regFrame, text="Kayit", image=kayit1, font= (my_font, 60), fg="#09e5ff", bg="#031e3b",bd=0).grid (row=1, column=1, columnspan=5)
tk.Label(regFrame, text="Ad: ", font= (my_font, 30), fg="#09e5ff", bg="#031e3b", bd=0).grid(row=2, column=1)
tk.Label (regFrame text="Soyad: ", font= ("Arial"30), fg="#09e5ff", bg="#031e3b", bd=0).grid (row=3, column=1)
tk.Label (regFrame text="Tc: ", font= (my_font, 30), fg="#09e5ff" bg="#031e3b", bd=0).grid(row=4, column=1)

nameEntry=tk.Entry(regFrame, textvariable=isim, font=(my_font ,30)bg="#031e3b").grid(row=2,column=2)
surnameEntry=tk.Entry(regFrame,textvariable=surname, font=(my_font,30),bg="#031e3b").grid(row=3, column=2)
tcEntry=tk.Entry(regFrame,textvariable=tc, font=(my_font,30),bg="#031e3b").grid(row=4, column=2)
registerButton = tk.Button(regFrame, text="Kayit", command=Kayit,image=tik, bg="#031e3b", bd=0 font=("Arial", 30))
registerButton.grid(row=5, column=2)

tk.Label(userMenuFrame, text="Hoşgeldiniz, ", font=("Courier", 30), fg="#09e5ff", bg="031e3b",bd=0).place(x=150,y=0)
tk.Label(userMenuFrame, text="AD", font=("Courier", 30), bg="031e3b", fg="#09e5ff",bd=0).place(x=100,y=60)
tk.Label(userMenuFrame, text="SOYAD", font=("Courier", 30), bg="031e3b", fg="#09e5ff",bd=0).place(x=20,y=60)
tk.Label(userMenuFrame, text="TC", font=("Courier", 30), bg="031e3b", fg="#09e5ff",bd=0).place(x=20,y=100)
tk.Label(userMenuFrame, textvariable=loggedInUser, font=("Courier", 30), bg="031e3b", fg="#09e5ff",bd=0).place(x=20,y=140)
tk.Button(userMenuFrame, image=back, font=("Arial", 30), command=logFrameRaiseFrame).grid(row=2, column=1)


dfu = Yuz_Giris()
raiseFrame(loginFrame)
root.mainloop()