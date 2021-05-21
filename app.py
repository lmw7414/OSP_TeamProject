#!/usr/bin/python3

from bs4 import BeautifulSoup as bs
#from selenium import webdriver
#import os
#import re
import urllib.request as ur
#import dload
from flask import Flask
from flask import render_template
from flask import request
import argparse
import subprocess
from flask import jsonify

app = Flask(__name__)

news = 'https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=0&ie=utf8&query=%EC%BD%94%EB%A1%9C%EB%82%98'
soup = bs(ur.urlopen(news).read(), 'html.parser')


pic =[]
pictures = soup.select('div.news_wrap.api_ani_send > a > img')
picture_num = 1
for picture in pictures:
    #print(picture['src']) #기사 썸네일 URL
    pic.append(picture['src'])
    img = picture['src']
    # dload.save(img, 'picture/img{}.jpg'.format(picture_num)) # 일단은 주석처리
    picture_num += 1  #dload.save를 이용하여 img파일을 내 프로젝트 폴더/picture폴더에 <<img숫자.jpg>>로 저장
#print()


comp =[]
time =[]
infos = soup.select('div.news_area > div.news_info > div.info_group')
for info in infos:
    #print(info.select_one('a').text.replace("언론사", "").replace("선정","")) #기사 언론사
    #print(info.select_one('span.info').text) #기사 시간
    comp.append(info.select_one('a').text.replace("언론사", "").replace("선정",""))
    time.append(info.select_one('span.info').text)
#print()


for i in soup.find_all('div',{"class":"news_area"}):
    for div_news_info in i.find_all('div',{"class":"news_info"}):
        div_news_info.extract() #<div class="news_area"> 속 <div class="news_info">를 제거


title = []
preview = []
titleurl = []
cnt = 0
for i in soup.find_all('div',{"class":"news_area"}):
#    print(comp[cnt])
#    print(time[cnt])

#    print(i.find_all('a')[0].get('title')) #기사 제목
    title.append(i.find_all('a')[0].get('title'))

#    print(i.find_all('a')[0].get('href'))  #기사 URL
    titleurl.append(i.find_all('a')[0].get('href'))
#    print(i.find_all('a')[1].text)  #기사 미리보기 내용
    preview.append(i.find_all('a')[1].text)
#    print(pic[cnt])
    cnt += 1

#    print()

@app.route('/')
def home():
	return render_template('home.html',comp = comp,time = time, title = title, preview = preview, titleurl = titleurl, pic = pic)

if __name__=='__main__':
	app.run(host='0.0.0.0', port=5000)
