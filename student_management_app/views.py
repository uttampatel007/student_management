from django.shortcuts import render
from django.http import HttpResponseRedirect,HttpResponse
from student_management_app.EmailBackEnd import EmailBackEnd
from django.contrib.auth import login,logout



# Create your views here.


def showDemoPage(request):
	return render(request,"index.html")
	
def showLoginPage(request):
	return render(request,"login.html")

def doLogin(request):
	if request.method!="POST":
		return HttpResponse("<h2>Method Not Allowed</h2>")
	else:
		print(request.POST.get("email"))
		user=EmailBackEnd.authenticate(request, username=request.POST.get("email"),password=request.POST.get("password"))
		if user!=None:
			login(request,user)
			return HttpResponse("Email : "+request.POST.get("email")+"Password : "+request.POST.get("password"))
		else:
			return HttpResponse("Invalid Login")

def GetUserDetails(request):
	if request.user!=None:
		return HttpResponse("user : "+request.user.email+"usertype : "+request.user.user_type)
	else:
		return HttpResponse("Please Log In")

def logout_user(request):
	logout(request)
	return HttpResponseRedirect("/")