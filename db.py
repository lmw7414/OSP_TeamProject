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

import urllib3
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from elasticsearch import Elasticsearch

es_host="127.0.0.1"
es_port="9200"

def create_index(index):
	if not es.indices.exists(index=index):
		return es.indices.create(index = index)

def insert(index, doc_type, body):
	return es.index(index = index, doc_type=doc_type, body=body)

def search(data=None, body=None):
	if data is None:
		data = {"match_all": {}}
	else:
		data = {"match" : data}
	body = {"query": data }
	res = es.search(index="survey" , body = body)
	return res

def calculate_survey(d1, d2, d3, d4, d5, d6, d7, d8, d9, d10):
	result_list=[]
	doc = {"q1": d1, "q2" : d2, "q3": d3, "q4" : d4, "q5" : d5, "q6" : d6, "q7" : d7, "q8" : d8, "q9" : d9, "q10" : d10}
	st =create_index("survey")
	res = insert('survey', 'survey_result', doc)
	respondent = es.count(index ="survey")
	q1_1 = search({'q1' :'a1_1' })
	Q1_1 = int(q1_1['hits']['total']['value'])
	result_list.append(Q1_1)
	q1_2 = search({'q1' :'a1_2' })
	Q1_2 = int(q1_2['hits']['total']['value']) 
	result_list.append(Q1_2)
	q1_3 = search({'q1' :'a1_3' })
	Q1_3 = int(q1_3['hits']['total']['value'])
	result_list.append(Q1_3)
	q1_4 = search({'q1' :'a1_4' })
	Q1_4 = int(q1_4['hits']['total']['value']) 
	result_list.append(Q1_4)
	q1_5 = search({'q1':'a1_5'})
	Q1_5 = int(q1_5['hits']['total']['value']) 
	result_list.append(Q1_5)
	q1_6 = search({'q1':'a1_6'})
	Q1_6 = int(q1_6['hits']['total']['value']) 
	result_list.append(Q1_6)
	q1_7 = search({'q1' : 'a1_7'})
	Q1_7 = int(q1_7['hits']['total']['value']) 
	result_list.append(Q1_7)
	q1_8 = search({'q1' : 'a1_8'})
	Q1_8 = int(q1_8['hits']['total']['value'])
	result_list.append(Q1_8)

	q2_1 =search({'q2' : 'a2_1'})
	Q2_1 = int(q2_1['hits']['total']['value']) 
	result_list.append(Q2_1)
	q2_2 =search({'q2' : 'a2_2'})
	Q2_2 = int(q2_2['hits']['total']['value'])
	result_list.append(Q2_2)
	q2_3 =search({'q2' : 'a2_3'})
	Q2_3 = int(q2_3['hits']['total']['value'])
	result_list.append(Q2_3)
	q2_4 =search({'q2' : 'a2_4'})
	Q2_4 = int(q2_4['hits']['total']['value'])
	result_list.append(Q2_4)
	q2_5 =search({'q2' : 'a2_5'})
	Q2_5 = int(q2_5['hits']['total']['value'])
	result_list.append(Q2_5)
	q2_6 =search({'q2' : 'a2_6'})
	Q2_6 = int(q2_6['hits']['total']['value'])
	result_list.append(Q2_6)
	q2_7 =search({'q2' : 'a2_7'})
	Q2_7 = int(q2_7['hits']['total']['value'])
	result_list.append(Q2_7)

	q3_1 = search({'q3' : 'a3_1'})
	Q3_1 = int(q3_1['hits']['total']['value'])
	result_list.append(Q3_1)
	q3_2 = search({'q3' : 'a3_2'})
	Q3_2 = int(q3_2['hits']['total']['value'])
	result_list.append(Q3_2)
	q3_3 = search({'q3' : 'a3_3'})
	Q3_3 = int(q3_3['hits']['total']['value'])
	result_list.append(Q3_3)
	q3_4 = search({'q3' : 'a3_4'})
	Q3_4 = int(q3_4['hits']['total']['value'])
	result_list.append(Q3_4)
	q3_5 = search({'q3' : 'a3_5'})
	Q3_5 = int(q3_5['hits']['total']['value'])
	result_list.append(Q3_5)

	q4_1 = search({'q4' : 'a4_1'})
	Q4_1 = int(q4_1['hits']['total']['value']) 
	result_list.append(Q4_1)
	q4_2 = search({'q4' : 'a4_2'})
	Q4_2 = int(q4_2['hits']['total']['value'])
	result_list.append(Q4_2)
	q4_3 = search({'q4' : 'a4_3'})
	Q4_3 = int(q4_3['hits']['total']['value']) 
	result_list.append(Q4_3)
	q4_4 = search({'q4' : 'a4_4'})
	Q4_4 = int(q4_4['hits']['total']['value']) 
	result_list.append(Q4_4)
	q4_5 = search({'q4' : 'a4_5'})
	Q4_5 = int(q4_5['hits']['total']['value'])
	result_list.append(Q4_5)

	q5_1 = search({'q5' : 'a5_1'})
	Q5_1 = int(q5_1['hits']['total']['value']) 
	result_list.append(Q5_1)
	q5_2 = search({'q5' : 'a5_2'})
	Q5_2 = int(q5_2['hits']['total']['value']) 
	result_list.append(Q5_2)
	q5_3 = search({'q5' : 'a5_3'})
	Q5_3 = int(q5_3['hits']['total']['value']) 
	result_list.append(Q5_3)
	q5_4 = search({'q5' : 'a5_4'})
	Q5_4 = int(q5_4['hits']['total']['value'])
	result_list.append(Q5_4)
	q5_5 = search({'q5' : 'a5_5'})
	Q5_5 = int(q5_5['hits']['total']['value']) 
	result_list.append(Q5_5)

	q6_1 = search({'q6' : 'a6_1'})
	Q6_1 = int(q6_1['hits']['total']['value']) 
	result_list.append(Q6_1)
	q6_2 = search({'q6' : 'a6_2'})
	Q6_2 = int(q6_2['hits']['total']['value']) 
	result_list.append(Q6_2)
	q6_3 = search({'q6' : 'a6_3'})
	Q6_3 = int(q6_3['hits']['total']['value']) 
	result_list.append(Q6_3)
	q6_4 = search({'q6' : 'a6_4'})
	Q6_4 = int(q6_4['hits']['total']['value']) 
	result_list.append(Q6_4)
	q6_5 = search({'q6' : 'a6_5'})
	Q6_5 = int(q6_5['hits']['total']['value'])
	result_list.append(Q6_5)

	q7_1 = search({'q7' : 'a7_1'})
	Q7_1 = int(q7_1['hits']['total']['value']) 
	result_list.append(Q7_1)
	q7_2 = search({'q7' : 'a7_2'})
	Q7_2 = int(q7_2['hits']['total']['value']) 
	result_list.append(Q7_2)
	q7_3 = search({'q7' : 'a7_3'})
	Q7_3 = int(q7_3['hits']['total']['value'])
	result_list.append(Q7_3)
	q7_4 = search({'q7' : 'a7_4'})
	Q7_4 = int(q7_4['hits']['total']['value'])
	result_list.append(Q7_4)
	q7_5 = search({'q7' : 'a7_5'})
	Q7_5 = int(q7_5['hits']['total']['value']) 
	result_list.append(Q7_5)
	q7_6 = search({'q7' : 'a7_6'})
	Q7_6 = int(q7_6['hits']['total']['value'])
	result_list.append(Q7_6)
	q7_7 = search({'q7' : 'a7_7'})
	Q7_7 = int(q7_7['hits']['total']['value'])
	result_list.append(Q7_7)

	q8_1 = search({'q8' : 'a8_1'})
	Q8_1 = int(q8_1['hits']['total']['value'])
	result_list.append(Q8_1)
	q8_2 = search({'q8' : 'a8_2'})
	Q8_2 = int(q8_2['hits']['total']['value'])
	result_list.append(Q8_2)	

	q9_1 =search({'q9' : 'a9_1'})
	Q9_1 = int(q9_1['hits']['total']['value'])
	result_list.append(Q9_1)
	q9_2 =search({'q9' : 'a9_2'})
	Q9_2 = int(q9_2['hits']['total']['value']) 
	result_list.append(Q9_2)
	q9_3 =search({'q9' : 'a9_3'})
	Q9_3 = int(q9_3['hits']['total']['value']) 
	result_list.append(Q9_3)
	q9_4 =search({'q9' : 'a9_4'})
	Q9_4 = int(q9_4['hits']['total']['value'])
	result_list.append(Q9_4)
	q9_5 =search({'q9' : 'a9_5'})
	Q9_5 = int(q9_5['hits']['total']['value']) 
	result_list.append(Q9_5)
	q9_6 =search({'q9' : 'a9_6'})
	Q9_6 = int(q9_6['hits']['total']['value'])
	result_list.append(Q9_6)

	q10_1 = search({'q10' : 'a10_1'})
	Q10_1 = int(q10_1['hits']['total']['value'])
	result_list.append(Q10_1)
	q10_2 = search({'q10' : 'a10_2'})
	Q10_2 = int(q10_2['hits']['total']['value'])
	result_list.append(Q10_2)
	q10_3 = search({'q10' : 'a10_3'})
	Q10_3 = int(q10_3['hits']['total']['value'])
	result_list.append(Q10_3)
	q10_4 = search({'q10' : 'a10_4'})
	Q10_4 = int(q10_4['hits']['total']['value'])
	result_list.append(Q10_4)
	q10_5 = search({'q10' : 'a10_5'})
	Q10_5 = int(q10_5['hits']['total']['value'])
	result_list.append(Q10_5)
	q10_6 = search({'q10' : 'a10_6'})
	Q10_6 = int(q10_6['hits']['total']['value'])
	result_list.append(Q10_6)
	tt =int(respondent['count'])
	return result_list, tt


	return render_template("covid_web_height.html",comp=comp, time=time, title=title, preview=preview, titleurl=titleurl, pic=pic, product1 = product1, product2 = product2, product3 = product3, patient_num_list = patient_num_list, local_num_list = local_num_list)


es = Elasticsearch([{'host':es_host, 'port':es_port}], timeout=30)
