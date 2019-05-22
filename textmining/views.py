from django.shortcuts import render,redirect   # 加入 redirect 套件
from django.http import HttpResponse
from .modules.SentencePreProcess import SentenceAnalyze

def textmine(request):

	# return HttpResponse('This is textminig main page!')
	articles_seg = []
	if request.method == 'POST':
		articles = request.POST.get('article')
		
		SA = SentenceAnalyze()
		articles_seg = SA.TextCut([articles])
		print(articles_seg)
		return render(request, 'textmine/miningindex.html', locals())


	return render(request, 'textmine/miningindex.html')