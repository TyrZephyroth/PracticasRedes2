import threading
import time
import glob
import os
import re
import json
from tkinter import *

directorioLibros="/home/itzco/Documents/Redes2/Practica1/librosCrudos/"
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
"""class MiHilo(threading.Thread):

    def __init__(self, threadID,name, file):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.file=file
        #self.counter = counter
    def run(self):
        print("Iniciando hilo " + self.name + "\t su ID es:", self.threadID)
        print("Este Hilo maneja el archivo:" + self.file)
        wordCount(palabrasAContar,self.file)
        #print ("Exiting " + self.name)"""

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
    #print(mydict)
    result[index]=mydict

#GUI
window = Tk()
window.geometry('720x1000')
window.title("Practica 1 Redes")
"""lbl = Label(window, text = "Libro")
lbl.pack()#lbl.grid(row=0)
topframe = Frame(window)
topframe.pack()
bottomframe = Frame(window)
bottomframe.pack(side=BOTTOM)"""
# Create new threads

txtCounter = len(glob.glob1(directorioLibros,"*.txt"))
print(txtCounter)
thread=[None]*txtCounter# Arreglo de Hilos
results=[None]*txtCounter#En este arreglo guardaremos los diccionarios de cada texto
"""txtLabels = [None]*txtCounter #Arreglo de labels para la GUI
resLabels = [None]*txtCounter #Arreglo de lables donde mostraremos los resultados de cada libro"""
txtFiles = []
scrollbar = Scrollbar(window)
scrollbar.pack(side=RIGHT, fill=Y) #scrollbar.grid(column=1,row=0, rowspan=94, sticky= N+S+E)
myListGUI = Listbox(window, yscrollcommand = scrollbar.set)
for file in glob.glob1(directorioLibros,"*.txt"):
    txtFiles.append(file)
for i in range (0,txtCounter):

    thread[i] = ThreadWithReturnValue(target=wordCount, args=(palabrasAContar, txtFiles[i], results, i ) )

    # Start new Threads
    thread[i].start()
    #thread[i].join()
for i in range (0,txtCounter):
    thread[i].join()
    myListGUI.insert(END,txtFiles[i])
    #txtLabels[i] = Label(window, text = txtFiles[i], justify=RIGHT)
    #txtLabels[i].pack()#txtLabels[i].grid(row=i+2, sticky=W)
    print("Texto: ",txtFiles[i],"palabras:")
    print (results[i])
    dictnAsString= json.dumps(results[i])
    myListGUI.insert(END,dictnAsString)
    #resLabels[i] = Label(window, text = dictnAsString, justify=RIGHT)
    #resLabels[i].pack()#resLabels[i].grid(row=i+1, sticky=W)
    print("\n")
print("El numero total de palabras es:",totaldePalabras )
print("El conteo global de palabras es:",globalCount )
for word in globalCount.keys():
    globalCount[word]=float(globalCount[word]/totaldePalabras)
print("La probabilidad es de:", globalCount)
myListGUI.insert(END,"El numero total de palabras es de:"+str(totaldePalabras))
dictnAsString= json.dumps(globalCount)
myListGUI.insert(END,"La probabilidad es de: "+dictnAsString)
myListGUI.pack(side = LEFT, fill = BOTH, expand=True)
scrollbar.config( command = myListGUI.yview)

#print("\n\n")
#print(results)
#print(results[0]['poesía'])

print ("Exiting Main Thread")

window.mainloop()
