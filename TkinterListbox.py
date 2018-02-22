from Tkinter import *
from PIL import ImageTk,Image
import json
from Sparrow import *
from Suggestions import *
from urllib2 import urlopen
import base64
import io
root = Tk()
root.title('Sparrow')
root.iconbitmap('C:\Sparrow\Icon\Sparrow.ico')
root.configure(bg='#000000')
root.geometry("260x570")

tileheight = "10"
tilewidth = "17"
#root.resizable(0,0)
# #244272
def is_ascii(s):
    return all(ord(c) < 128 for c in s)
def p(x):
    print x
def removeAka(s):
    l = []
    words = s.split()
    for x in words:
        if x=='aka':
            break
        else:
            l.append(x)
    return ' '.join(l)
class App:
    def __init__(self,master):
        self.master = master
        self.createWidgets()
        self.searchButtons = {}
        self.similarButtons = {}
    def addtoList(self,item):
        self.list.insert(END,item)
    def makeTitle(self):
        movie = self.searchbox.get()
        return movie
    def searchMovie(self):
        root.geometry("1100x630")
        self.searchButtons = {}
        self.similarButtons = {}
        movie = self.searchbox.get()
        search = getSearched(movie)
        similar = getSimilar(movie)
        col = 5
        r = 0
        for y in search:
            x = removeAka(makeSafeFilename(y))
            title = removeAka(y)
            if getImdb(title):
                #these allow the images to be stored on your hard drive
                path='C:\Sparrow\Images\\'+x+'.jpg'
                writeImage(getImage(title),path)
                #these pull them from the web
                #image_url = getImage(x)
                #image_byt = urlopen(image_url).read()
                
                #data_stream = io.BytesIO(image_byt)
                #pil_image = Image.open(data_stream)
                #img = ImageTk.PhotoImage(pil_image)
                img = ImageTk.PhotoImage(Image.open(path))
                self.searchButtons[title] = Button(self.main,
                                                   height=tileheight,
                                                   width=tilewidth,
                                                   text=title)
                self.searchButtons[title].image = img
                self.searchButtons[title].config(command=lambda y=self.searchButtons[title].cget('text'): self.onClick(y))
                self.searchButtons[title].grid(column = col,row =r)
                col+=1
                if col>9:
                    col=5
                    r+=1
        for y in similar:
            x = removeAka(makeSafeFilename(y))
            if y not in search:
                title = removeAka(y)
                if getImdb(title):
                    path='C:\Sparrow\Images\\'+x+'.jpg'
                    writeImage(getImage(title),path)

                    #image_url = getImage(x)
                    #image_byt = urlopen(image_url).read()
                    #data_stream = io.BytesIO(image_byt)
                    #pil_image = Image.open(data_stream)
                    #img = ImageTk.PhotoImage(pil_image)
                    img = ImageTk.PhotoImage(Image.open(path))
                    self.similarButtons[title] = Button(self.main,
                                                        height=tileheight,
                                                        width=tilewidth,
                                                        text=title)
                    self.similarButtons[title].image = img
                    self.similarButtons[title].config(command=lambda y=self.similarButtons[title].cget('text'): self.onClick(y))
                    self.similarButtons[title].grid(column = col,row =r)
                    col+=1
                    if col>9:
                        col=5
                        r+=1
            else:
                pass
    def onClick(self,y):
        self.list.insert(END,y)
        with open('C:\Sparrow\SavedList.json','r') as f:
            try:
                saved = json.load(f)
            except ValueError:
                saved = []
        saved.append(y)
        with open('C:\Sparrow\SavedList.json','w') as f:
            json.dump(saved,f)
            
    def getEm(self,b=False):
        movielist = self.list.get(0,END)
        with open('C:\Sparrow\SavedList.json','w') as f:
            json.dump([],f)
        getMovies(movielist,Data)
        waitandDownload(movielist[:6])
        waitandDownload(movielist[6:])
        self.list.delete(0,END)

    def add_and_Suggest(self):
        movie = self.searchbox.get()
        self.onClick(movie)
        root.geometry("600x600")
        self.suggestlabel = Label(text="Movies you might like",bg="#000000",fg="#ffffff",)
        self.suggestlabel.grid(column=2,row=0)
        self.suggestbox.config(height="20",width="30")
        for x in getSimilar(movie,2):
            self.suggestbox.insert(END,x)
    def createWidgets(self):
        #Frame of buttons of movie titles from the popular section
        self.main = Frame(root,bd="3",width="800",height="510",bg='#000000',
                          highlightbackground="#ffffff",relief="solid")
        self.main.grid(column=2,sticky="E",rowspan=10,row=0,columnspan=5)
        
        #List elements:
        self.e1 =Frame(height="30",width="210",bg="#000000",highlightbackground="#ffffff")
        self.e1.grid(column=0,row=0,columnspan=2,sticky="NW")
        self.etitle = Label(self.e1,text='Sparrow',fg="#ffffff",font='Impact',bg='#000000',justify="left")
        self.etitle.grid(padx=15,sticky="N")

        self.list = Listbox(root,width="30",height="18",bg="#000000",borderwidth=0,fg="#ffffff")
        self.list.grid(column=0,rowspan=7,columnspan=2,row=1,sticky="N",padx=7)

        self.download = Button(root,font="Impact",width="10",height="1",fg="#ffffff",
                               bg="#529B8F",text="Download",
                               command=lambda: self.getEm(True))
        self.download.grid(column=1,row=8,)

        self.clear = Button(root,font="Impact",width="10",height="1",fg="#ffffff",
                            bg="#529B8F",text="Remove",command=lambda: self.list.delete(END))
        self.clear.grid(column=0,row=8)

        self.searchbox =Entry(root,width=20)
        self.searchbox.grid(column=0,row=9,columnspan=2)

        self.search = Button(root,font="Impact",width="10",height="1",fg="#ffffff",
                             bg="#529B8F",text='Search',
                             command=lambda: self.searchMovie())
        self.search.grid(column=1,row=10)
        self.add = Button(root,font="Impact",width="10",height="1",fg="#ffffff",
                             bg="#529B8F",text='Add',
                             command=lambda:self.add_and_Suggest())
        self.add.grid(column=0,row=10,)
        
        self.suggestbox = Listbox(root,bg="#000000",width=0,height=0,fg="#ffffff")
        self.suggestbox.grid(column=2,row=1,rowspan=4)
        

        with open('C:\Sparrow\SavedList.json','r') as f:
            try:
                saved = json.load(f)
            except ValueError:
                saved = []
        for x in saved:
            self.list.insert(END,x)

        
App(root)
root.mainloop()
