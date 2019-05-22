from django.shortcuts import render,redirect   # 加入 redirect 套件
from django.contrib.auth import authenticate
from django.contrib import auth
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from uploadArticle.models import UserArticleFile
import json
from .modules import tfidf as myfunction
import pandas as pd

# Create your views here.
@login_required(login_url='/loginapp/login')
def index(request):

	return render(request, 'tfidfanalyze/index.html')

@login_required(login_url='/loginapp/login')
def tfidf(request):

	article_num = request.POST.get('countvar')
	

	article_list = []
	for i in range(1, int(article_num)+1):
		val = request.POST.get(str(i))
		if val == None:
			continue
		tmp = UserArticleFile.objects.get(pk=val)
		if(tmp not in article_list):
			article_list.append(tmp)
	

	df = None
	for f in article_list:
		if f.hascache:
			TmpWordMatrix = json.loads(f.cache)
			df = myfunction.ConcatWordMatrix(TmpWordMatrix, df)
	df = df.fillna(0)
	
	article_name = json.dumps([f.title for f in article_list])
	df_tfidf = myfunction.DoTFIDF(df, [f.title for f in article_list])
	
	
	# df_tfidf_dict = df_tfidf.to_dict()
	
	PCA = myfunction.DoPCA(df_tfidf.T)
	print(PCA)
	PCA_List = json.dumps(PCA.tolist())
	# return render(request, 'tfidfanalyze/showtfidf.html', locals())
	# return HttpResponse(df_tfidf[df_tfidf>0.007].dropna(axis=1).T.to_html())
	return render(request, 'tfidfanalyze/xytest.html', locals())



