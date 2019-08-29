import threading
import time
import glob
import os
import re
import json
from tkinter import *
from tkinter import filedialog
from tkinter import *

directorioLibros="/home/zeph/Escritorio/practica 1/libros/"
palabrasAContar={"regalo":0 , "corazón":0, "delicioso":0, "perdón":0, "carta":0, "poesía":0}
globalCount={"regalo":0 , "corazón":0, "delicioso":0, "perdón":0, "carta":0, "poesía":0}
totaldePalabras=0

class ThreadWithReturnValue(threading.Thread):
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs={}, Verbose=None):
        threading.Thread.__init__(self, group, target, name, args, kwargs)
        self._return = None
    def run(self):
        #print(type(self._target))
        if self._target is not None:
            self._return = self._target(*self._args, **self._kwargs)
    def join(self, *args):
        threading.Thread.join(self, *args)
        return self._return

def wordCount(wordsToMatch, file, result, index):
    global totaldePalabras
    fileToRead=open(directorioLibros+file,"r",encoding="utf-8-sig")
    text=fileToRead.read().split()
    mydict=palabrasAContar.copy()
    for word in text:
        if word in mydict.keys():
            count=mydict[word]
            mydict[word]=count+1
            globalCount[word]+=1
            totaldePalabras=totaldePalabras+1
    result[index]=mydict

#GUI
window = Tk()
window.geometry('1000x600')
window.title("Practica 1 Redes")
# Create new threads

txtCounter = len(glob.glob1(directorioLibros,"*.txt"))
print(txtCounter)
thread=[None]*txtCounter# Arreglo de Hilos
results=[None]*txtCounter#En este arreglo guardaremos los diccionarios de cada texto
txtFiles = []
scrollbar = Scrollbar(window)
scrollbar.pack(side=RIGHT, fill=Y) #scrollbar.grid(column=1,row=0, rowspan=94, sticky= N+S+E)
myListGUI = Listbox(window, yscrollcommand = scrollbar.set)

def analizartodos():
    for file in glob.glob1(directorioLibros,"*.txt"):
        txtFiles.append(file)
    for i in range (0,txtCounter):
        thread[i] = ThreadWithReturnValue(target=wordCount, args=(palabrasAContar, txtFiles[i], results, i ) )
        # Start new Threads
        thread[i].start()
    
    for i in range (0,txtCounter):
        thread[i].join()
        myListGUI.insert(END,txtFiles[i])
        dictnAsString= json.dumps(results[i])
        myListGUI.insert(END,dictnAsString)
    
        myListGUI.insert(END, "Las palabras del libro son : " + str(totaldePalabras))
    
    for word in globalCount.keys():
        globalCount[word]=float(globalCount[word]/totaldePalabras)

    
    myListGUI.insert(END,"El numero total de palabras es de:"+str(totaldePalabras))
    myListGUI.insert(END,"EL porcentaje global es: " +str(globalCount) )
    dictnAsString= json.dumps(globalCount)
    return 0



def analizar1():

    myListGUI.filename =  filedialog.askopenfilename(initialdir = "/home/zeph/Escritorio/practica 1/libros/",title = "Select file",filetypes = (("txt files","*.txt"),("all files","*.*")))
    myListGUI.insert(END,myListGUI.filename)

    cadenaPalabras2 = open(myListGUI.filename , "r+")
    Buscar = 'regalo corazón delisioso perdon carta poesia'

    cadenaPalabras= cadenaPalabras2.read()
    #print(cadenaPalabras)

    listaPalabras = Buscar.split()

    frecuenciaPalab = []
    for w in listaPalabras:
        frecuenciaPalab.append(cadenaPalabras.count(w))

    myListGUI.insert(END, str(listaPalabras))
    myListGUI.insert(END, str(frecuenciaPalab))

    return 0



hilo1 = threading.Thread(target=analizar1)
hilo1.start()

myListGUI.pack(side = LEFT, fill = BOTH, expand=True)
scrollbar.config( command = myListGUI.yview)



b1 = Button (myListGUI, text = "Analizar todos", width = 15, height = 2, command = analizartodos)
b1.place (x = 50, y = 50)

b1 = Button (myListGUI, text = "Analizar 1 libro", width = 15, height = 2, command = analizar1 ) 
b1.place (x = 50, y = 100)



print ("Exiting Main Thread")

window.mainloop()
