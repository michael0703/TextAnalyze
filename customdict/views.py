from django.shortcuts import render,redirect   # 加入 redirect 套件
from django.contrib.auth import authenticate
from django.contrib import auth
from django.http import HttpResponse
from django.contrib.auth.models import User
from loginapp.models import PersonalDict

def customdict(request):
	if request.user.is_authenticated:
		name = request.user.username
		uu = User.objects.get(username=name)
	if request.method == 'POST':
		
		try:
			PersonaldictRaw = request.POST.get('dictbox', False)
			Personaldict = PersonaldictRaw.split(',')
			for pd in Personaldict:
				tmppd = PersonalDict(DictName=pd, user=uu)
				tmppd.save()
		except:
			print('wrong1')

		try:
			uploadfile = request.FILES['upload_file']
			# print(uploadfile.name)
			messages = uploadfile.read()
			
			msgs = messages.decode('UTF-8').split('\n')
			for msg in msgs:
				tmppd = PersonalDict(DictName=msg, user=uu)
				tmppd.save()
			# print(messages)
		except:
			messages = ''
			print('wrong2')
		
		return render(request, 'dictpage.html', locals())

	return render(request, 'dictpage.html', locals())