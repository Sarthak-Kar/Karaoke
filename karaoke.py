import sqlite3
from lyricsgenius import Genius
import os
import shutil
from sqlite3.dbapi2 import Cursor
import urllib.request
import json
import urllib
from youtube_title_parse import get_artist_title

def refine_title(title):
    start=title.find('(')
    end=title.find(')')
    if(start!=-1 and end !=-1):
        title=title[:start] + title[end+1:]
    return title


path="C:\\Users\\Asus\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\2f2d0jsu.default\\places.sqlite"
c=sqlite3.connect(path) 
cursor=c.cursor()
cursor.execute("SELECT moz_places.last_visit_date, moz_places.url FROM moz_places ORDER BY last_visit_date DESC LIMIT 1")
result=cursor.fetchone()
#print(result[1])
params = {"format": "json", "url": result[1]}
url = "https://www.youtube.com/oembed"
query_string = urllib.parse.urlencode(params)
url = url + "?" + query_string

with urllib.request.urlopen(url) as response:
    response_text = response.read()
    data = json.loads(response_text.decode())
    #print(data['title'])
    artist, title=get_artist_title(data['title'])
    artist=refine_title(artist)
    title=refine_title(title)
    print(artist+" "+title)

genius = Genius('b8A_bHSkUWEbjyzE7p2fXEmWqwHLEfp6K5mbijbzzyAhSoP89y3WoSxeJQpr0LEV', remove_section_headers=True)
song=genius.search_songs(artist+" "+title)
try:
    url=(song['hits'][0]['result']['path'])
    print(genius.lyrics(song_url='https://genius.com'+url))

except:
    print("No lyrics found")
    try_again=input()
    song=genius.search_songs(try_again)
    url=(song['hits'][0]['result']['path'])
    print(genius.lyrics(song_url='https://genius.com'+url))

wait=input()




