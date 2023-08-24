from django.shortcuts import redirect, render
from django.contrib import messages
from .models import Profile, Meep
from .forms import MeepForm, SignUpForm

from django.contrib.auth import authenticate,login, logout
from django.contrib.auth.forms import UserCreationForm
from django import forms
# Create your views here.
def home(request):
    if request.user.is_authenticated:
        form = MeepForm(request.POST or None)
        if request.method == "POST":
            if form.is_valid():
                meep = form.save(commit=False) # dont save yet
                meep.user = request.user # save for specific user only
                meep.save() # save finally
                messages.success(request, ("Your Meep has been Posted!"))

                return redirect('home')
        
        
        meeps = Meep.objects.all().order_by("-created_at")
        return render(request, 'home.html', {"meeps":meeps, "form":form})
    else:
        meeps = Meep.objects.all().order_by("-created_at")
        return render(request, 'home.html', {"meeps":meeps})

def profile_list(request):
    if request.user.is_authenticated:
        profiles = Profile.objects.exclude(user=request.user) # exclusing the current logged in user
        return render(request, 'profile_list.html', {"profiles" : profiles})
    else:
        messages.success(request, ("You Must Be Logged In!"))
        return redirect('home')
    
def profile(request, pk):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user_id=pk)
        meeps = Meep.objects.filter(user_id=pk).order_by("-created_at")
        
        
        # Post form logic
        if request.method == "POST":
            # get current user id
            current_user_profile = request.user.profile
            # get form data
            action = request.POST['follow']
            # decide to follow or unfollow
            if action=="unfollow":
                current_user_profile.follows.remove(profile)
            elif action=="follow":
                current_user_profile.follows.add(profile)
            # save profile
            current_user_profile.save()
            
            # See all the user's meeps
                
        return render(request, "profile.html", {"profile":profile, "meeps":meeps})
    else:
        messages.success(request, ("You Must Be Logged In!"))
        return redirect('home')
    
def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, ("Welcome Back!"))
            return redirect('home')
        else:
            messages.success(request, ("There was an error logging you in."))
            return redirect('login')
    else:
        return render(request, "login.html", {})
    
    
def logout_user(request):
    logout(request)
    messages.success(request, "You have been Logged Out.")
    return redirect("home")

def register_user(request):
	form = SignUpForm()
	if request.method == "POST":
		form = SignUpForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data['username']
			password = form.cleaned_data['password1']
			# first_name = form.cleaned_data['first_name']
			# second_name = form.cleaned_data['second_name']
			# email = form.cleaned_data['email']
			# Log in user only need username and password1
			user = authenticate(username=username, password=password)
			login(request,user)
			messages.success(request, ("You have successfully registered! Welcome!"))
			return redirect('home')
	
	return render(request, "register.html", {'form':form})