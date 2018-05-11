from django.shortcuts import render, redirect
from .models import user, notes
from django.http import HttpResponse
from datetime import date
# Create your views here.mplat

def loginRequired(methodName):
	def wrapper(*args,**keywords):
		request = args[0]
		if 'username_key' in request.session:
			return methodName(*args,**keywords)
		else:
			return redirect(loginUserView)
	return wrapper

def registerUserView(request):
	if request.method == 'GET':
		return render(request,'register.html')
	elif request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		email = request.POST['email']
		u = user.registerUser(username,email,password)
		if isinstance(u,user):
			message = '{0} registered'.format(username)
			return redirect(loginUserView)

		elif u == -1:
			message = '{0} already exists'.format(username)
		else:
			message = 'Unexpected error occured'
		return HttpResponse(message)



def loginUserView(request):
	if request.method == 'GET':
		return render(request,'login.html')
	elif request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		u = user.loginUser(username,password)
		if isinstance(u,user):
			#request.session['username_key'] = u.username
			request.session['username_key'] = username
			return redirect(submitnotesView)
			#want to send username
			#return render(request, 'index.html',{'message':message})
		elif u == -1:
			message = 'Username or password is invalid'
		else:
			message = 'Unexpected error occured'
		return HttpResponse(message)
		
@loginRequired
def submitnotesView(request):
	if request.method == 'GET':
		username = request.session['username_key']
		all_notes = notes.objects.filter(username1=username)
		message = 'Welcome ' + username
		return render(request,'index.html',{'notes': all_notes,'message': message})
	elif request.method == 'POST':
		username = request.session['username_key']
		title = request.POST['title']
		content = request.POST['content']
		date_of_creation = str(date.today())
		u = notes.registerNotes(username,title,content,date_of_creation)
		if isinstance(u,notes):
			return redirect(submitnotesView)
		else:
			message = 'Unexpected error occured'
		return HttpResponse(message)

def addnotesView(request):
	if request.method == 'GET':
		username = request.session['username_key']
		return render(request,'add_note.html')
	elif request.method == 'POST':
		return render(request,'add_note.html')


def updatenotesView(request):
	if request.method == 'POST':
		id1 = request.POST['update']
		u = notes.objects.filter(id=id1)
		obj = u[0]
		return render(request,'add_note.html',{'obj':obj})
	elif request.method == 'GET':
		return redirect(updatenotesView)


def updateView(request):
	if request.method == 'POST':
		id1 = request.POST['update']
		title = request.POST['title']
		content = request.POST['content']
		date_of_creation = str(date.today())			
		i = notes.updateNotes(id1,title,content,date_of_creation)
		if i==1:
			return redirect(submitnotesView)
		else:
			message = 'Unexpected error occured '+id1
		return HttpResponse(message)

	elif request.method == 'GET':
		return redirect(updateView)	
		
		

def deleteNote(request):
	if request.method == 'POST':
		id1 = request.POST['delete']
		notes.objects.filter(id=id1).delete()
		return redirect(submitnotesView)

def logout(request):
	if request.method == 'POST':
		del request.session['username_key']
		return redirect(loginUserView)
'''def sharenotesView(request):
	if request.method == 'POST':
		username = request.POST['username']
		note_id = request.POST['note_id']
		u = shared_notes.share_note(note_id,username)

		if isinstance(u,shared_notes):
			message = 'Notes shared Successfully'
		else:
			message = 'Unexpected error occured'
		return HttpResponse(message)'''

