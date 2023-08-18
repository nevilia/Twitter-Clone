from django.contrib import admin
from django.contrib.auth.models import Group, User
from .models import Profile
# Register your models here.

# Removing Group model
admin.site.unregister(Group)

# Mix Profile info into User info
class ProfileInline(admin.StackedInline):
    model = Profile

# Extend User
class UserAdmin(admin.ModelAdmin):
    model = User
    fields = ["username"]
    inlines = [ProfileInline]
    
# Only keeping the username field and deleting everything else
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
# admin.site.register(Profile)


