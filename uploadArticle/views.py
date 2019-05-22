
from django.shortcuts import render,redirect   # 加入 redirect 套件
from django.contrib.auth import authenticate
from django.contrib import auth
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import UserArticleFile, UserImageFile
from .modules import ArticleSeg
from .modules import ImgProc
import json
from customdict.models import UserDictFile
import cv2
import numpy as np


from keras.models import load_model

my_model = load_model('./uploadArticle/modules/my_25800model.h5')
my_model.predict(np.zeros((2, 25,800,1)))
# Create your views here.


@login_required(login_url='/loginapp/login')
def index(request):
	if request.method == 'POST':
		name = request.user.username
		uu = User.objects.get(username=name)
		try:
			title = request.POST['title']
			upfile = request.FILES['upload_file']
			print(upfile.name)
			if UserArticleFile.objects.filter(title=title).exists():
				FileUploadMsg = '同名的檔案存在！'
			else:
				uploadfile = UserArticleFile(title=title, file=upfile, user=uu)
				upfile.open()

				rawpage = upfile.read().decode('utf-8')

				#for PDF upload debug
				print(rawpage)
				
				rawpage = rawpage.split('\n')
				report = []
				reports = []
				for line in rawpage:
					report.append(line.strip('\r'))
				reports.append(report)

				clean_reports = []
				# first clean the article
				clean_reports = ArticleSeg.ArticleSeg(reports)

				deletef = UserDictFile.objects.get(pk=18)	#18 is the Deleteword.txt
				deletef.file.open()
				content = deletef.file.read().decode('utf-8')
				content = content.split('\n')
				content = [x.strip('\r') for x in content ]


				WordMatrix = {}
				# then make the word matrix
				for clean_report in clean_reports:
					ArticleSeg.MakeWordMatrix(clean_report, WordMatrix)
				for key in WordMatrix.copy():
					if key in content:
						WordMatrix.pop(key)

				WordMatrixStr = json.dumps(WordMatrix)
				uploadfile.hascache = True
				uploadfile.cache = WordMatrixStr
				uploadfile.save()

		except:
			print('Nothing Upload')
			pass
	return render(request, 'upart/index.html')

@login_required(login_url='/loginapp/login')
def admin(request):

	uu = User.objects.get(username=request.user.username)
	arts = uu.ArticleFile.all()


	limit = 7
	paginator = Paginator(arts, limit)
	page = request.GET.get('page','1')
	result = paginator.page(page)

	return render(request, 'upart/admin.html', {'arts':result})


@login_required(login_url='/loginapp/login')
def deletearticle(request, idx):

	art = UserArticleFile.objects.get(pk=idx)
	art.delete()

	return redirect('/uploadArticles/adminarticles')

def showarticle(request, idx):

	f = UserArticleFile.objects.get(pk=idx)
	f.file.open()
	content = f.file.read().decode('utf-8')
	content = content.split('\n')
	content = [x.strip('\r') for x in content ]

	return	render(request, 'blank.html', locals())

def preprocindex(request):

	uu = User.objects.get(username=request.user.username)
	arts = uu.ArticleFile.all()


	limit = 7
	paginator = Paginator(arts, limit)
	page = request.GET.get('page','1')
	result = paginator.page(page)
	
	return render(request, 'upart/preprocindex.html', {'arts':result})	


def procarticle(request, idx):

	try:
		deletefname = request.POST.get('selectbar')
		deletef = UserDictFile.objects.get(pk=int(deletefname))
		deletef.file.open()
		content = deletef.file.read().decode('utf-8')
		content = content.split('\n')
		content = [x.strip('\r') for x in content ]
		print(deletefname, deletef)
	except:
		content = []
		pass


	f = UserArticleFile.objects.get(pk=idx)

	f.file.open()

	reports = []
	rawpage = f.file.read().decode('utf-8')
	rawpage = rawpage.split('\n')
	report = []
	for line in rawpage:
		report.append(line.strip('\r'))
	reports.append(report)

	clean_reports = []
	# first clean the article
	clean_reports = ArticleSeg.ArticleSeg(reports)

	WordMatrix = {}
	# then make the word matrix
	for clean_report in clean_reports:
		ArticleSeg.MakeWordMatrix(clean_report, WordMatrix)

	# delete the deleteworld
	for key in WordMatrix.copy():
		if key in content:
			WordMatrix.pop(key)
			# print(key)

	# Do the NER

	# NerService = ArticleSeg.NerService()
	# NerService.Assign(reports)
	# NerService.NerAnalyze()
	# NerService.MakeNerDict()

	# NerDict = NerService.NerDict


	### Need to store the cache
	WordMatrixStr = json.dumps(WordMatrix)
	# NerDictStr = json.dumps(NerDict)
	f.hascache = True
	f.cache = WordMatrixStr
	# f.NerField = NerDictStr
	f.save()
	# print(NerDictStr)

	return	redirect('/uploadArticles/preprocarticleindex')

def showpreprocresult(request, idx):

	f = UserArticleFile.objects.get(pk=idx)
	WordMatrix = json.loads(f.cache)
	# NerField = json.loads(f.NerField)
	# print(NerField)
	# dd = json.dumps(WordMatrix)
	return render(request, 'upart/showpreprocresult.html', locals()) 


def uploadimage(request):

	# if not upload img simply show the page
	if request.method != 'POST':
		return render(request, 'upart/uploadimageindex.html')

	name = request.user.username
	uu = User.objects.get(username=name)

	try:
		
		upimg = request.FILES.getlist('upload_img')
		
		for img in upimg:
			title = img.name
			if UserImageFile.objects.filter(title=title).exists():
				print("Same file name exists")
			else:
				img = UserImageFile(title=title, user=uu, img=img)
				img.save()

		return render(request, 'upart/uploadimageindex.html')
	except:
		print("Something Broke")
		return render(request, 'upart/uploadimageindex.html')

@login_required(login_url='/loginapp/login')
def imgadmin(request):

	uu = User.objects.get(username=request.user.username)
	imgs = uu.ImgFile.all()


	# imgs_src = []
	# for img in imgs:
	# 	img_path = img.img.url.replace("/upfile", "./UserDir")
	# 	src = cv2.imread(img_path)
	# 	imgs_src.append(src)
	# ImgProcessor = ImgProc.ImgProcessor('./uploadArticle/modules/my_model.h5')

	# ImgProcessor.PreProcessImg(imgs_src)

	# y_pred = ImgProcessor.GetResult()
	# print(y_pred)
	

	return render(request, 'upart/uploadimgadmin.html', {'imgs':imgs})


@login_required(login_url='/loginapp/login')
def deleteimg(request, idx):

	img = UserImageFile.objects.get(pk=idx)
	img.delete()

	return redirect("/uploadArticles/uploadimage/admin")

@login_required(login_url='/loginapp/login')
def procimg(request):

	if request.method != 'POST':
		return redirect("/uploadArticles/uploadimage/admin")
	
	name = request.user.username
	uu = User.objects.get(username=name)

	startID = request.POST['startID']
	endID = request.POST['endID']

	startID = int(startID)
	endID = int(endID)

	imgs_src = []

	for i in range(startID, endID+1):
		db_img = uu.ImgFile.get(pk=i)
		img_path = db_img.img.url.replace("/upfile", "./UserDir")
		src = cv2.imread(img_path)
		imgs_src.append(src)


	global my_model
	ImgProcessor = ImgProc.ImgProcessor(my_model)

	ImgProcessor.PreProcessImg(imgs_src)

	y_pred = ImgProcessor.GetResult()
	class1_count = 0
	class2_count = 0
	class3_count = 0

	for row in y_pred:
		if np.isnan(np.sum(row)):
			continue
		if np.argmax(row) == 0:
			class1_count += 1
		elif np.argmax(row) == 1:
			class2_count += 1
		elif np.argmax(row) == 2:
			class3_count += 1

	print(class1_count, class2_count, class3_count)

	return render(request, "upart/imgprocresult.html", locals())
	# return redirect("/uploadArticles/uploadimage/admin")


















