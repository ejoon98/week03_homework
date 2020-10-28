import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.dbsparta

headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36'}
data = requests.get('https://comic.naver.com/webtoon/list.nhn?titleId=651673&weekday=sat')
soup = BeautifulSoup(data.text, 'html.parser')
trs=soup.select('#content > table > tr')

for tr in trs:
    name = tr.select_one('td > a')

    if name is None:
        continue

    naming=name["href"]

    img = tr.select_one('td > a > img')

    if img is None:
        continue

    imgsrc = img["src"]

    title_tag=tr.select_one('td.title > a')

    if title_tag is None:
        continue
    title = title_tag.text

    rate_tag = tr.select_one('td > div.rating_type > strong')

    if rate_tag is None:
        continue
    rate = rate_tag.text

    date_tag=tr.select_one('td.num')

    if date_tag is None:
        continue
    date = date_tag.text

    data = {
        'naming' : naming,
        'imgsrc' : imgsrc,
        'title' : title,
        'rate' : rate,
        'date' : date


    }

    print(naming, imgsrc, title, rate, date)
    db.webtoon.insert_one(data)



