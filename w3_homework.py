import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.misicchat

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
data = requests.get('https://www.genie.co.kr/chart/top200?ditc=D&rtm=Y', headers=headers)

soup = BeautifulSoup(data.text,'html.parser')


lists = soup.select('#body-content > div.newest-list > div > table > tbody > tr')


for music in lists:
    music.select_one('td.number > span').decompose()
    rank = music.select_one('td.number').text.strip()
    title = music.select_one('a.title.ellipsis').text.strip()
    singer = music.select_one('a.artist.ellipsis').text
    doc = {
        'rank': rank,
        'title': title,
        'artits': singer
    }

    print(rank,title,singer)
    db.misicchat.update_one({'rank': rank}, {'$set' : {'title': title}}, upsert = True)
    db.misicchat.update_one({'rank': rank}, {'$set' : {'artits': singer}}, upsert = True)