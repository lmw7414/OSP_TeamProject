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
import pandas as pd
import urllib.request as ur
from flask import jsonify
import urllib3

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
# ----서현 추가----


@app.route('/corona_product_list')
def corona_product_list():
	###마스크
	target_url1 = 'https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=1&ie=utf8&query=%EB%A7%88%EC%8A%A4%ED%81%AC'
	html1 = ur.urlopen(target_url1).read()
	soup1 = bs(html1, 'html.parser')

	product1 = soup1.select_one('div.shop_product.type_ad.v1.api_ani_send > a')
	#print(product1['href'])
	product1_href = product1['href']  #구매링크

	pic1 = soup1.select('div.shop_product.type_ad.v1.api_ani_send > a > img')
	picList1 = []
	for pic1 in pic1:
		picList1.append(pic1['src'])
	#print(picList1[0])
	pic1_url = picList1[0] #사진링크

	title1 = soup1.select_one('div.product_info > a')
	#print(title1.text)
	title1 = title1.text #상품명

	price1 = soup1.select_one('div.product_info > div.price_area > div.price')
	#print(price1.text)
	price1 = price1.text #상품가격

	store1 = soup1.select_one('div.elss.store > a')
	#print(store1.text)
	store1 = store1.text #판매처

	###손소독제
	target_url2 = 'https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=1&ie=utf8&query=%EC%86%90%EC%86%8C%EB%8F%85%EC%A0%9C'
	html2 = ur.urlopen(target_url2).read()
	soup2 = bs(html2, 'html.parser')

	product2 = soup2.select_one('div.shop_product.type_ad.v1.api_ani_send > a')
	#print(product2['href'])
	product2_href = product2['href']  #구매링크

	pic2 = soup2.select('div.shop_product.type_ad.v1.api_ani_send > a > img')
	picList2 = []
	for pic2 in pic2:
		picList2.append(pic2['src'])
	#print(picList2[0])
	pic2_url = picList2[0] #사진링크

	title2 = soup2.select_one('div.product_info > a')
	#print(title2.text)
	title2 = title2.text #상품명

	price2 = soup2.select_one('div.product_info > div.price_area > div.price')
	#print(price2.text)
	price2 = price2.text #상품가격

	store2 = soup2.select_one('div.elss.store > a')
	#print(store2.text)
	store2 = store2.text #판매처





	###코로나자가진단키트
	target_url3 = 'https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=0&ie=utf8&query=%EC%BD%94%EB%A1%9C%EB%82%98+%EC%9E%90%EA%B0%80%EC%A7%84%EB%8B%A8+%ED%82%A4%ED%8A%B8'
	html3 = ur.urlopen(target_url3).read()
	soup3 = bs(html3, 'html.parser')

	product3 = soup3.select_one('div.shop_product.type_ad.v1.api_ani_send > a')
	#print(product3['href'])
	product3_href = product3['href']  #구매링크

	pic3 = soup3.select('div.shop_product.type_ad.v1.api_ani_send > a > img')
	picList3 = []
	for pic3 in pic3:
		picList3.append(pic3['src'])
	#print(picList3[0])
	pic3_url = picList3[0] #사진링크

	title3 = soup3.select_one('div.product_info > a')
	#print(title3.text)
	title3 = title3.text #상품명

	price3 = soup3.select_one('div.product_info > div.price_area > div.price')
	#print(price3.text)
	price3 = price3.text #상품가격

	store3 = soup3.select_one('div.elss.store > a')
	#print(store3.text)
	store3 = store3.text #판매처

	return render_template('corona_product_list.html',product1_href = product1_href, pic1_url = pic1_url, title1 = title1, price1 = price1, store1 = store1, product2_href = product2_href, pic2_url = pic2_url, title2 = title2, price2=price2, store2 = store2, product3_href = product3_href, pic3_url = pic3_url, title3 = title3, price3 = price3, store3 = store3)


#주연이
@app.route('/news_list')
def find_news():
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
	return render_template('news_list.html',comp = comp,time = time, title = title, preview = preview, titleurl = titleurl, pic = pic)


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

#@app.route('/path')
#def show_path():
#    return render_template("post.html")

@app.route('/')
def index():
    return render_template("covid_web_height_origin.html")

if __name__ == '__main__':
	app.run()
