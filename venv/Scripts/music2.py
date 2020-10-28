import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.dbsparta

headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36 Edg/86.0.622.51'}
data = requests.get('https://www.genie.co.kr/chart/top200?ditc=D&rtm=N&ymd=20200713',headers=headers)
soup = BeautifulSoup(data.text, 'html.parser')
trs=soup.select('#body-content > div.newest-list > div.music-list-wrap > table.list-wrap > tbody > tr')

for tr in trs:
    rate_tag = tr.select_one('td.number')

    if rate_tag is None:
        continue

    rate = rate_tag.text[0:2].strip()


    name = tr.select_one('td.info > a.title.ellipsis')

    if name is None:
        continue

    naming=name.text.strip()

    artist = tr.select_one('td.info > a.artist.ellipsis')

    if artist is None:
        continue

    artisting=artist.text.strip()

    data = {
        'rate': rate,
        'naming': naming,
        'artisting': artisting,

    }

    print(rate,naming,artisting)
    db.music.insert_one(data)



