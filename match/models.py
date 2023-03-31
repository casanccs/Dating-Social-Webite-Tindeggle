from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.forms import *
from django.forms import ModelForm
from django.forms import TextInput, Textarea, DateInput

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.CharField(max_length=500, blank=True)
    ppic1 = models.ImageField()
    ppic2 = models.ImageField(blank=True)
    ppic3 = models.ImageField(blank=True)
    ppic4 = models.ImageField(blank=True)
    ppic5 = models.ImageField(blank=True)
    ppic6 = models.ImageField(blank=True)
    dob = models.DateField(help_text="   Type exactly like: 'YYYY-MM-DD'")
    gender = models.CharField(choices=[('M', 'Male'), ('F','Female'), ('O', 'Other')], max_length=1)
    age = models.IntegerField(default=0)
    count = models.IntegerField(blank=True, default=0) #This field is not used for a "typical" usage

    def __str__(self):
        return self.user.username


class Interest(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    choices = [
        ('Anime', 'Anime'),
        ('K-Pop', 'K-Pop'),
        ('K-Shows', 'K-Shows'),
        ('Webtoon', 'Webtoon'),
        ('American Shows', 'American Shows'),
        ('Movies', 'Movies'),
        ('Food', 'Food'),
        ('Yoga', 'Yoga'),
        ('Working Out', 'Working Out'),
        ('Fighting', 'Fighting'),
        ('Cars', 'Cars'),
        ('Business', 'Business'),
        ('Stocks', 'Stocks'),
        ('School', 'School'),
        ('Relationship', 'Relationship'),
        ('Deep Talks', 'Deep Talks'),
        ('Controversial Subjects', 'Controversial Subjects'),
        ('Video Games', 'Video Games'),
        ('Sports', 'Sports')
    ]
    interest = models.CharField(choices=choices, blank=True, max_length=100)
    
    def __str__(self):
        return f"{self.profile.user.username}: {self.interest}"
    
class ChatRoom(models.Model):
    room_name = models.CharField(max_length=100, primary_key=True)

    def __str__(self):
        return self.room_name

class Participant(models.Model):
    chatRoom = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

class Message(models.Model):
    content = models.CharField(max_length=300, blank=True)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE,default=None)
    chatRoom = models.ForeignKey(ChatRoom, on_delete=models.CASCADE,default=None)
    time = models.DateTimeField(auto_now_add=True)


class Relationship(models.Model):
    profileUser = models.ForeignKey(Profile, related_name="profileUser", on_delete=models.CASCADE)
    profileOther = models.ForeignKey(Profile, related_name="profileOther", on_delete=models.CASCADE)
    choices = [
        ("like", "like"),
        ("not like", "not like"),
    ]
    relationship = models.CharField(blank=True, max_length=30, choices=choices)

    def __str__(self):
        if self.relationship == "like":
            return f"{self.profileUser.user.username} <3 => {self.profileOther.user.username}"
        else:
            return f"{self.profileUser.user.username} X => {self.profileOther.user.username}"




###############################################

class ProfileCreationForm1(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'email', 'first_name', 'last_name']

class ProfileCreationForm2(ModelForm):
    class Meta:
        model = Profile
        fields = ['dob', 'gender', 'bio']
        labels = {
            'dob': 'Date of Birth',
        }
        widgets = {
            'bio': Textarea(attrs={'placeholder': 'Tell Everyone About Yourself.'}),
            'dob': DateInput()
        }

class ProfileCreationForm3(ModelForm):
    class Meta:
        model = Profile
        fields = ['ppic1', 'ppic2', 'ppic3', 'ppic4', 'ppic5', 'ppic6']
        labels = {
            'ppic1': 'Choose Up To 5 Photos',
            'ppic2': '',
            'ppic3': '',
            'ppic4': '',
            'ppic5': '',
            'ppic6': '',
        }