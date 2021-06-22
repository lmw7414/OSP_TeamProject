#!/usr/bin/python

import sys
import os
import re
import requests
import argparse
#import subprocess
from bs4 import BeautifulSoup as bs
from urllib import parse
import urllib.request as ur
from flask import jsonify
import urllib3


# 모듈
def corona_product_list():
	product1_list=[]
	product2_list=[]
	product3_list=[]
	###마스크
	target_url1 = 'https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=1&ie=utf8&query=%EB%A7%88%EC%8A%A4%ED%81%AC'
	html1 = ur.urlopen(target_url1).read()
	soup1 = bs(html1, 'html.parser')
	
	product1 = soup1.select_one('div.product_info > a')
	
	product1_href = product1['href']  #구매링크
	product1_list.append(product1_href)
	pic1 = soup1.select('a.thumb > img')
	pic1_url = pic1[0]['src']
	
	#pic1_url = pic1 #사진링크
	product1_list.append(pic1_url)
	title1 = soup1.select_one('div.product_info > a')
	title1 = title1.text #상품명
	product1_list.append(title1)

	price1 = soup1.select_one('div.product_info > div.price_area > div.price')
	price1 = price1.text #상품가격
	product1_list.append(price1)

	store1 = soup1.select_one('div.elss.store > a')
	store1 = store1.text #판매처
	product1_list.append(store1)

	###손소독제
	target_url2 = 'https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=1&ie=utf8&query=%EC%86%90%EC%86%8C%EB%8F%85%EC%A0%9C'
	html2 = ur.urlopen(target_url2).read()
	soup2 = bs(html2, 'html.parser')

	product2 = soup2.select_one('div.product_info > a')
	product2_href = product2['href']  #구매링크
	product2_list.append(product2_href)

	pic2 = soup2.select('a.thumb > img')
	pic2_url = pic2[0]['src']
	product2_list.append(pic2_url)

	title2 = soup2.select_one('div.product_info > a')
	title2 = title2.text #상품명
	product2_list.append(title2)

	price2 = soup2.select_one('div.product_info > div.price_area > div.price')
	price2 = price2.text #상품가격
	product2_list.append(price2)

	store2 = soup2.select_one('div.elss.store > a')
	store2 = store2.text #판매처
	product2_list.append(store2)

	###코로나자가진단키트
	target_url3 = 'https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=0&ie=utf8&query=%EC%BD%94%EB%A1%9C%EB%82%98+%EC%9E%90%EA%B0%80%EC%A7%84%EB%8B%A8+%ED%82%A4%ED%8A%B8'
	html3 = ur.urlopen(target_url3).read()
	soup3 = bs(html3, 'html.parser')

	product3 = soup3.select_one('div.product_info > a')
	product3_href = product3['href']  #구매링크
	product3_list.append(product3_href)

	pic3 = soup3.select('a.thumb > img')
	pic3_url = pic3[0]['src'] #사진링크
	product3_list.append(pic3_url)

	title3 = soup3.select_one('div.product_info > a')
	title3 = title3.text #상품명
	product3_list.append(title3)

	price3 = soup3.select_one('div.product_info > div.price_area > div.price')
	price3 = price3.text #상품가격
	product3_list.append(price3)

	store3 = soup3.select_one('div.elss.store > a')
	store3 = store3.text #판매처
	product3_list.append(store3)
	
	return product1_list, product2_list, product3_list

#모듈
def find_news(comp, time, title, preview, titleurl, pic):
    news = 'https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=0&ie=utf8&query=%EC%BD%94%EB%A1%9C%EB%82%98'
    soup = bs(ur.urlopen(news).read(), 'html.parser')
    pictures = soup.select('div.news_wrap.api_ani_send')
    picture_num = 1
    pic = []
    for i in range(len(pictures)):
        imgtest = pictures[i].select('a > img')
        if(len(imgtest) == 0):
            #준비한 빈 사진 넣고
            pic.append("https://11luuvtufne6f2y33i1nvedi-wpengine.netdna-ssl.com/wp-content/uploads/2017/10/no-image-icon.png")
        else:
            pic.append(str(imgtest).split("src=\"")[1].split("\"")[0])
            img = str(imgtest).split("src=\"")[1].split("\"")[0]
            picture_num += 1
   
    infos = soup.select('div.news_area > div.news_info > div.info_group')
    for info in infos:
        comp.append(info.select_one('a').text.replace("언론사", "").replace("선정",""))
        time.append(info.select_one('span.info').text)


    for i in soup.find_all('div',{"class":"news_area"}):
        for div_news_info in i.find_all('div',{"class":"news_info"}):
            div_news_info.extract() #<div class="news_area"> 속 <div class="news_info">를 제거

    cnt = 0
    for i in soup.find_all('div',{"class":"news_area"}):
        #    print(i.find_all('a')[0].get('title')) #기사 제목
        title.append(i.find_all('a')[0].get('title'))
        #    print(i.find_all('a')[0].get('href'))  #기사 URL
        titleurl.append(i.find_all('a')[0].get('href'))
        #    print(i.find_all('a')[1].text)  #기사 미리보기 내용
        preview.append(i.find_all('a')[1].text)
        cnt += 1
    return comp, time, title, preview, titleurl, pic

#모듈
def corona_patient_num():
    target_url = 'https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=0&ie=utf8&query=%EC%BD%94%EB%A1%9C%EB%82%98'
    html = ur.urlopen(target_url).read()
    soup = bs(html, 'html.parser')

    first = soup.select_one('li.info_01 > p.info_num').get_text() # 확진환자
    second = soup.select_one('li.info_03 > p.info_num').get_text() # 격리해제
    third = soup.select_one('li.info_04 > p.info_num').get_text() # 사망자
    fourth = soup.select_one('li.info_02 > p.info_num').get_text() # 검사진행

    patient_num = []
    patient_num.append(first)
    patient_num.append(second)
    patient_num.append(third)
    patient_num.append(fourth)

    return patient_num

#모듈
def corona_local():
    target_url = 'http://ncov.mohw.go.kr/bdBoardList_Real.do?brdId=1&brdGubun=13&ncvContSeq=&contSeq=&board_id=&gubun='
    html = ur.urlopen(target_url).read()
    soup = bs(html, 'html.parser')
    #총 17개
    #서울 부산 대구 인천 광주 대전 울산 세종 경기 강원 충북 충남 전북 전남 경북 경남 제주 순서
    local_num = []
    temps = soup.select('table.num.midsize > tbody > tr')
    for temp in temps:
    	local_num.append(temp.select_one('td.number').get_text())
    return local_num


if __name__ == '__main__':
	es = Elasticsearch([{'host':es_host, 'port':es_port}], timeout=30)
	app.run()
