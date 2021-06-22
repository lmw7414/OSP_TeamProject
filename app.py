#!/usr/bin/python3
#-*- coding: utf-8 -*-
# html style settings
html_string = '''
<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<title>{city} 확진자 이동경로</title>
<style>
table{style_1}
table, th, td{style_2}
</style>
</head>
<body>
{path}
</body>
<button type="button" class="navyBtn" onClick="location.href='/path'">돌아가기</button>
</html>
'''
style_1 = '''
{
margin: 0px;
text-align: center;
border: 1px solid #444444;
border-collapse: collapse;
table-layout: auto;
word-wrap: break-word;
}
'''

style_2='''
border-bottom: 1px solid #444444;
padding: 10px;
border: 1px solid #bcbcbc;
font-size: small;
}
'''

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
import urllib.request as ur
from flask import jsonify
import urllib3

# _for graph_
import pandas as pd
import matplotlib
import matplotlib.font_manager as fm
import matplotlib.pyplot as plt
import numpy as np

#path = '/usr/share/fonts/truetype/nanum/NanumBarunGothic.ttf'
#fontprop = fm.FontProperties(fname=path, size=20)
#print(fontprop)
plt.rcParams['font.family'] = 'NanumGothicCoding'


app = Flask(__name__)

# 서현
@app.route('/daegu_path', methods=['GET'])
def path_daegu():
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    url = 'http://covid19.daegu.go.kr/00937400.html'
    res = requests.get(url)

    html = bs(res.content, "html.parser")

    daegu_all = html.find('tbody').get_text().rstrip()
    daegu_split = daegu_all.split("\n\n\n\n")
    # print(daegu_split)

    table = html.find_all('th')
    index = []
    for i in range(len(table)):
        index.append(table[i].get_text())
    
    daegu_path = pd.DataFrame(columns=index)
    for i in range(1,len(daegu_split)):
        content = daegu_split[i].split("\n\n")    
        #print(content)
        daegu_path.loc[len(daegu_path)] = content

    path = daegu_path.to_html(justify='center', index=False)
    with open('templates/path_daegu.html', 'w') as f:
        f.write(html_string.format(city="대구광역시", style_1=style_1, style_2=style_2, path=path))

    return render_template('path_daegu.html')

@app.route('/gyeongsan_path', methods=['GET'])
def path_gs():
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    url = 'https://www.gbgs.go.kr/programs/coronaMoveNew/coronaMoveNew.do'
    res = requests.get(url)

    html = bs(res.content, "html.parser")

    index = html.find('tr').get_text().strip().split("\n")
    # print(index)

    gs_all = html.find_all('tbody')
    gs_path = pd.DataFrame(columns=index)
    for i in range(len(gs_all)):
        split = "".join(gs_all[i].get_text().lstrip()).split("\n")
        content = []
        for j in range(len(index)):
            if split[j] == "":
                content.append("-")
            else:
                content.append(split[j])
        # print(content)
        gs_path.loc[len(gs_path)] = content

    path = gs_path.to_html(justify='center', index=False)
    with open('templates/path_gs.html', 'w') as f:
        f.write(html_string.format(city="경산시", style_1=style_1, style_2=style_2, path=path))

    return render_template('path_gs.html')

@app.route('/pohang_path', methods=['GET'])
def path_pohang():
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    url = 'https://www.pohang.go.kr/COVID-19/9568/subview.do'
    res = requests.get(url, verify=False)

    html = bs(res.content, "html.parser")

    index = html.find('tr').get_text().strip().split("\n")
    # print(index)

    ph_all = html.find_all('tr')
   
    ph_path = pd.DataFrame(columns=index)
    for i in range(1, len(ph_all)):
        split = "".join(ph_all[i].get_text().lstrip()).split("\n")
        content = []
        for j in range(len(index)):
            if split[j] == "":
                content.append("-")
            else:
                content.append(split[j])
        # print(content)
        ph_path.loc[len(ph_path)] = content

    path = ph_path.to_html(justify='center', index=False)
    with open('templates/path_pohang.html', 'w') as f:
        f.write(html_string.format(city="포항시", style_1=style_1, style_2=style_2, path=path))

    return render_template('path_pohang.html')
# ----서현 추가1----

# 서현2
@app.route('/index')
def index_graph():
	# ###_고용관련_
	고용 = pd.read_csv("data/고용.csv")
	고용['연월'] = 고용['연월'].astype(str)
	#print(고용.head())
	취업자 = 고용[고용['유형별'] == '취업자'].reset_index().drop(['index', '유형별'], axis=1)
	실업자 = 고용[고용['유형별'] == '실업자'].reset_index().drop(['index', '유형별'], axis=1)
	실업률 = 고용[고용['유형별'] == '실업률'].reset_index().drop(['index', '유형별'], axis=1)
	고용률 = 고용[고용['유형별'] == '고용률'].reset_index().drop(['index', '유형별'], axis=1)

	# ### _취업자 및 고용률 추이_
	fig1 = plt.figure(figsize=(20, 10))
	ax1_1 = fig1.add_subplot()
	ax1_1.plot(list(고용률['연월'][12:]), list(고용률['15세이상'][12:]), 
		 color='dodgerblue', label='15세이상고용률', linewidth=3
		)
	ax1_1.set_ylim([50, 70])
	ax1_1.tick_params(axis='y', labelsize=20)
	ax1_1.set_ylabel('고용률(%)', fontsize=18)
	ax1_1.set_xticklabels(고용률['연월'], fontsize=20, rotation=45)
	ax1_1.plot(list(고용률['연월'][12:]), list(고용률['15-64세'][12:]), 
		 color='skyblue', label='15-64세 고용률', linewidth=3)
	ax1_1.legend(loc='upper left', ncol=2, fontsize=20)

	ax1_2 = ax1_1.twinx()
	ax1_2.bar(list(취업자['연월'][12:]), list(취업자['15세이상'][12:]), color='gray', label='취업자', align='center')
	ax1_2.set_ylim([25000, 30000])
	ax1_2.tick_params(axis='y', labelsize=20)
	ax1_2.set_ylabel('취업자(천명)', fontsize=18)
	ax1_2.legend(['취업자'], loc='upper right', fontsize=20)

	plt.xticks(ticks=취업자['연월'][12:], labels=취업자['연월'][12:], rotation=45, fontsize=20)
	plt.locator_params(axis='x', nbins=len(취업자['연월'][12:])/4)
	plt.title('취업자 및 고용률 추이\n', fontsize=20)

	fig1.savefig('static/graph/employed.png')

	# ### _실업자 및 실업률 추이_
	fig2 = plt.figure(figsize=(20, 10))

	ax2_1 = fig2.add_subplot()
	ax2_1.plot(list(실업률['연월'][12:]), list(실업률['15세이상'][12:]), 
		 color='coral', label='실업률', linewidth=3)
	ax2_1.set_ylim([0, 6])
	ax2_1.tick_params(axis='y', labelsize=20)
	ax2_1.set_ylabel('실업률(%)', fontsize=18)
	ax2_1.set_xticklabels(실업률['연월'][12:], fontsize=20, rotation=45)
	ax2_1.legend(['실업률'], loc='upper left', fontsize=20)

	ax2_2 = ax2_1.twinx()
	ax2_2.bar(list(실업자['연월'][12:]), list(실업자['15세이상'][12:]), color='gray', label='실업자', align='center')
	ax2_2.set_ylim([500, 1700])
	ax2_2.tick_params(axis='y', labelsize=20)
	ax2_2.set_ylabel('실업자(천명)', fontsize=18)
	ax2_2.legend(['실업자'], loc='upper right', fontsize=20)

	plt.xticks(ticks=실업자['연월'][12:], labels=실업자['연월'][12:], rotation=45, fontsize=20)
	plt.locator_params(axis='x', nbins=len(실업자['연월'][12:])/4)
	plt.title('실업자 및 실업률 추이\n', fontsize=20)
	#plt.show()

	fig2.savefig('static/graph/unemployed.png')
		

	# ### __온라인 쇼핑__
	온라인쇼핑 = pd.read_csv("data/온라인쇼핑.csv")
	온라인쇼핑['연월'] = 온라인쇼핑['연월'].astype(str)
	온라인쇼핑['합계'] = 온라인쇼핑['합계']/100
	#온라인쇼핑.head()

	#print(min(온라인쇼핑['합계']))
	#print(max(온라인쇼핑['합계']))

	# ## _온라인 쇼핑 동향_

	fig3 = plt.figure(figsize=(20, 10))
	ax3_1 = fig3.add_subplot()
	ax3_1.bar(list(온라인쇼핑['연월']), list(온라인쇼핑['합계']), color='lightgray', label='거래액', align='center')
	ax3_1.set_ylim([20000, 180000])
	ax3_1.tick_params(axis='y', labelsize=20)
	ax3_1.set_ylabel('거래액(억원)', fontsize=18)
	ax3_1.set_xticklabels(온라인쇼핑['연월'], fontsize=20, rotation=45)
	ax3_1.legend(['온라인쇼핑거래액'], loc='upper left', fontsize=20)

	ax3_2 = ax3_1.twinx()
	ax3_2.plot(list(온라인쇼핑['연월']), list(온라인쇼핑['전년동월비']), 
		 color='indigo', label='전년동월비', linewidth=3.5)
	ax3_2.set_ylim([0, 50])
	ax3_2.tick_params(axis='y', labelsize=20)
	ax3_2.set_xlabel('월별', fontsize=20)
	ax3_2.set_ylabel('비율(%)', fontsize=18)
	ax3_2.legend(['전년동월비'], loc='upper right', fontsize=20)

	plt.xticks(ticks=온라인쇼핑['연월'], labels=온라인쇼핑['연월'], rotation=45, fontsize=20)
	plt.locator_params(axis='x', nbins=len(온라인쇼핑['연월'])/2)
	plt.title('온라인 쇼핑 동향\n', fontsize=20)
	#plt.show()

	fig3.savefig('static/graph/online_shopping.png')

	# ### __소비자물가지수__
	소비자물가지수 = pd.read_csv("data/물가.csv")
	소비자물가지수 = pd.DataFrame(소비자물가지수.transpose())
	소비자물가지수.columns = 소비자물가지수.loc['품목성질별', :]
	소비자물가지수 = 소비자물가지수.drop(['품목성질별'])
	#소비자물가지수.head()

	월별 = list(소비자물가지수.index)
	전월비 = list(소비자물가지수.loc[:, "전월비"])
	전년동월비 = list(소비자물가지수.loc[:, "전년동월비"])

	fig4 = plt.figure(figsize=(20, 10))

	ax4_1 = fig4.add_subplot()
	ax4_1.plot(월별, 전년동월비, color='coral', label='전년동월비', linewidth=3)
	ax4_1.set_ylim([-4, 6])
	ax4_1.tick_params(axis='y', labelsize=20)
	ax4_1.set_xlabel('Month', fontsize=20)
	ax4_1.set_ylabel('전년동월비(%)', fontsize=22)
	ax4_1.legend(['전년동월비'], loc='upper left', fontsize=20)
	ax4_1.set_xticklabels(월별, fontsize=20, rotation=45)

	ax4_2 = ax4_1.twinx()
	ax4_2.bar(월별, 전월비, color='gray', label='전월비', align='edge')
	ax4_2.set_ylim([-2, 3])
	ax4_2.tick_params(axis='y', labelsize=20)
	ax4_2.set_ylabel('전월비(%)', fontsize=22)
	ax4_2.legend(['전월비'], loc='upper right', fontsize=20)

	plt.xticks(ticks=월별, labels=월별, rotation=45, fontsize=20)
	plt.locator_params(axis='x', nbins=len(월별)/4)
	plt.title('소비자물가동향\n', fontsize=20)
	#plt.show()

	fig4.savefig('static/graph/price.png')

	# ###__html__
	return render_template('index.html')
#----서현2 fin----

@app.route('/corona_product_list')
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

	pic2 = soup2.select('a.thumb > img')
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

#주연이
@app.route('/news_list')
def find_news(comp, time, title, preview, titleurl, pic):
	news = 'https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=0&ie=utf8&query=%EC%BD%94%EB%A1%9C%EB%82%98'
	soup = bs(ur.urlopen(news).read(), 'html.parser')
	pictures = soup.select('div.news_wrap.api_ani_send > a > img')
	picture_num = 1
	for picture in pictures:
		#print(picture['src']) #기사 썸네일 URL
		pic.append(picture['src'])
		img = picture['src']
		# dload.save(img, 'picture/img{}.jpg'.format(picture_num)) # 일단은 주석처리
		picture_num += 1  #dload.save를 이용하여 img파일을 내 프로젝트 폴더/picture폴더에 <<img숫자.jpg>>로 저장
		#print()
	
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
	return comp, time, title, preview, titleurl, pic


#대전
#대전
@app.route('/daejeon_path')
def path_daejeon2():
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    
    target_url = 'https://www.daejeon.go.kr/corona19/index.do?menuId=0008'
    html = ur.urlopen(target_url).read()
    soup = bs(html, 'html.parser')

    thead = soup.find('table', {'class':'corona'}).find_all('th')
    theadList = []
    for i in range(len(thead)):
        if i == 6:
            continue
        theadList.append(thead[i].get_text().replace('\n','')) #theadList는 '비고'를 없앤 상태. len = 6

    #print(theadList)


    daejeon_all = soup.find('tbody').get_text().replace(u'\xa0',u'').lstrip()
    #print(daejeon_all)
    daejeon_split = daejeon_all.split("\n\n\n\n")
    #print(daejeon_split)
    #print(len(daejeon_split))
    #print()

    pd.options.display.max_columns = None
    pd.options.display.max_rows = None

    daejeon_path = pd.DataFrame(columns = theadList)

    for i in range(0,len(daejeon_split)):
        split = daejeon_split[i].split("\n\n")
        #print(i)
        #print(len(split))
        #print(split)
        #print()

        content = []
        newcontent=[]
        for j in range(len(split)):
            if split[j]=='':
                continue
            else:
                content.append(split[j])
        #print(len(content))
        #print(content)
        #print()
        if len(content) != 6:
            continue
        else:
            newcontent = content
        #print(len(newcontent))
        #print(newcontent)
        #print()
        daejeon_path.loc[len(daejeon_path)] = newcontent

    #print(daejeon_path)

    path = daejeon_path.to_html(justify='center', index=False)
    with open('templates/path_daejeon.html', 'w') as f:
        f.write(html_string.format(city="대전광역시", style_1=style_1, style_2=style_2, path=path))

    return render_template('path_daejeon.html')

#민우
@app.route('/find_word')
def find_word():
	return render_template('find_word.html')
#민우
@app.route('/word_list')
def word_list():
	idx=0
	word = request.args.get("word")
	result = parse.quote(word)
	pageNum=1
	url = f'http://ncov.mohw.go.kr/tcmBoardList.do?pageIndex={pageNum}&brdId=3&brdGubun=&board_id=&search_item=1&search_content={result}'
	name_list=[]
	href_list=[]
	url_source=[]
	html = ur.urlopen(url)
	soup = bs(html.read(), 'html.parser')
	my_para = soup.find_all('a', {"class" : "bl_link"})
	countNum = int(soup.find('strong').get_text())
	num=countNum
	print(countNum)
	while countNum !=1 :
		url = f'http://ncov.mohw.go.kr/tcmBoardList.do?pageIndex={pageNum}&brdId=3&brdGubun=&board_id=&search_item=1&search_content={result}'
		html = ur.urlopen(url)
		soup = bs(html.read(), 'html.parser')
		my_para = soup.find_all('a', {"class" : "bl_link"})
		for i in my_para:
			
			us=i.attrs['onclick']
			name_list.append(i.text)
			us = us.replace("fn_tcm_boardView","")
			us= re.sub('[\';() ]','', us)
			us=us.split(',')
			url_source = us
			make_url="http://ncov.mohw.go.kr" + url_source[0] +"?brdId="+ url_source[1] + "&brdGubun="+url_source[2]+ "&dataGubun=&ncvContSeq=" + url_source[3] +"&contSeq=" + url_source[3] + "&board_id=" + url_source[4] +"&gubun=" +url_source[5]
			href_list.append(make_url)
			if countNum !=0:
				countNum-=1
		if countNum ==0 :
			break
		pageNum+=1;
	return render_template('/word_list.html',num=num, name_list=name_list, href_list=href_list)

#민우
'''
@app.route('/busan_path')
def busan_path():
	url = 'https://www.busan.go.kr/covid19/Travelhist.do'

	busanlist=[]
	llist=[]
	#html = ur.urlopen(url)
	#soup = BeautifulSoup(html.read(), 'html.parser')
	#my_para = soup.find_all('a', {"class" : "bl_link"})
	html = ur.urlopen(url)
	soup = bs(html.read(), 'html.parser')
	my_para = soup.find_all('tbody')
	table = soup.find_all('th')
	index = []
	
	#데이터프레임 리스트 검색
	thnum=1
	for th in table:
		#print(thnum)
		#print(th)
		if thnum > 54 :
			index.append(th.get_text())
		thnum+=1
	#내용
	num=1
	for i in my_para:
		#print(int(num))
		#print(i.text)
		if num==4 :
			busan_text=i.text.lstrip("\n\n")
			#print(busan_text)
			busanlist=busan_text.split('\n\n\n')
		num+=1


	#print(busanlist)
	#busanres=[]
	for i in range(0, len(busanlist)):
		#print(busanlist[i].split('\n'))
		busanlist[i] =busanlist[i].split('\n')

	print(busanlist)
	print(len(index))

	sido=[]
	sigugun=[]
	jangso=[]
	sangho=[]
	address=[]
	nochul=[]
	sodok=[]
	for i in busanlist:
		if len(i) ==7:
			sido.append(i[0])
			sigugun.append(i[1])
			jangso.append(i[2])
			sangho.append(i[3])
			address.append(i[4])
			nochul.append(i[5])
			sodok.append(i[6])
	return render_template('/busan_path.html',num = int(len(sido)),index=index, sidolist=sido, sigugunlist=sigugun, jangsolist=jangso, sangholist=sangho, addresslist=address,nochullist=nochul,sodoklist=sodok)
'''

@app.route('/busan_path')
def busan_path():
	urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
	url = 'https://www.busan.go.kr/covid19/Travelhist.do'
	res = requests.get(url)
	busanlist=[]
	llist=[]
	
	html = bs(res.content,"html.parser")
	my_para = html.find_all('tbody')
	table = html.find_all('th') # 데이터 이름 검색
	index = []
	
	
	#데이터프레임 리스트 검색
	thnum=1
	for th in table:
		#print(thnum)
		#print(th)
		if thnum > 54 :
			index.append(th.get_text())
		thnum+=1
	#print(index)
	#내용
	num=1
	for i in my_para:
		#print(int(num))
		#print(i.text)
		if num==4 :
			busan_text=i.text.lstrip("\n\n")
			#print(busan_text)
			busanlist=busan_text.split('\n\n\n')
		num+=1


	#print(busanlist)
	#busanres=[]
	for i in range(0, len(busanlist)):
		#print(busanlist[i].split('\n'))
		busanlist[i] =busanlist[i].split('\n')
	
	busan_path = pd.DataFrame(columns=index)
	for i in busanlist:
		if len(i) ==7:
			content = i
			busan_path.loc[len(busan_path)]= content
		
	#print(busan_path)
	
	path = busan_path.to_html(justify='center', index = False)
	with open('templates/path_busan.html', 'w') as f:
		f.write(html_string.format(city="부산광역시", style_1=style_1, style_2 =style_2, path=path))
	return render_template('path_busan.html')

@app.route('/path')
def show_path():
    return render_template("post.html")

@app.route('/')
def index():
	comp =[]
	pic =[]
	time =[]
	title = []
	preview = []
	titleurl = []
	index_pic = []
	employ_pic = []
	online_shopping_pic = []
	price_pic = []
	
	product1=[]
	product2=[]
	product3=[]
	product1, product2, product3 = corona_product_list()
	comp, time, title, preview, titleurl, pic = find_news(comp, time, title, preview, titleurl, pic)
 	
	return render_template("covid_web_height.html",comp=comp, time=time, title=title, preview=preview, titleurl=titleurl, pic=pic, product1 = product1, product2 = product2, product3 = product3)

if __name__ == '__main__':
	app.run()
