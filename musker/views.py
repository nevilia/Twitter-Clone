from django.shortcuts import redirect, render
from django.contrib import messages
from .models import Profile, Meep
from .forms import MeepForm

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