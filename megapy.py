import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib import style
from matplotlib import pyplot as plt

from urllib.request import urlopen
from bs4 import BeautifulSoup

import tkinter as tk
from tkinter import ttk
from tkinter import *

from PIL import Image,ImageTk

import re
import os.path
import requests
import zipfile

import threading
from queue import Queue
import time
from itertools import takewhile,repeat


import numpy as np


## http://www1.caixa.gov.br/loterias/_arquivos/loterias/D_mgsasc.zip Mega
## http://www1.caixa.gov.br/loterias/_arquivos/loterias/D_lotfac.zip lotoFacil

##http://www.estatisticasdamegasena.com.br/site/?p=est_home&lot=meg&sub=est&est=1
##http://www.mega-sena.org/como-ganhar-e-como-jogar
##http://www1.caixa.gov.br/app/loterias/mega-sena.html

#V-K-T-M= B

##V = quantidade de números que será utilizada no fechamento, ou seja, quantas dezenas estarão presentes na aposta
##K = quantas dezenas que serão marcados em cada bilhete
##T= é o prêmio mínimo (Quadra, Quina ou Sena) que você deseja garantir
##M = é a condição necessária para garantir que parâmetro T seja cumprido
##B = quantidade de bilhetes necessários para que este fechamento funcione

##20Numeros Quentes* os que mais saem nos ultimos 20 jogos
##10Numeros frios* os que menos saem nos ultimos 10 jogos
##numeros repetidos nos X jogos

##Probabilidades
##Cn,p =       n!
##            p!(n - p)!

##Numero de digitos por aposta
##Por exemplo, o palpite: 1 11 21 35 45 51
##Ele tem: 1 + 2 + 2 + 2 + 2 + 2 = 11 dígitos

##Agora o palpite: 2 4 9 34 39 59
##Esse palpite possui: 1 + 1 + 1 + 2 + 2 + 2 = 9 dígitos.

##175: 1 10 13 20 42 50
##A soma dos dígitos dessa resultado da Mega-Sena é 19.




def HotNumbers():
    print("20 Numeros Quentes* os que mais saem nos ultimos 20 jogos")

def ColdNumbers():
    print("20 Numeros Frios* os que mais saem nos ultimos 20 jogos")

def NumerosRepeat():
    print ("Numeros repetidos nos X jogos")

def SomaDigitos():
    print ("Soma dos digitos")

LARGE_FONT= ("Agency FB", 14)
DEFAULT_FONT= ("Agency FB", 12)
SMALL_FONT= ("Agency FB", 10)
TIME=20000
style.use("ggplot")

f = plt.figure()
a = f.add_subplot(111)


def popupmsg(tit,msg):
    popup = tk.Tk()
    popup.wm_title(tit)
    label = ttk.Label(popup, text=msg, font=DEFAULT_FONT)
    label.pack(side="top", fill="both", pady=10, expand=True)
    B1 = ttk.Button(popup, text="Ok", command = popup.destroy)
    B1.pack()
    popup.mainloop()


def DownloadFile(url):
    local_filename = url.split('/')[-1]
    r = requests.get(url)
    with open(local_filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)
    return

def makeData():

    url = 'http://www1.caixa.gov.br/loterias/_arquivos/loterias/D_mgsasc.zip'
    DownloadFile(url)

    with zipfile.ZipFile('D_mgsasc.zip') as zf:
        zf.extractall()

    bsObj = BeautifulSoup(open("d_megasc.htm",'rb'),"html.parser")


    data = bsObj.findAll('td')
    dados = []
    for value in data:
        dados.append(value.text)

    del data

    srtDados = str(dados)
    datas = re.findall("[0-9][0-9]/[0-9][0-9]/[0-9][0-9][0-9][0-9]",srtDados)
    datesindex = []
    dateslen = len(datas)

    for j in range(0,dateslen):
        datesindex.append(dados.index(datas[j]))
    sorteios = []
    for x in datesindex:
        sorteios.append(dados[x:x+7])

    try:
        with open('lock.lock', 'r') as lock:
           lockvalue = lock.readline()
        lastLine = int(lockvalue)
        print("Arquivo Lock encontrado \nContinuando a execução da ultima linha executada!")
        print (lastLine)
##        popupmsg("Alerta","Arquivo Lock encontrado \nContinuando a execução da ultima linha executada!\n\n lastLine")

    except:
        print ("Criando arquivo Lock")
        with open("lock.lock", "w")as lock:
            lock.write("0")
        lastLine = 0
    finally:
        print ("...Obtendo Dados... ")

    eof=len(sorteios)
    if (lastLine+1 != eof):
        for value in range(lastLine,eof):
            with open("lock.lock", "w")as lock:
                    lock.write(str(value))

            with open("foo.txt", "a+")as sort:
                z=value+1
                sort.write("Nº sorteio: %s \n" % z)
                sort.write("Date: %s \n" % sorteios[value][0])
                for number in range(1,7):
                    sort.write( str(sorteios[value][number])+ "\n")

        with open("score.txt", "a+")as score:
            for number in range(1,7):
                score.write( str(sorteios[value][number])+ "\n")

##        with open("score.txt", "r")as score:
##            word = score.readlines()

        prefix = ["01","02","03","04","05","06","07","08","09",10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60]

##        with open("data.txt", "w")as score:
##            score.write("0")

        lista=[]
        for value in range(0,eof):
            for number in range(1,7):
                lista.append(sorteios[value][number])


    with open("graphData.txt","a+")as gData:
        for x in prefix:
            k=str(x)
            records= "{0},{1}".format(x,lista.count(k))
            gData.write(records)
            gData.write("\n")

#        print ("Arquivo de jogos salvo com sucesso")
        
        #print(lista[0]+lista[1]+lista[2]+lista[3]+lista[5])

def animate(i):
    pullData = open("graphData.txt","r").read()
    dataList = pullData.split('\n')
    xList = []
    yList = []
    for eachLine in dataList:
        if len(eachLine) > 1:
            x, y = eachLine.split(',')
            xList.append(int(x))
            yList.append(int(y))

    a.clear()
    plt.title('Nº Sorteados')
    plt.ylabel('Nº Vezes sorteados')
    plt.xlabel('Numeros')
    plt.subplots_adjust(left=0.07, bottom=0.10, right=0.95, top=0.95, wspace=0.2, hspace=0.2)
    ax = plt.subplot()
    start, end = ax.get_xlim()
    starty, endy = ax.get_ylim()
#    ax.xaxis.set_ticks(np.arange(start, end, 1))
    ax.xaxis.set_ticks(np.arange(1, 61, 1))
    ax.yaxis.set_ticks(np.arange(min(yList)-3, max(yList)+3, 2))
    ax.set_ylim(top=max(yList)+2,bottom=min(yList)-2)
    bars = plt.bar(xList, yList)
    plt.axhline(y= 90*2, color='b', linestyle='-')
    plt.setp(bars, color='r',edgecolor='k',linewidth=1)



class MegaPy(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.wm_title(self, "Mega client")


        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)


        menubar = tk.Menu(container)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Input File", command = lambda: popupmsg("Danger","Not supported just yet!"))
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=quit)
        menubar.add_cascade(label="File", menu=filemenu)

        Data = tk.Menu(menubar, tearoff=0)
        Data.add_command(label="Make Data Graph", command = makeData)
        menubar.add_cascade(label="Data", menu=Data)


        Help = tk.Menu(menubar, tearoff=0)
        Help.add_command(label="About", command = About)
        menubar.add_cascade(label="Help", menu=Help)

        tk.Tk.config(self, menu=menubar)


        self.frames = {}

        for F in (StartPage, Mega_chart):

            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)
        #tk.TK.iconbitmap(self,default="*.ico")

    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)

        tk.Label(self, text="Start Page", font=LARGE_FONT).place(relx=0.45,rely=0.05)

        tk.Label(self, text="01 02 03 04 05 06 07 08 09 10", font=LARGE_FONT).place(relx=0.45,rely=0.10)
        tk.Label(self, text="11 12 13 14 15 16 17 18 19 20", font=LARGE_FONT).place(relx=0.45,rely=0.15)
        tk.Label(self, text="21 22 23 24 25 26 27 28 29 30", font=LARGE_FONT).place(relx=0.45,rely=0.20)
#        tk.Label(self, text="", font=LARGE_FONT).place(relx=0.5 ,rely=0.2)
        tk.Label(self, text="31 32 33 34 35 36 37 38 49 40", font=LARGE_FONT).place(relx=0.45,rely=0.25)
        tk.Label(self, text="41 42 43 44 45 46 47 48 49 50", font=LARGE_FONT).place(relx=0.45,rely=0.30)
        tk.Label(self, text="51 52 53 54 55 56 57 58 59 60", font=LARGE_FONT).place(relx=0.45,rely=0.35)

        ttk.Button(self, text="Graph Page",command=lambda: controller.show_frame(Mega_chart)).place(relx=0.5,rely=0.9)
        ttk.Button(self, text="EXIT",command=quit).place(relx=0.9,rely=0.9)



class Mega_chart(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Graph Page!", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        button1 = ttk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))
        button1.pack()

        canvas = FigureCanvasTkAgg(f, self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        toolbar = NavigationToolbar2Tk(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)


def About():
    About = tk.Toplevel()
    About.wm_title("About")
    ttk.Label(About, text="About Loteria Tkinter Client", font=LARGE_FONT).grid(row=0,rowspan=3,column=0,columnspan=4,pady=10)

    logo = PhotoImage(file="ico/mega.gif")
    logo2 = PhotoImage(file="ico/lotofacil.gif")
    ttk.Label(About, image=logo).grid(row=4,column=0)
    ttk.Label(About, image=logo2).grid(row=5,column=0)

    explanation = "At present, only GIF and PPM/PGM formats are supported, but an interface exists to allow additional image file formats to be added easily."

    ttk.Label(About, justify=LEFT, text=explanation, font=DEFAULT_FONT).grid(row=5,column=2)
    
    ttk.Button(About, text="0x0", command = About.destroy).place(relx = 0.0, rely = 0.0)
    ttk.Button(About, text="0x5", command = About.destroy).place(relx = 0.5, rely = 0.5)
    #ttk.Button(About, text="Ok", command = About.destroy).grid(row=6,column=2)

    About.mainloop()



app = MegaPy()
app.geometry("1280x768+150+150")
try:
    ani = animation.FuncAnimation(f, animate, interval=TIME)
except:
    with open("graphData.txt","w")as gdata:
        gdata.write("")
app.mainloop()

#rm *.zip *.htm *.gif
