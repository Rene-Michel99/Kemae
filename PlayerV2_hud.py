# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Music_hud.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

import os
from mutagen.mp3 import MP3
import threading
import time
import mutagen
import stagger
from random import randint
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox,QCompleter
import keyboard
from tkinter import *
import warnings
warnings.filterwarnings("ignore")

class Musica():
    def __init__(self,album,nome,artist,picture,path,length):
        if type(album)==list:
            self.album=''.join(album)
        else:
            self.album=album
        if type(nome)==list:
            self.nome=''.join(nome)
        else:
            self.nome=nome
        if type(artist)==list:
            self.artist=''.join(artist)
        else:
            self.artist=artist
        self.picture=picture
        self.path=path
        self.length=length

def try_get_tag(tag,info):
    try:
        return info[tag]
    except:
        return ''

def tira_coisa(string):
    if string.find('[Audio]')!=-1:
        string=string.replace('[Audio]','')
    if string.find('(Lyrics)')!=-1:
        string=string.replace('(Lyrics)','')
    if string.find('[Hd]')!=-1:
        string=string.replace('[Hd]','')
    if string.find('(Lyric Video)')!=-1:
        string=string.replace('(Lyric Video)','')
    if string.find('(Official Audio)')!=-1:
        string=string.replace('(Official Audio)','')
    if string.find('(Official Video)')!=-1:
        string=string.replace('(Official Video)','')
    if string.find('(Lyrics Video)')!=-1:
        string=string.replace('(Lyrics Video)','')
    return string

def transform(nome):
    nome=tira_coisa(nome)
    if nome.find('-')!=-1:
        mid=nome.find('-')
        nome=nome.title()
        log=nome.find('.Mp3')
        music=nome[mid+1:log]
        artist=nome[:mid]
        if music[0]==' ':
            music=music[1:]
        elif music[0]==' ' and musica[1]==' ':
            music=music[2:]
        return music,artist
    else:
        return nome.replace('.mp3',''),''

def remove_from_begin(st):
    new_string=''
    for i in range(len(st)):
        if st[i]=='.' or st[i]=="'" or st[i]==' ':
            continue
        return st[i:]

def adequa(string):
    string=tira_coisa(string)
    music,artist=transform(string)
    if music[0]==' ' or music[0]=="'" or music[0]=='.':
        music=remove_from_begin(music)
    return music,artist

def get_tag(tag,info):
    x=try_get_tag(tag,info)
    return x

def create_img(data,path):
    from PIL import Image
    import io

    im=io.BytesIO(data)
    imageFile=Image.open(im)
    if str(imageFile).find('Jpeg')!=-1:
        imageFile='.jpeg'
    elif str(imageFile).find('Png')!=-1:
        imageFile='.png'
    arq=open(path+imageFile,'wb')
    arq.write(data)
    arq.close()
    return path+imageFile

def get_length(path):
    suiz=path
    st=MP3(suiz)
    absol=divmod(st.info.length,60)
    duration=absol[0]+(absol[1]/100)
    duration*=60
    return duration

def get_with_stagger(path,item):
    info=stagger.read_tag(path+item)
    album=info.album
    title=info.title
    artist=info.artist
    picture=info[stagger.id3.APIC][0].data
    if title=='':
        title,artist=adequa(item)
    if type(picture)==bytes:
        picture=create_img(picture,path+title)
    length=get_length(path+item)
    if title[0]==' ' or title[0]=="'" or title[0]=='.':
        title=remove_from_begin(title)
    music=Musica(album,title,artist,picture,path+item,length)
    return music

def get_with_mutagen(path,item):
    info=mutagen.mp3.EasyMP3(path+item).tags
    
    album=get_tag('album',info)
    title=get_tag('title',info)
    artist=get_tag('artist',info)
    picture='music-note.png'
    if title=='':
        title,artist=adequa(item)
    length=get_length(path+item)
    if title[0]==' ' or title[0]=="'" or title[0]=='.':
        title=remove_from_begin(title)
    music=Musica(album,title,artist,picture,path+item,length)
    return music

def define_data(path,item):
    try:
        return get_with_stagger(path,item)
    except:
        return get_with_mutagen(path,item)

def get_user_path():
    path=os.getcwd()
    path=path.replace('\\','/')
    path=path.replace('C:','')
    end=path[7:]
    end=end[:end.find('/')]
    return '/Users/'+end+'/Music/'
    

def define_musics():
    path=get_user_path()
    lista=os.listdir(path)

    musicas=[]

    for item in lista:
        if item.find('.mp3')!=-1:
            musicas.append(define_data(path,item))
    return musicas

def split(input_list):
    input_list_len = len(input_list)
    midpoint = input_list_len // 2
    return input_list[:midpoint], input_list[midpoint:]

def merge_sorted_lists(list_left, list_right):
    if len(list_left) == 0:
        return list_right
    elif len(list_right) == 0:
        return list_left
    index_left = index_right = 0
    list_merged = []  
    list_len_target = len(list_left) + len(list_right)
    while len(list_merged) < list_len_target:
        if list_left[index_left].nome <= list_right[index_right].nome:
            list_merged.append(list_left[index_left])
            index_left += 1
        else:
            list_merged.append(list_right[index_right])
            index_right += 1
        if index_right == len(list_right):
            list_merged += list_left[index_left:]
            break
        elif index_left == len(list_left):
            list_merged += list_right[index_right:]
            break
    return list_merged

def merge_sort(input_list):
    if len(input_list) <= 1:
        return input_list
    else:
        left, right = split(input_list)
        return merge_sorted_lists(merge_sort(left), merge_sort(right))
            

from pygame import mixer
class Mixer:
    mixer.init()
    def __init__(self):
        self.pause=False

    def handle_event(self,music=''):
        if music=='':
            if not self.pause:
                self.pause=True
                mixer.music.pause()
            else:
                self.pause=False
                mixer.music.unpause()
        else:
            mixer.music.load(music)
            mixer.music.play()

    def get_volume(self):
        return mixer.music.get_volume()

    def set_volume(self,volume):
        mixer.music.set_volume(volume)

    def is_busy(self):
        if mixer.get_busy():
            return True
        else:
            return False
        
class Button:
    def __init__(self,num,lista,objeto,texto):
        self.num=num
        self.lista=lista
        self.bt=QtWidgets.QPushButton(objeto)
        self.bt.setText(texto)
        self.bt.clicked.connect(self.handleInput)

    def handleInput(self):
        self.lista.append(self.num)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 632)
        MainWindow.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setStyleSheet("background-color: rgb(25, 25, 25);")
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setContentsMargins(0, 0, -1, 0)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName("gridLayout")
        self.scrollArea = QtWidgets.QScrollArea(self.centralwidget)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents_2 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_2.setGeometry(QtCore.QRect(0, 0, 645, 408))
        self.scrollAreaWidgetContents_2.setObjectName("scrollAreaWidgetContents_2")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents_2)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout_3.addLayout(self.verticalLayout_2)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents_2)
        self.gridLayout.addWidget(self.scrollArea, 1, 2, 1, 1)
        self.line_7 = QtWidgets.QFrame(self.centralwidget)
        self.line_7.setStyleSheet("background-color: rgb(26, 26, 26);")
        self.line_7.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_7.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_7.setObjectName("line_7")
        self.gridLayout.addWidget(self.line_7, 3, 1, 1, 1)
        self.search = QtWidgets.QLineEdit(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.search.setFont(font)
        self.search.setStyleSheet("color: rgb(255, 255, 255);")
        self.search.setInputMask("")
        self.search.setText("")
        self.search.setEchoMode(QtWidgets.QLineEdit.Normal)
        self.search.setClearButtonEnabled(True)
        self.search.setObjectName("search")
        self.gridLayout.addWidget(self.search, 0, 2, 1, 1)
        self.gridLayout_7 = QtWidgets.QGridLayout()
        self.gridLayout_7.setSpacing(6)
        self.gridLayout_7.setObjectName("gridLayout_7")
        self.line_5 = QtWidgets.QFrame(self.centralwidget)
        self.line_5.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_5.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_5.setObjectName("line_5")
        self.gridLayout_7.addWidget(self.line_5, 4, 4, 1, 1)
        self.max_time = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.max_time.setFont(font)
        self.max_time.setStyleSheet("color: rgb(255, 255, 255);")
        self.max_time.setObjectName("max_time")
        self.gridLayout_7.addWidget(self.max_time, 5, 4, 1, 1)
        self.music_info = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.music_info.setFont(font)
        self.music_info.setStyleSheet("color: rgb(255, 255, 255);")
        self.music_info.setObjectName("music_info")
        self.gridLayout_7.addWidget(self.music_info, 2, 0, 2, 1)
        self.proxima = QtWidgets.QPushButton(self.centralwidget)
        self.proxima.setStyleSheet("")
        self.proxima.setObjectName("proxima")
        self.gridLayout_7.addWidget(self.proxima, 2, 4, 2, 1)
        self.pausar = QtWidgets.QPushButton(self.centralwidget)
        self.pausar.setStyleSheet("")
        self.pausar.setObjectName("pausar")
        self.gridLayout_7.addWidget(self.pausar, 2, 3, 2, 1)
        self.line_2 = QtWidgets.QFrame(self.centralwidget)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.gridLayout_7.addWidget(self.line_2, 4, 0, 1, 1)
        self.anterior = QtWidgets.QPushButton(self.centralwidget)
        self.anterior.setStyleSheet("")
        self.anterior.setObjectName("anterior")
        self.gridLayout_7.addWidget(self.anterior, 2, 2, 2, 1)
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.gridLayout_7.addWidget(self.line, 4, 1, 1, 1)
        self.line_3 = QtWidgets.QFrame(self.centralwidget)
        self.line_3.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.gridLayout_7.addWidget(self.line_3, 4, 2, 1, 1)
        self.line_4 = QtWidgets.QFrame(self.centralwidget)
        self.line_4.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_4.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_4.setObjectName("line_4")
        self.gridLayout_7.addWidget(self.line_4, 4, 3, 1, 1)
        self.order = QtWidgets.QPushButton(self.centralwidget)
        self.order.setText("")
        self.order.setObjectName("order")
        self.gridLayout_7.addWidget(self.order, 2, 1, 2, 1)
        self.time_music = QtWidgets.QSlider(self.centralwidget)
        self.time_music.setEnabled(False)
        self.time_music.setTracking(True)
        self.time_music.setOrientation(QtCore.Qt.Horizontal)
        self.time_music.setObjectName("time_music")
        self.gridLayout_7.addWidget(self.time_music, 5, 2, 1, 2)
        self.time_now = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.time_now.setFont(font)
        self.time_now.setStyleSheet("color: rgb(255, 255, 255);")
        self.time_now.setObjectName("time_now")
        self.gridLayout_7.addWidget(self.time_now, 5, 1, 1, 1)
        self.gridLayout_7.setColumnStretch(0, 2)
        self.gridLayout_7.setColumnStretch(2, 1)
        self.gridLayout_7.setColumnStretch(3, 1)
        self.gridLayout_7.setColumnStretch(4, 1)
        self.gridLayout.addLayout(self.gridLayout_7, 3, 2, 1, 1)
        self.gridLayout_8 = QtWidgets.QGridLayout()
        self.gridLayout_8.setObjectName("gridLayout_8")
        self.label = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.setStyleSheet("color: rgb(255, 255, 255);")
        self.label.setObjectName("label")
        self.gridLayout_8.addWidget(self.label, 0, 0, 1, 1)
        self.gridLayout.addLayout(self.gridLayout_8, 0, 0, 1, 1)
        self.line_8 = QtWidgets.QFrame(self.centralwidget)
        self.line_8.setStyleSheet("background-color: rgb(26, 26, 26);")
        self.line_8.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_8.setLineWidth(1)
        self.line_8.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_8.setObjectName("line_8")
        self.gridLayout.addWidget(self.line_8, 1, 1, 1, 1)
        self.line_9 = QtWidgets.QFrame(self.centralwidget)
        self.line_9.setStyleSheet("background-color: rgb(26, 26, 26);")
        self.line_9.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_9.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_9.setObjectName("line_9")
        self.gridLayout.addWidget(self.line_9, 0, 1, 1, 1)
        self.line_10 = QtWidgets.QFrame(self.centralwidget)
        self.line_10.setStyleSheet("background-color: rgb(26, 26, 26);")
        self.line_10.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_10.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_10.setObjectName("line_10")
        self.gridLayout.addWidget(self.line_10, 2, 0, 1, 1)
        self.verticalLayout_6 = QtWidgets.QVBoxLayout()
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.scroll_playlists = QtWidgets.QScrollArea(self.centralwidget)
        self.scroll_playlists.setWidgetResizable(True)
        self.scroll_playlists.setObjectName("scroll_playlists")
        self.scrollAreaWidgetContents_3 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_3.setGeometry(QtCore.QRect(0, 0, 126, 300))
        self.scrollAreaWidgetContents_3.setObjectName("scrollAreaWidgetContents_3")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents_3)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.create_plt = QtWidgets.QPushButton(self.scrollAreaWidgetContents_3)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.create_plt.setFont(font)
        self.create_plt.setStyleSheet("color: rgb(255, 255, 255);")
        self.create_plt.setObjectName("create_plt")
        self.verticalLayout_5.addWidget(self.create_plt)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.verticalLayout_5.addLayout(self.verticalLayout_4)
        self.scroll_playlists.setWidget(self.scrollAreaWidgetContents_3)
        self.verticalLayout_6.addWidget(self.scroll_playlists)
        self.volume = QtWidgets.QDial(self.centralwidget)
        self.volume.setMaximum(10)
        self.volume.setPageStep(1)
        self.volume.setProperty("value", 5)
        self.volume.setObjectName("volume")
        self.verticalLayout_6.addWidget(self.volume)
        self.gridLayout.addLayout(self.verticalLayout_6, 1, 0, 1, 1)
        self.music_img = QtWidgets.QLabel(self.centralwidget)
        self.music_img.setText("")
        self.music_img.setObjectName("music_img")
        self.gridLayout.addWidget(self.music_img, 3, 0, 1, 1)
        self.gridLayout.setColumnStretch(0, 1)
        self.gridLayout.setColumnStretch(2, 5)
        self.gridLayout.setRowStretch(0, 9)
        self.gridLayout.setRowStretch(1, 3)
        self.gridLayout.setRowStretch(3, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.initialize()

    def initialize(self):
        self.ctrl_list=[]
        self.running=True
        self.random=False
        self.end_music=False
        self.current_music=0
        self.event=0
        self.define_musics()
        self.define_buttons()
        self.set_info_bar()
        
        self.mixer=Mixer()
        th=threading.Thread(target=self.tocar)
        th.daemon=True
        th.start()

        th=threading.Thread(target=self.update_bar)
        th.daemon=True
        th.start()

    def update_time_now(self,tempo):
        string=''
        if tempo<60:
            if len(str(int(tempo)))==1:
                string='0:0'+str(int(tempo))
            else:
                string='0:'+str(int(tempo))
        else:
            minutos=int(tempo/60)
            tempo=tempo-(60*minutos)
            if len(str(int(tempo)))==1:
                string='0'+str(minutos)+':0'+str(int(tempo))
            else:
                string='0'+str(minutos)+':'+str(int(tempo))
        self.time_now.setText(string+'  ')
        
    
    def update_bar(self):
        cont=0
        music_now=self.current_music
        while True:
            if music_now!=self.current_music:
                music_now=self.current_music
                cont=0
            if not self.mixer.pause:
                time.sleep(0.004)
                cont+=0.01
                self.time_music.setValue(cont)
                self.update_time_now(cont)
            if cont>=self.musics[self.current_music].length:
                self.end_music=True

    def set_info_bar(self):
        duration=self.musics[self.current_music].length

        st=str(duration/60)
        st=list(st)
        st[1]=':'
        st=st[:4]
        st=''.join(st)

        self.time_music.setMaximum(duration)
        self.max_time.setText('   '+st)
        self.time_music.setValue(0)
        self.time_now.setText('0:00')

        string=self.musics[self.current_music].nome+'\n\n'+self.musics[self.current_music].artist
        self.music_info.setText(string)

    def change_order(self):
        if not self.random:
            self.order.setStyleSheet("background-color: rgb(0, 255, 0);")
            self.random=True
        else:
            self.random=False
            self.order.setStyleSheet("background-color: rgb(25, 25, 25);")
        
    def define_buttons(self):
        icon = QtGui.QIcon()
        icon2 = QtGui.QIcon()
        icon3 = QtGui.QIcon()
        icon4 = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("next.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        icon2.addPixmap(QtGui.QPixmap("pause.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        icon3.addPixmap(QtGui.QPixmap("previous.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        icon4.addPixmap(QtGui.QPixmap("change.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        
        self.proxima.setIcon(icon)
        self.proxima.setIconSize(QtCore.QSize(32, 32))
        self.proxima.clicked.connect(self.next)

        self.pausar.setIcon(icon2)
        self.pausar.setIconSize(QtCore.QSize(32,32))
        self.pausar.clicked.connect(self.pause)

        self.anterior.setIcon(icon3)
        self.anterior.setIconSize(QtCore.QSize(32,32))
        self.anterior.clicked.connect(self.previous)

        self.order.setIcon(icon4)
        self.order.setIconSize(QtCore.QSize(16,16))
        self.order.clicked.connect(self.change_order)

        self.volume.setMaximum(10)
        self.volume.setMinimum(0)
        self.volume.setValue(5)
        self.volume.setSliderPosition(5)

        lista=[]
        for music in self.musics:
            lista.append(music.nome)
            if not music.artist in lista:
                lista.append(music.artist)
        completer=QCompleter(lista)
        self.search.setCompleter(completer)
        self.search.editingFinished.connect(self.get_music)

    def get_music(self):
        search=self.search.text()
        self.search.clear()
        if search!='':
            for i,music in enumerate(self.musics):
                if search==music.nome or search==music.artist:
                    self.ctrl_list.append(i)
                    break
            
    def define_musics(self):
        self.buttons=[]
        nordenado=define_musics()
        self.musics=merge_sort(nordenado)
        
        for i in range(len(self.musics)): #ordenar
            loc=str(i+1)+' .'+self.musics[i].nome+'\nalbum: '+self.musics[i].album+'\nartist: '+self.musics[i].artist
            button=Button(i,self.ctrl_list,self.scrollAreaWidgetContents_2,loc)
            button.bt.setStyleSheet("background-color: rgb(50, 50, 50);")
            self.buttons.append(button)
            self.verticalLayout_2.addWidget(self.buttons[i].bt)
        
    def pause(self):
        self.mixer.handle_event()

    def get_order(self,direction):
        if self.random:
            self.current_music=randint(0,len(self.musics)-1)
        elif direction=='+':
            if self.current_music<len(self.musics)-1:
                self.current_music+=1
            else:
                self.current_music=0
        else:
            if self.current_music<=0:
                self.current_music=len(self.musics)-1
            else:
                self.current_music-=1
            
        
    def next(self):
        self.get_order('+')
        self.ctrl_list.append(self.current_music)

    def previous(self):
        self.get_order('-')
        self.ctrl_list.append(self.current_music)

    def change_msc(self):
        i=self.ctrl_list.pop()

        self.current_music=i
        self.mixer.handle_event(self.musics[self.current_music].path)
        self.set_info_bar()
        pixmap=QtGui.QPixmap(self.musics[self.current_music].picture)
        pixmap=pixmap.scaled(128,128)
        self.music_img.setPixmap(pixmap)
        self.end_music=False

    def tocar(self):
        self.mixer.handle_event(self.musics[0].path)
        actual_vol=self.volume.value()
        actual_text=''
        while self.running:
            if self.ctrl_list!=[]:
                self.change_msc()
            elif self.end_music:
                self.next()
            elif actual_vol!=self.volume.value():
                self.mixer.set_volume(self.volume.value()/10)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Ainda n sei"))
        self.search.setPlaceholderText(_translate("MainWindow", "Pesquise o nome da música..."))
        self.max_time.setText(_translate("MainWindow", "0:00"))
        self.music_info.setText(_translate("MainWindow", "Musica"))
        self.proxima.setText(_translate("MainWindow", "\n"""))
        self.pausar.setText(_translate("MainWindow", "\n"""))
        self.anterior.setText(_translate("MainWindow", "\n"""))
        self.time_now.setText(_translate("MainWindow", "0:00"))
        self.label.setText(_translate("MainWindow", "Playlists"))
        self.create_plt.setText(_translate("MainWindow", "Criar Playlist"))
        
        
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

