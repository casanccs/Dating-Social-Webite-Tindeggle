from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import *
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required
def HomeView(request):
    profile = Profile.objects.get(user=request.user)
    context = {
        'profile': profile,
    }
    return render(request, 'match/home.html', context)

def CreateProfileView(request):
    if request.method == 'POST':
        form1 = ProfileCreationForm1(request.POST)
        form2 = ProfileCreationForm2(request.POST)
        form3 = ProfileCreationForm3(request.FILES)
        n = len(request.FILES)
        if form1.is_valid() and form2.is_valid():
            data1 = form1.cleaned_data
            data2 = form2.cleaned_data
            data3 = request.FILES
            user = User.objects.create_user(data1['username'], data1['email'], data1['password1'])
            user.first_name = data1['first_name']
            user.last_name = data1['last_name']
            user.save()
            profile = Profile(user=user, bio=data2['bio'], 
                              dob=data2['dob'], gender=data2['gender'])
            profile.ppic1 = data3['ppic1']
            if n>1:
                profile.ppic2 = data3['ppic2']
                if n>2:
                    profile.ppic3 = data3['ppic3']
                    if n>3:
                        profile.ppic4 = data3['ppic4']
                        if n>4:
                            profile.ppic5 = data3['ppic5']
                            if n>5:
                                profile.ppic5 = data3['ppic6']
            profile.save()
            login(request, user)
            return HttpResponseRedirect(reverse('addInterests'))
        else:
            context = {
                'form1': form1,
                'form2': form2,
                'form3': form3,
            }
            return render(request, 'match/createProfile.html', context)
    else:
        form1 = ProfileCreationForm1()
        form2 = ProfileCreationForm2()
        form3 = ProfileCreationForm3()
        context = {
            'form1': form1,
            'form2': form2,
            'form3': form3,
        }
    return render(request, 'match/createProfile.html', context)

def AddInterestsView(request):
    profile = Profile.objects.get(user=request.user)
    choices = [ c[1] for c in Interest.interest.field.choices ]
    context = {
        'profile': profile,
        'choices': choices,
    }
    return render(request, 'match/addInterests.html', context)