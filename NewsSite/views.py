from django.shortcuts import render,redirect   # 加入 redirect 套件
from django.contrib.auth import authenticate
from django.contrib import auth
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
import json
from .modules.crawl import Crawler
from .models import News
from .modules.calsentiment import *
from snownlp import SnowNLP
import datetime
import random 
import time

def calSnownlp(article):

	posprob = 1
	negprob = 1
	for sentence in article:
		tmpPos=SnowNLP(sentence).sentiments
		posprob *= tmpPos
		negprob *= (1 - tmpPos)

	pos = posprob / (posprob + negprob)
	neg = negprob / (posprob + negprob)

	return pos, neg


def calwithDict(article):

	pos_path = "./NewsSite/modules/positives.txt"
	neg_path = "./NewsSite/modules/negatives.txt"

	with open(pos_path, 'r') as f:
		pos_dict = [line.split("\n") for line in f.readlines()]
	with open(neg_path, 'r') as f:
		neg_dict = [line.split("\n") for line in f.readlines()]
	print("POSDICT, NEGDICT", pos_dict, "===", neg_dict)
	posscore = 0
	negscore = 0
	for sentence in article:
		for term in jieba.cut(sentence):
			if term in pos_dict:
				posscore += 1
			elif term in neg_dict:
				negscore += 1
	if posscore > negscore:
		return 1, 0
	else:
		return 0, 1


def calSentimentScore(article):

	pos_path = "./NewsSite/modules/pos_json.txt"
	neg_path = "./NewsSite/modules/neg_json.txt"
	pos_dict = LoadDict(pos_path)
	neg_dict = LoadDict(neg_path)    
	SumofPosdict = sum(Counter(pos_dict).values())
	SumofNegdict = sum(Counter(neg_dict).values())

	sentiment_withWeight=CalArticle(article, pos_dict, neg_dict, SumofPosdict, SumofNegdict)
	# print(sentiment_withWeight)
	pos_weightprob, neg_weightprob = sentiment_withWeight[0], sentiment_withWeight[1]
	pos_snowprob, neg_snowprob = calSnownlp(article)

	pos_withdict, neg_withdict = calwithDict(article)
	# print(pos_weightprob, neg_weightprob)
	# print(pos_snowprob, neg_snowprob)
	final_pos = (pos_weightprob + pos_snowprob + pos_withdict) / 3
	final_neg = (neg_weightprob + neg_snowprob + neg_withdict) / 3
	print(final_pos, final_neg)
	print("======")
	if final_pos > final_neg:
		return 1, final_pos
	elif final_pos < final_neg:
		return 0, final_neg
	else:
		return 0.5, 0.5


def getTermDict(News):

	pos_path = "./NewsSite/modules/pos_json.txt"
	neg_path = "./NewsSite/modules/neg_json.txt"
	pos_dict = LoadDict(pos_path)
	neg_dict = LoadDict(neg_path)

	PosTermDict = {}
	NegTermDict = {}

	for _new in News:
		contents = _new.content.split("|||")
		# contents = _new.title.split()
		for line in contents:
			for term in jieba.cut(line):
				if term in pos_dict:
					if term not in PosTermDict:
						PosTermDict[term] = 0
					PosTermDict[term] += 1
				elif term in neg_dict:
					if term not in NegTermDict:
						NegTermDict[term] = 0
					NegTermDict[term] += 1
	# print(PosTermDict, NegTermDict)
	return PosTermDict, NegTermDict


def index(request):

	return render(request, 'NewsSite/index.html')

def crawl(request, forum):

	crawler = Crawler()
	debug=""
	daily_news_detailmeta = crawler.GetNews(forum, section='Gossiping', limit=20)
	print(len(daily_news_detailmeta))
	for single_new in daily_news_detailmeta:
		title=single_new['new_title']
		url=crawler.forum_domain[forum]+single_new['new_url']
		content=[line for line in single_new['new_content'].split('，') if len(line) > 3]
		timestamp=datetime.datetime.now().date()
		company=forum
		flag, posprob=calSentimentScore(content) 
		# debug += ("{}||{}||{}||{}||{}\n===============\n\n\n".format(title, url, content, company, posprob))
		print("Final PosProb:", posprob)
		new=News.objects.get_or_create(title=title, url=url, company=company, positiveprob=posprob, timestamp=timestamp, content="|||".join(content))
		if (new[1] == False):
			print("Exists!Dont Save")
			continue
		# print(new[0].content)
		new[0].save()
	return HttpResponse(debug)

def filter(request):

	if request.method != 'POST':
		return HttpResponse("You Shall not pass!")
	choose = 1
	try:
		startdate, enddate = datetime.datetime.strptime(request.POST['startdate'], "%Y-%m-%d"), datetime.datetime.strptime(request.POST['enddate'], "%Y-%m-%d")
		msg=""
	except:
		msg="給我選數字啊！"
		choose = 0
		return render(request,"NewsSite/index.html",locals())
		
	if enddate < startdate:
		msg = "別亂選啊！"
		choose = 0
		return render(request,"NewsSite/index.html",locals())

	keyword=request.POST['keyword']

	choosenNews = News.objects.filter(timestamp__gte=startdate).filter(timestamp__lte=enddate).filter(title__contains=keyword)
	print(choosenNews)
	plotchart=0
	if(len(choosenNews) > 0):
		plotchart=1

	curdate = startdate
	datelist = []
	while curdate < enddate:
		datelist.append(curdate.date())
		curdate += datetime.timedelta(days=1)
	datelist.append(curdate.date())
	

	d={}
	for _date in datelist:
		d[_date.__str__()] = len(choosenNews.filter(timestamp=datetime.datetime.strptime(_date.__str__(), "%Y-%m-%d")))
	# print(d)
	d=json.dumps(d)

	sentiment=[0, 0]
	random.seed(int(time.time()))
	for news in choosenNews:
		print(news.title, news.positiveprob)
		if news.positiveprob > 0.59:
			sentiment[0] += 1
		else:
			sentiment[1] += 1
	sentiment=json.dumps(sentiment)


	#### for top3 Pos/Neg article
	sortedNews = sorted(choosenNews, key=lambda x: x.positiveprob)
	try:
		PosTop3 = sortedNews[:3]
		NegTop3 = sortedNews[-3:]
	except:
		print("Not enough news to pick top3")
		PosTop3 = []
		NegTop3 = []
		for i in range(0, 3):
			try:
				PosTop3.append(sortedNews[i])
			except:
				break
		for i in range(-3, 0):
			try:
				NegTop3.append(sortedNews[i])
			except:
				break
	print("======")
	for p in PosTop3:
		print(p.title, p.positiveprob)
	for n in NegTop3:
		print(n.title, n.positiveprob)
	print("======")
	####


	#### for the sentiment word
	PosTermDict, NegTermDict = getTermDict(choosenNews)
	posD = {}
	negD = {}
	stopwords = ['。', '，', '「', '」', '？', '的', '我', '你', '他', '？', '-', '、', ' ', '', ":", '/', ')', '>']
	# print(PosTermDict, NegTermDict)
	sortedPos = sorted(PosTermDict, key=lambda x: PosTermDict[x], reverse=True)
	sortedNeg = sorted(NegTermDict, key=lambda x: NegTermDict[x], reverse=True)
	multiK = 25
	maxPos = PosTermDict[sortedPos[0]]
	maxNeg = NegTermDict[sortedNeg[0]]
	print("This is Max:{}, {}".format(maxPos, maxNeg))
	for tmp in range(0, min(len(sortedPos), 500)):
		term = sortedPos[tmp]
		if term in stopwords:
			continue
		posD[term] = ((PosTermDict[term] - 1) / (maxPos - 1) ) * multiK
		# posD[term] = PosTermDict[term] * multiK
		# print(term, posD[term])
	for tmp in range(0, min(len(sortedNeg), 500)):
		term = sortedNeg[tmp]
		if term in stopwords:
			continue
		negD[term] = ((NegTermDict[term] - 1 ) / (maxNeg - 1)) * multiK
		# negD[term] = NegTermDict[term] * multiK
		# print(term, negD[term])
	PosTermDict = json.dumps(posD)
	NegTermDict = json.dumps(negD)

	####

	return render(request,"NewsSite/index.html",locals())


# Create your views here.
