import pygame
from tkinter.filedialog import askdirectory,askopenfilename
import os
import sys
import threading
from mutagen.mp3 import MP3
from mutagen.id3 import ID3
from tkinter import *
import time
import tkinter.messagebox as messagebox

def browse_file():
    global is_paused
    global realnames
    global is_muted
    global length
    global index
    file_path=askopenfilename(filetypes=[("MP3 media","*.mp3")])
    if not file_path:
        return
    if not listofsongs:
        pygame.mixer.init()
        is_paused=True
        is_muted=False
    listofsongs.append(file_path)
    realdir=os.path.realpath(file_path)
    audio=ID3(realdir)
    if audio['TIT2']:
        realname=audio['TIT2'].text[0]
    else:
        realname="Unkown Title"
    listbox.insert(END,realname)
    realnames.append(realname)
    length.append(MP3(realdir).info.length)
    #updatelabel()
    if len(listofsongs)==1:
        songlabel['text'] = realnames[index] + "-ready"
        show_detail(index)
        index=0
        listbox.select_set(index)

def directorychooser():
    global  realnames
    global is_paused
    global is_muted
    global index
    temp_realnames=[]
    temp_filelist=[]
    directory=askdirectory()
    if not directory:
        return
    os.chdir(directory)
    for files in os.listdir(directory):
        if files.endswith('.mp3'):
            '''
            realdir=os.path.realpath(files)
            audio=ID3(realdir)
            if audio['TIT2']:
                temp_realnames.append(audio['TIT2'].text[0])
            else:
                temp_realnames.append('Unkown Title')
            listofsongs.append(files)
            length.append(MP3(realdir).info.length)
            '''
            temp_filelist.append(files)
   # global listbox
    if not temp_filelist:
      return
    if not listofsongs:
        pygame.mixer.init()
        is_paused=True
        is_muted=False
    for files in temp_filelist:
      realdir = os.path.realpath(files)
      audio = ID3(realdir)
      if audio['TIT2']:
        temp_realnames.append(audio['TIT2'].text[0])
      else:
        temp_realnames.append('Unkown Title')
      listofsongs.append(files)
      length.append(MP3(realdir).info.length)
    for name in temp_realnames:
        listbox.insert(END, name)
        realnames.append(name)
    if len(listofsongs)==len(temp_realnames):
        index=0
        songlabel['text'] = realnames[index] + "-ready"
        show_detail(index)
        listbox.select_set(index)

def remove():
    if listbox.curselection():
        to_remove=int(listbox.curselection()[0])
        global index,listofsongs,realnames,length
        if index==to_remove:
            pygame.mixer.music.stop()
            songlabel['text']='Welcome'
            lengthlabel['text']='--:--'
            currentlabel['text']='--:--'
        listofsongs.pop(to_remove)
        realnames.pop(to_remove)
        length.pop(to_remove)
        listbox.delete(to_remove)
        index%=len(listofsongs)
        listbox.select_set(index)
        listbox.activate(index)

def helpinfo():
    messagebox.showinfo("Ying!","A simple MP3 player designed by Silver.")

def nextsong(event):
    global index
    global is_paused
    global is_muted
    if is_paused==None or is_muted==None:
        return
    index+=1
    index%=len(listofsongs)
    pygame.mixer.music.stop()
    time.sleep(1.01)
    pygame.mixer.music.load(listofsongs[index])
    if is_paused==False:
        pygame.mixer.music.play()
        songlabel['text'] = realnames[index] + "-playing"
    elif is_paused==True:
        songlabel['text']=realnames[index]+"-paused"
    show_detail(index)
    listbox.selection_clear(0,END)
    listbox.select_set(index)
    listbox.activate(index)

def prevsong(event):
    global index
    global is_paused
    global is_muted
    if is_paused==None or is_muted==None:
        return
    index-=1
    index%=len(listofsongs)
    pygame.mixer.music.stop()
    time.sleep(1.01)
    pygame.mixer.music.load(listofsongs[index])
    if is_paused==False:
        pygame.mixer.music.play()
        songlabel['text'] = realnames[index] + "-playing"
    elif is_paused==True:
        songlabel['text'] = realnames[index] + "-paused"
    show_detail(index)
    listbox.selection_clear(0,END)
    listbox.select_set(index)
    listbox.activate(index)

def stopsong(event):

    global is_paused
    global is_muted
    if is_paused==None or is_muted==None:
        return
    is_paused = True
    playbutton['image']=play_logo
    pygame.mixer.music.stop()
    pygame.mixer.init()
    is_paused=False
    songlabel['text'] = realnames[index] + "-stoped"
    currentlabel['text']='00:00'

def play_pause(event):
    global  is_paused
    global is_muted
    global index
    if is_muted==None or is_paused==None:
        return

    if pygame.mixer.music.get_busy():
        if int(listbox.curselection()[0])==index:
            if is_paused:
                pygame.mixer.music.unpause()
                is_paused=False
                playbutton['image']=pause_logo
                songlabel['text']=realnames[index]+"-playing"
            else:
                pygame.mixer.music.pause()
                is_paused=True
                playbutton['image']=play_logo
                songlabel['text'] = realnames[index] + "-paused"
        else:
            index=int(listbox.curselection()[0])
            if is_paused:
                pygame.mixer.music.stop()
                pygame.mixer.music.load(listofsongs[index])
                is_paused=False
                playbutton['image']=pause_logo
                songlabel['text']=realnames[index]+"-playing"
                pygame.mixer.music.play()
                show_detail(index)
            else:
                pygame.mixer.music.stop()
                is_paused=True
                playbutton['image']=play_logo
                songlabel['text'] = realnames[index] + "-paused"
    else:
        index=int(listbox.curselection()[0])
        pygame.mixer.music.load(listofsongs[index])
        pygame.mixer.music.play()
        is_paused=False
        playbutton['image']=pause_logo
        songlabel['text'] = realnames[index] + "-playing"
        show_detail(index)

def set_vol(val):
    global curr_vol
    curr_vol = int(val)
    if is_paused!=None and is_muted==False:
        pygame.mixer.music.set_volume(int(val)/100)

       # print(curr_vol)

def mute(event):
    global is_muted
    if is_muted!=None:
        if is_muted:
            pygame.mixer.music.set_volume(curr_vol/100)
            is_muted=False
            mutebutton.config(image=mute_logo)
        else:
            pygame.mixer.music.set_volume(0)
            is_muted=True
            mutebutton.config(image=unmute_logo)

def on_closing():
    if pygame.mixer.get_init():
        pygame.mixer.music.stop()
    root.destroy()

def show_detail(index):
    total_length=length[index]
    mins, secs = divmod(total_length, 60)
    mins = round(mins)
    secs = round(secs)
    timeformat = '{:02d}:{:02d}'.format(mins, secs)
    lengthlabel['text'] = timeformat
    currentlabel['text']='00:00'

    t1=threading.Thread(target=time_count,args=(total_length,))
    t1.start()


def time_count(total_length):
    global is_paused
    current_length=0
    while current_length<=total_length and pygame.mixer.music.get_busy():
        if is_paused:
            continue
        else:
            mins, secs = divmod(current_length, 60)
            mins = round(mins)
            secs = round(secs)
            timeformat = '{:02d}:{:02d}'.format(mins, secs)
            currentlabel['text'] = timeformat
            time.sleep(1)
            current_length+=1
    if current_length>total_length:
        songlabel['text']=realnames[index]+'-finished'
    sys.exit()

root=Tk()
root.title('Ying!')

listofsongs=[]
realnames=[]
length=[]
is_paused=None
is_muted=None
curr_vol=100

menubar=Menu(root)
root.config(menu=menubar)

subMenu1=Menu(menubar, tearoff=0)
menubar.add_cascade(label="File", menu=subMenu1)
subMenu1.add_command(label="Open file", command=browse_file)
subMenu1.add_command(label="Open directory", command=directorychooser)
subMenu1.add_command(label="Remove selected", command=remove)

subMenu2=Menu(menubar,tearoff=0)

menubar.add_cascade(label="Help", menu=subMenu2)
subMenu2.add_command(label="About us", command=helpinfo)
index=0

Topframe=Frame(root)
Topframe.grid(row=0,column=0,columnspan=4,rowspan=3,sticky=E+W+N+S)

listbox=Listbox(Topframe,relief=SUNKEN)
listbox.grid(row=0,column=0,columnspan=3,rowspan=3,padx=30)
subFrame=Frame(Topframe)
subFrame.grid(row=0,column=3,rowspan=3,sticky=E)

try:
   wd = sys._MEIPASS
except AttributeError:
   wd = os.getcwd()
add_file_logo=PhotoImage(file=os.path.join(wd,"icons/icons8-add-file-filled-50.png"))
add_file_button=Button(subFrame,image=add_file_logo,command=browse_file)
add_file_button.pack(side=TOP)


add_folder_logo=PhotoImage(file=os.path.join(wd,"icons/icons8-add-folder-filled-50.png"))
add_folder_button=Button(subFrame,image=add_folder_logo,command=directorychooser)
add_folder_button.pack(side=TOP)

remove_logo=PhotoImage(file=os.path.join(wd,"icons/icons8-trash-filled-50.png"))
remove_button=Button(subFrame,image=remove_logo,command=remove)
remove_button.pack(side=TOP)

prev_logo=PhotoImage(file=os.path.join(wd,"icons/icons8-rewind-filled-50.png"))
prevbutton=Button(root,image=prev_logo)
prevbutton.grid(row=3,column=0,sticky=N+W+E)
prevbutton.bind("<Button-1>",prevsong)

play_logo=PhotoImage(file=os.path.join(wd,"icons/icons8-play-button-circled-filled-50.png"))
pause_logo=PhotoImage(file=os.path.join(wd,"icons/icons8-pause-button-filled-50.png"))
playbutton=Button(root,image=play_logo)
playbutton.grid(row=3,column=1,sticky=N+W+E)
playbutton.bind("<Button-1>",play_pause)

next_logo=PhotoImage(file=os.path.join(wd,"icons/icons8-fast-forward-filled-50.png"))
nextbutton=Button(root,image=next_logo)
nextbutton.grid(row=3,column=2,sticky=N+W+E)
nextbutton.bind("<Button-1>",nextsong)

stop_logo=PhotoImage(file=os.path.join(wd,"icons/icons8-stop-filled-50.png"))
stopbutton=Button(root,image=stop_logo)
stopbutton.grid(row=3,column=3,sticky=N+W+E)
stopbutton.bind("<Button-1>",stopsong)


scale=Scale(root,from_=100,to=0,orient=VERTICAL,command=set_vol)
scale.set(100)
scale.grid(row=0,column=4,sticky=W+S)

statusbar=Frame(root,relief=SUNKEN)
statusbar.grid(row=4,columnspan=5)
songlabel=Label(statusbar,text='Welcome',width=35)
songlabel.grid(row=0,column=0,sticky=S+N)

lengthlabel=Label(statusbar,text='--:--')
lengthlabel.grid(row=0,column=2,sticky=S+N+W+E)

currentlabel=Label(statusbar,text='--:--')
currentlabel.grid(row=0,column=1,sticky=S+N+W+E)

mute_logo=PhotoImage(file=os.path.join(wd,"icons/icons8-no-audio-filled-50.png"))
unmute_logo=PhotoImage(file=os.path.join(wd,"icons/icons8-sound-filled-50.png"))
mutebutton=Button(root,image=mute_logo)
mutebutton.bind("<Button-1>",mute)
mutebutton.grid(row=3,column=4,sticky=N+W+E)

root.protocol("WM_DELETE_WINDOW",on_closing)
root.mainloop()
