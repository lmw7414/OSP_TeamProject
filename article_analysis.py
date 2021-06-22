#!/usr/bin/python

import sys
import os
import re
import requests
import argparse
from bs4 import BeautifulSoup as bs
from urllib import parse
import urllib.request as ur
import urllib3
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from elasticsearch import Elasticsearch

word_d ={}
sent_list=[]

def process_new_sentence(s):
	sent_list.append(s)
	tokenized = word_tokenize(s)
	for word in tokenized:
		if word not in word_d.keys():
			word_d[word]=0
		word_d[word] += 1

def make_vector(i):
	v= []
	s = sent_list[i]
	tokenized = word_tokenize(s)
	for w in word_d.keys():
		val = 0
		for t in tokenized:
			if t == w:
				val +=1
		v.append(val)
	return v

def make_string(url):
	html = ur.urlopen(url)
	soup = bs(html.read(), 'html.parser')
	url_text = soup.find_all('p')
	url_sentence =""
	for p in url_text:
		us=p.text
		us= re.sub('[-/,.“”—’\'%:]','', us)
		us = us.replace("''","")
		url_sentence += us	
	return url_sentence

def analysis3():
	url ='https://abcnews.go.com/Health/Coronavirus'
	html = ur.urlopen(url)
	soup = bs(html.read(), 'html.parser')
	my_para = soup.find_all('a', {"class" : "AnchorLink News__Item external flex flex-row"})

	url1 = my_para[0].attrs['href']
	url2 = my_para[1].attrs['href']

	return url1, url2







