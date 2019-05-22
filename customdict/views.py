#coding:utf-8
from django.shortcuts import render,redirect   # 加入 redirect 套件
from django.contrib.auth import authenticate
from django.contrib import auth
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import UserDictSet, PersonalDict, UserDictFile
import codecs

def customdict(request):
	if request.user.is_authenticated:
		name = request.user.username
		uu = User.objects.get(username=name)
	if request.method == 'POST':
		
		try:
			PersonaldictRaw = request.POST.get('dictbox', False)
			Personaldict = PersonaldictRaw.split(',')
			for pd in Personaldict:
				pd = pd.strip()
				if PersonalDict.objects.filter(DictName=pd, user=uu).exists():
					continue
				tmppd = PersonalDict(DictName=pd, user=uu)
				tmppd.save()
		except:
			# print('wrong1')
			pass

		try:
			title = request.POST['title']
			upfile = request.FILES['upload_file']
			print(upfile.charset)
			if UserDictFile.objects.filter(title=title).exists():
				FileUploadMsg = '同名的檔案存在！'
			else:
				uploadfile = UserDictFile(title=title, file=upfile, user=uu)
				uploadfile.save()
		except:
			print('wrong2')
			pass
		
		return render(request, 'customdict/dictpage.html', locals())

	return render(request, 'customdict/dictpage.html', locals())


@login_required(login_url='/loginapp/login')
def editdict(request):
	uu = User.objects.get(username=request.user.username)
	
	if request.method == 'POST':
		filterstr = request.POST.get('filterstr')
		try:
			pds = uu.pds.filter(DictName__contains=filterstr)
		except:
			pass
	else:
		pds = uu.pds.all()

	limit = 5
	paginator = Paginator(pds, limit)
	page = request.GET.get('page','1')
	result = paginator.page(page)

	return render(request, 'customdict/editdict.html', {'pds':result})

@login_required(login_url='/loginapp/login')
def edit(request, idx):
	if request.method != 'POST':
		return redirect('/customdictpage')
	pd = PersonalDict.objects.get(pk=idx)
	updatepd = request.POST.get('editdictionary')
	if PersonalDict.objects.filter(DictName=updatepd).exists():
		return redirect('/customdictpage/editdict')
	pd.DictName = updatepd
	pd.save()
	return redirect('/customdictpage/editdict')


@login_required(login_url='/loginapp/login')
def delete(request, idx):
	pd = PersonalDict.objects.get(pk=idx)
	pd.delete()
	return redirect('/customdictpage/editdict')


@login_required(login_url='/loginapp/login')
def build(request):

	return render(request, 'customdict/build.html')

@login_required(login_url='/loginapp/login')
def showdictfile(request, idx):
	f = UserDictFile.objects.get(pk=idx)
	f.file.open()
	content = f.file.read().decode('utf-8')
	content = content.split('\n')
	content = [x.strip('\r') for x in content ]

	return	render(request, 'blank.html', locals())

@login_required(login_url='/loginapp/login')
def deletedictfile(request, idx):
	f = UserDictFile.objects.get(pk=idx)
	f.delete()

	return redirect('/customdictpage/buildset')










