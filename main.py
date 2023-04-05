from bs4 import BeautifulSoup
import requests
import mysql.connector
source = requests.get('https://www.imdb.com/chart/top/')
htmlcontent=source.content
soup=BeautifulSoup(htmlcontent,'html.parser')
movies=soup.find('tbody',class_='lister-list').find_all('tr')

i=1
for movie in movies:
    name=movie.find('td',class_='titleColumn').find('a')
    rating=movie.find('td',class_='ratingColumn imdbRating')
    year=movie.find('td',class_='titleColumn').find('span',class_='secondaryInfo')
    print(i,name.text,year.text.strip("()"),rating.text.strip('\n'))
    i=i+1
#///////////////////////////////////////

# To store in a mysql Databse

mydb=mysql.connector.connect(host='localhost', user='root', password='******', database='imdb')
cur=mydb.cursor()
q1="create table imdb(S_no integer(4), Name varchar(100), year integer(4), rating float(2.2))"
q2="insert into imdb values(%s,%s,%s,%s)"
cur.execute(q1)
values=[]
j=1
for movie in movies:
    name=movie.find('td',class_='titleColumn').find('a')
    rating=movie.find('td',class_='ratingColumn imdbRating')
    year=movie.find('td',class_='titleColumn').find('span',class_='secondaryInfo')
    values.extend([j,name.text,year.text.strip("()"),rating.text.strip("\n")])
    cur.execute(q2,values)
    j=j+1
    values.clear()
mydb.commit()