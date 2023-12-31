from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

# Create a post: meep model
class Meep(models.Model):
    user = models.ForeignKey(
        User, related_name="meeps", on_delete=models.DO_NOTHING
    )
    body = models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name="meep_like", blank=True)
    
    
    # Keep count of likes
    def number_of_likes(self):
        return self.likes.count()
        
    def __str__(self):
        return(f"{self.user}"
               f"({self.created_at:%Y-%m-%d %H:%M}): "
               f"{self.body}"
               )

# Create a USer Profile Model.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    follows = models.ManyToManyField("self",
                                     related_name="followed_by",
                                     symmetrical=False, #I can follow you, you dont have to follow me, vise versa
                                     blank=True)
    
    date_modified = models.DateTimeField(User, auto_now=True)
    profile_image = models.ImageField(null=True, blank=True, upload_to="images/")
    
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