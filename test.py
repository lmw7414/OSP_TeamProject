#!/usr/bin/python3

import sys
import os
import re
import requests
import argparse
import subprocess
from flask import Flask
from flask import render_template
from flask import request
from bs4 import BeautifulSoup as bs
from urllib import parse
import pandas as pd
import urllib.request as ur
from flask import jsonify
import urllib3


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
	#print(product1_href)
	product1_list.append(product1_href)
	pic1 = soup1.select('a.thumb > img')
	pic1_url = pic1[0]['src']
	#picList1 = []
	#for pic1 in pic1:
	#	picList1.append(pic1['src'])
	#print(picList1[0])
	#pic1_url = pic1 #사진링크
	product1_list.append(pic1_url)

	title1 = soup1.select_one('div.product_info > a')
	#print(title1.text)
	title1 = title1.text #상품명
	product1_list.append(title1)

	price1 = soup1.select_one('div.product_info > div.price_area > div.price')
	#print(price1.text)
	price1 = price1.text #상품가격
	product1_list.append(price1)

	store1 = soup1.select_one('div.elss.store > a')
	#print(store1.text)
	store1 = store1.text #판매처
	product1_list.append(store1)

	###손소독제
	target_url2 = 'https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=1&ie=utf8&query=%EC%86%90%EC%86%8C%EB%8F%85%EC%A0%9C'
	html2 = ur.urlopen(target_url2).read()
	soup2 = bs(html2, 'html.parser')

	product2 = soup2.select_one('div.product_info > a')
	#print(product2['href'])
	product2_href = product2['href']  #구매링크
	product2_list.append(product2_href)

	pic2 = soup2.select('a.thumb> img')
	pic2_url = pic2[0]['src']
	#picList2 = []
	#for pic2 in pic2:
	#	picList2.append(pic2['src'])
	#print(picList2[0])
	#pic2_url = pic2#사진링크
	product2_list.append(pic2_url)

	title2 = soup2.select_one('div.product_info > a')
	#print(title2.text)
	title2 = title2.text #상품명
	product2_list.append(title2)

	price2 = soup2.select_one('div.product_info > div.price_area > div.price')
	#print(price2.text)
	price2 = price2.text #상품가격
	product2_list.append(price2)

	store2 = soup2.select_one('div.elss.store > a')
	#print(store2.text)
	store2 = store2.text #판매처
	product2_list.append(store2)





	###코로나자가진단키트
	target_url3 = 'https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=0&ie=utf8&query=%EC%BD%94%EB%A1%9C%EB%82%98+%EC%9E%90%EA%B0%80%EC%A7%84%EB%8B%A8+%ED%82%A4%ED%8A%B8'
	html3 = ur.urlopen(target_url3).read()
	soup3 = bs(html3, 'html.parser')

	product3 = soup3.select_one('div.product_info > a')
	#print(product3['href'])
	product3_href = product3['href']  #구매링크
	product3_list.append(product3_href)

	pic3 = soup3.select('a.thumb > img')
	#print(type(pic3))
	#print(pic3[0])
	#picList3 = []
	#print(pic3[0]['src'])
	pic3_url = pic3[0]['src'] #사진링크
	#print(pic3_url)
	product3_list.append(pic3_url)
	title3 = soup3.select_one('div.product_info > a')
	#print(title3.text)
	title3 = title3.text #상품명
	product3_list.append(title3)
	price3 = soup3.select_one('div.product_info > div.price_area > div.price')
	#print(price3.text)
	price3 = price3.text #상품가격
	product3_list.append(price3)
	store3 = soup3.select_one('div.elss.store > a')
	#print(store3.text)
	store3 = store3.text #판매처
	product3_list.append(store3)
	#print(product1_list)
	#print(product2_list)
	#print(product3_list)
	return product1_list, product2_list, product3_list

corona_product_list()

