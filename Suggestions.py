import sys
sys.path.append('C:\Sparrow\Files')
from Sparrow import *

Popular2016 = 'http://www.imdb.com/search/title?year=2016&sort=moviemeter,asc&view=simple'
MostPopular = 'http://www.imdb.com/chart/moviemeter?ref_=nv_mv_mpm_8'

YearJson = "C:\Sparrow\Year.json"
PopularJson = "C:\Sparrow\Popular.json"
          
def getYear(website):
    Movies = []
    s,r = http.request(website)
    soup = BeautifulSoup(r,'lxml')
    i=0
    for x in soup.select('span[class="lister-item-header"] a'):
        if i <=4:
            Movies.append(x.getText())
            i+=1
    return Movies

def getTableData(website,attrs={'class':'chart full-width'},lim=5):
    s,r= http.request(website)
    soup=BeautifulSoup(r,'lxml')
    data = []
    table = soup.find('table', attrs)
    table_body = table.find('tbody')
    rows = table_body.find_all('tr')
    i=0
    for row in rows:
        if i<=lim:
            cols = row.find_all('td')
            cols = [ele.text.strip() for ele in cols]
            data.append([ele for ele in cols if ele])
            i+=1
    return data

def getPopular(website):
    Movies = []
    data = getTableData(website)
    i=0
    for x in data:
        if len(x) == 3 and i <= 3:
            Movies.append(x[0].split('\n')[0])
            i+=1
    return Movies
            

def getGenre(genre):
    Movies = []
    site = "http://www.imdb.com/genre/" + genre + '/?ref_=gnr_mn_ac_mp'
    s,r = http.request(site)
    soup = BeautifulSoup(r,'lxml')
    rows = soup.select('table[class="results"] tr')
    data = []
    i=0
    for row in rows:
        if i<=2:
            cols=row.find_all('td')
            cols = [ele.text.strip() for ele in cols]
            data.append([ele for ele in cols if ele])
            i +=1
    for x in data:
        Movies.append(x[1].split('\n')[0])
    return Movies

def getSearched(movie):
    Movies = []
    site = 'http://www.imdb.com/find?q=' + "%20".join(movie.split()) + '&s=tt&ref_=fn_al_tt_mr'
    s,r = http.request(site)
    soup = BeautifulSoup(r,'lxml')
    rows = soup.select('table[class="findList"] tr')
    data = []
    i=0
    for row in rows:
        if i<5:
            cols=row.find_all('td')
            cols = [ele.text.strip() for ele in cols]
            data.append([ele for ele in cols if ele])
            i +=1
    for x in data:
        if len(x[0]) < len(x[0])+15 or x==data[0]:
            if 'Video' not in x[0] and 'TV' not in x[0]:
                Movies.append(x[0])
    return Movies

def WriteData():
    YearList = getYear(Popular2016)
    PopularList = getPopular(MostPopular)
    ##write an individual json file of getMovies foreach list and genre
    #suggestions is the parent file,stored as a json, containing 3 more dictionarys
    Popular = {}
    Year = {}
    Genres = {}
    for x in PopularList:
        Popular[x]=getMagnet(x)
        writeImage(x,'C:\Sparrow\Images')
    for x in YearList:
        Year[x] = getMagnet(x)
        writeImage(x,'C:\Sparrow\Images')
    for x in genres:
        y = {}
        for film in getGenres(x):
            writeImage(x,'C:\Sparrow\Images')
            y[film] = getMagnet(film)
        Genres[x] = y
    with open('C:\Sparrow\Suggestions.json','r') as f:
        try:
            Suggestions = json.load(f)
        except ValueError:
            Suggestions = {}
    Suggestions['Popular'] = Popular
    Suggestions['Year'] = Year
    Suggestions['Genres']= Genres
    with open('C:\Sparrow\Suggestions.json','w') as f:
        json.dump(Suggestions,f)
            


        
    
    
        
