#!/usr/bin/python
#-*- coding: utf-8 -*-
# html style settings

#모듈 추가
import article_analysis
import crawling
import db


import sys
import os
import re
import requests
import argparse
#import subprocess
from flask import Flask
from flask import render_template
from flask import request
from bs4 import BeautifulSoup as bs
from urllib import parse
import urllib.request as ur
from flask import jsonify
import urllib3
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from elasticsearch import Elasticsearch

# _for graph_
import pandas as pd
import matplotlib
import matplotlib.font_manager as fm
import matplotlib.pyplot as plt
import numpy as np

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
plt.rcParams['font.family'] = 'NanumGothicCoding'


es_host="127.0.0.1"
es_port="9200"

app = Flask(__name__)

#------------------------------------확진자 이동경로 파악 함수 정의--------------------------------
#대구
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
#경산
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

#포항
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

#부산
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
		if thnum > 54 :
			index.append(th.get_text())
		thnum+=1
	#내용
	num=1
	for i in my_para:
		if num==4 :
			busan_text=i.text.lstrip("\n\n")
			busanlist=busan_text.split('\n\n\n')
		num+=1

	for i in range(0, len(busanlist)):
		busanlist[i] =busanlist[i].split('\n')
	
	busan_path = pd.DataFrame(columns=index)
	for i in busanlist:
		if len(i) ==7:
			content = i
			busan_path.loc[len(busan_path)]= content
	
	path = busan_path.to_html(justify='center', index = False)
	with open('templates/path_busan.html', 'w') as f:
		f.write(html_string.format(city="부산광역시", style_1=style_1, style_2 =style_2, path=path))
	return render_template('path_busan.html')

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

    daejeon_all = soup.find('tbody').get_text().replace(u'\xa0',u'').lstrip()
    daejeon_split = daejeon_all.split("\n\n\n\n")

    pd.options.display.max_columns = None
    pd.options.display.max_rows = None

    daejeon_path = pd.DataFrame(columns = theadList)

    for i in range(0,len(daejeon_split)):
        split = daejeon_split[i].split("\n\n")
        content = []
        newcontent=[]
        for j in range(len(split)):
            if split[j]=='':
                continue
            else:
                content.append(split[j])

        if len(content) != 6:
            continue
        else:
            newcontent = content

        daejeon_path.loc[len(daejeon_path)] = newcontent

    path = daejeon_path.to_html(justify='center', index=False)
    with open('templates/path_daejeon.html', 'w') as f:
        f.write(html_string.format(city="대전광역시", style_1=style_1, style_2=style_2, path=path))

    return render_template('path_daejeon.html')


@app.route('/path')
def path():
    return render_template('post.html')


# ---------------------------------크롤링 관련 함수 정의--------------------------------------------
@app.route('/find_word')
def find_word():
	return render_template('/find_word.html')

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



# --------------------------------설문조사 관련 함수 정의 --------------------------------------------
@app.route('/survey_result', methods=['post'])
def show_survey():
	
	data1 = request.form.get('q1')
	data2 = request.form.get('q2')
	data3 = request.form.get('q3')
	data4 = request.form.get('q4')
	data5 = request.form.get('q5')
	data6 = request.form.get('q6')
	data7 = request.form.get('q7')
	data8 = request.form.get('q8')
	data9 = request.form.get('q9')
	data10 = request.form.get('q10')
	result_list, tt = db.calculate_survey(data1, data2, data3, data4, data5, data6, data7, data8, data9, data10)
	
	return render_template('survey_result.html', respondent = tt, rlist=result_list)

@app.route('/survey')
def do_survey():
	return render_template('survey.html')

# ----------------------------------그래프 관련 함수 정의--------------------------------------------
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


# ----------------------------------기사 분석 함수 정의---------------------------------------------
word_d ={}
sent_list=[]

@app.route('/1')
def analysis1():
	url1, url2 = article_analysis.analysis3()
	return render_template('/1.html', url1=url1, url2=url2)

@app.route('/1_')
def analysis2():
	url1, url2 = article_analysis.analysis3()

	#첫번째 url
	url1_sentence = article_analysis.make_string(url1)
	article_analysis.process_new_sentence(url1_sentence)
	#두번째url
	url2_sentence = article_analysis.make_string(url2)
	article_analysis.process_new_sentence(url2_sentence)

	v1 = article_analysis.make_vector(0)
	v2 = article_analysis.make_vector(1)

	dotpro = np.dot(v1, v2)
	cossimil = dotpro / (np.linalg.norm(v1) * np.linalg.norm(v2))
	return render_template('/1_.html',dotpro=dotpro, cossimil=cossimil)

@app.route('/2')
def get_url():
	return render_template('/2.html')

@app.route('/2_')
def show_url():
	url1 = request.args.get("url1")
	url2 = request.args.get("url2")
	#첫번째url
	url1_sentence = article_analysis.make_string(url1)
	article_analysis.process_new_sentence(url1_sentence)
	#두번째url
	url2_sentence = article_analysis.make_string(url2)
	article_analysis.process_new_sentence(url2_sentence)
	v1 = article_analysis.make_vector(0)
	v2 = article_analysis.make_vector(1)

	dotpro = np.dot(v1, v2)
	cossimil = dotpro / (np.linalg.norm(v1) * np.linalg.norm(v2))
	return render_template('/2_.html',url1= url1, url2= url2, dotpro=dotpro, cossimil=cossimil)

# ----------------------------------------나머지------------------------------------------------
@app.route('/quizz')
def quizz():
	return render_template('/quizz.html')


@app.route('/')
def index():
	comp =[]
	pic =[]
	time =[]
	title = []
	preview = []
	titleurl = []
	
	product1=[]
	product2=[]
	product3=[]

	patient_num_list=[]

	local_num_list=[]

	product1, product2, product3 = crawling.corona_product_list()
	comp, time, title, preview, titleurl, pic = crawling.find_news(comp, time, title, preview, titleurl, pic)
	patient_num_list = crawling.corona_patient_num()
	local_num_list = crawling.corona_local()

	return render_template("covid_web_height.html",comp=comp, time=time, title=title, preview=preview, titleurl=titleurl, pic=pic, product1 = product1, product2 = product2, product3 = product3, patient_num_list = patient_num_list, local_num_list = local_num_list)

if __name__ == '__main__':
	es = Elasticsearch([{'host':es_host, 'port':es_port}], timeout=30)
	app.run()
