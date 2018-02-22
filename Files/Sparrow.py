###I am trying to make Sparrow more modular to help in debugging
##Gonna be lit
##Start time: 10:56pm on a friday night #lit
import httplib2
from bs4 import BeautifulSoup, SoupStrainer
import json
import webbrowser
import requests
import pyautogui
import os
import subprocess
import keyboard
import time
import re

http = httplib2.Http()
httpcache = httplib2.Http('.cache')

Data = 'C:\Sparrow\ObjectData.json'
imageFolder = 'C:\Sparrow\Images\\'
buttonFolder = 'C:\Sparrow\Buttons\\'

def makeDirectories(dlist):
    for x in dlist:
        if not os.path.exists(x):
            os.makedirs(x)
        else:
            pass
def launchBetternet(b=False):
    if b:
        subprocess.Popen([r"C:\Program Files (x86)\Betternet\Betternet.exe"],shell=True)
    else:
        pass

def makeSafeFilename(inputFilename):
    cleaned_up_filename = re.sub(r"[/\\:*?'<>|!]", '', inputFilename)
    ''.join(i for i in cleaned_up_filename if ord(i)<128)
    return cleaned_up_filename

def getLink(url,selector,b=1):
    s,r = http.request(url)
    results = []
    a=0
    soup = BeautifulSoup(r,"html.parser",parse_only=SoupStrainer('a',href=True))
    for link in soup.find_all("a",href=True):
        if selector in link['href']:
            results.append(link['href'])
            a+=1
        if a == b:
            if b == 1:
                return results[0]
            else:
                return results
        else:
            pass
def getImdb(movie):
    title = '+'.join(movie.split())
    site = 'http://www.imdb.com/find?ref_=nv_sr_fn&q='+title+'&s=all'
    site1 = getLink(site,'title/tt')
    if site1 == None:
        return False
    else:
        link = 'http://www.imdb.com'+ site1
        return link

def getMagnet(m):#takes the name of a movie4
    try:
        movie = makeSafeFilename(m)
        PB = 'https://thepiratebay.org'
        site = PB + '/search/'
        if len(movie.split()) >1:
            for x in movie.split():
                if x != movie.split()[-1]:
                    site += x +'%20'
                else:
                    site += x
        else:
            site +=movie
        site += '/0/7/0'
        T = getLink(site,'/torrent/')
        newsite = PB + T
        return getLink(newsite,'magnet')
    except TypeError:
        if 'or' in movie.split():
            m=''
            for x in range(movie.split().index('or')):
                m+=movie.split()[x]
            return getMagnet(m)
        else:
            return None
                
            
def getImage(movie):#DONT FUCK WITH THIS IT WORKS and it returns a link
    if getImdb(movie):
        site = getImdb(movie)
        s,r = http.request(site)
        soup = BeautifulSoup(r,'lxml')
        link = soup.find(itemprop='image')
        image = link['src']
        return image
    else:
        return False


def getRating(movie):##returns a float
    try:
        site = getImdb(movie)
        ratesite = site[0:-16]+ 'ratings?ref_=tt_ov_rt'
        rating = getLink(ratesite,'user_rating')[-3:]
        return float(rating)
    except TypeError:
        return False

def getGenres(movie):##returns a list of genres
    genres = []
    site = getImdb(movie)
    s,r = http.request(site)
    soup = BeautifulSoup(r,'lxml')
    for x in soup.select('a > span[itemprop="genre"]'):
        genres.append(x.getText())
    return genres
    
def getSimilar(movie,b=6):
    similar = []
    site = getImdb(movie)
    s,r = http.request(site)
    soup = BeautifulSoup(r,'lxml')
    for x in soup.select('img[height="113"]')[0:b]:
        similar.append(x['title'])
    return similar

def getDirector(movie):
    site = getImdb(movie)
    s,r = http.request(site)
    soup = BeautifulSoup(r,'lxml')
    director = soup.select('span[itemprop="director"]')[0].getText()
    return director.strip()

def getCast(movie):
    Cast = []
    site = getImdb(movie)
    s,r = http.request(site)
    soup = BeautifulSoup(r,'lxml')
    t = soup.select('table[class="cast_list"] tr span[itemprop="name"]')
    for x in t:
        Cast.append(x.getText())
    return Cast

def writeImage(imageURL,imageFile):
    if not os.path.exists(imageFile) and imageURL:
        s,r = httpcache.request(imageURL)
        with open(imageFile,'wb') as f:
            f.write(r)
    else:
        pass
def getMovies(movielist,location):
    makeDirectories([location,imageFolder])
    with open(location,'r+') as f:
        try:
            Movies = json.load(f)
        except ValueError:
            Movies = {}
    for x in movielist:
        if x not in Movies and getImdb(x):
            if getRating(x):
                magnet = getMagnet(x)
                image = getImage(x)
                rating = getRating(x)
                genres = getGenres(x)
                #similar = getSimilar(x)
                #director = getDirector(x)
                #cast = getCast(x)
                ##write to json
                Movies[x.lower()] = [magnet,image,rating,genres]
        else:
            pass
    with open(location,'w+') as f:
        json.dump(Movies,f)

def waitandDownload(movielist):#takes a list of movies and time in seconds
    with open(Data,'r+') as f:
        try:
            Movies = json.load(f)
        except ValueError:
            return False
    for y in movielist:
        print y
        if y.lower() in Movies:
            link = Movies[y.lower()][0]
            webbrowser.open(link)
    try:
        Button = pyautogui.locateOnScreen(buttonFolder + 'UB.png')
        Center = pyautogui.center(Button)
        for x in movielist:
            pyautogui.click(Center)
    except TypeError:
        for x in movielist:
            keyboard.press_and_release('enter')
            time.sleep(.3)
            keyboard.press_and_release('enter')

def Sparrow(movielist,b=False):
    launchBetternet(b)
    getMovies(movielist,Data)
    waitandDownload(movielist)



