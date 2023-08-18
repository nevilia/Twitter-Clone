from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

# Create a USer Profile Model.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    follows = models.ManyToManyField("self",
                                     related_name="followed_by",
                                     symmetrical=False, #I can follow you, you dont have to follow me, vise versa
                                     blank=True)
    
    date_modified = models.DateTimeField(User, auto_now=True)
    
    def __str__(self):
        return self.user.username


# automatically create profile when a new user signs up
def create_profile(sender, instance, created, **kwargs):
    if created: # if user is already created. Djnago handles it
        user_profile = Profile(user=instance)
        user_profile.save() # saves the profile first
        # user follows himself as soon as profile is created
        user_profile.follows.set([instance.profile.id]) # instance is the current one. django automatically gives us id. we access the "profile" id
        user_profile.save() # saves who to follow
        
        
post_save.connect(create_profile, sender=User)