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
from snownlp import SnowNLP
import datetime
import random 
import time


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
		# content=single_new['new_content']
		timestamp=datetime.datetime.now().date()
		company=forum
		posprob=SnowNLP(title).sentiments
		# debug += ("{}||{}||{}||{}||{}\n===============\n\n\n".format(title, url, content, company, posprob))
		new=News.objects.get_or_create(title=title, url=url, company=company, positiveprob=posprob, timestamp=timestamp)
		if (new[1] == False):
			print("Exists!Dont Save")
			continue
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
		if random.random() < news.positiveprob :
			sentiment[0] += 1
		else:
			sentiment[1] += 1
	sentiment=json.dumps(sentiment)


	return render(request,"NewsSite/index.html",locals())


# Create your views here.
