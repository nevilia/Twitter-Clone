from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages
from .models import Profile, Meep
from .forms import MeepForm, SignUpForm, ProfilePicForm

from django.contrib.auth import authenticate,login, logout
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User

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

def update_user(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        profile_user = Profile.objects.get(user_id=request.user.id)
        
        user_form = SignUpForm(request.POST or None, request.FILES or None, instance=current_user) # Take all of current users info and pass in the form
        profile_form = ProfilePicForm(request.POST or None, request.FILES or None, instance=profile_user)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            login(request, current_user)
            messages.success(request, ('Your Profile has been updated')) # Might come up with an error "username already exists". this was made for Django 4.1.4 and won't fall into this error
            return redirect('home')

        return render(request, "update_user.html", {'user_form':user_form, 'profile_form':profile_form})
    else:
        messages.success(request, ('You Must be Logged In'))
        return redirect('home')
    
    
def meep_like(request, pk):
    if request.user.is_authenticated:
        meep = get_object_or_404(Meep, id=pk)
        if meep.likes.filter(id = request.user.id):
                # if a user has already liked it and clicks again, it must mean unlike rather than simply incrementing the count
            meep.likes.remove(request.user)
        else:
            meep.likes.add(request.user)
        # this is essentially redirecting us to the current page. we can access what page we are on as following
        return redirect(request.META.get("HTTP_REFERER"))
    else:
        messages.success(request, ("You must be logged in!"))
        return redirect('home')
    
def meep_share(request, pk):
    meep = get_object_or_404(Meep, id=pk)
    if meep:
        return render(request, "share_meep.html", {'meep':meep})
        
    else:
        messages.success(request, ("That Meep doesn't exist"))
        return redirect('home')