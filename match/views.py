from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import *
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from datetime import date
from django.http import JsonResponse
import json
# Create your views here.

@login_required
def HomeView(request):
    profile = Profile.objects.get(user=request.user)
    profile.age = (date.today() - profile.dob).days//365
    profile.save()
    interests = Interest.objects.filter(profile=profile)
    context = {
        'profile': profile,
        'interests': interests,
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
                              dob=data2['dob'], gender=data2['gender'],
                              age=(date.today() - date(data2['dob'])).days//365)
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
    if request.method == "POST":
        for choice in request.POST:
            interest = Interest(profile=profile,interest=choice)
            interest.save()
        return HttpResponseRedirect(reverse('HomeView'))
    choices = [ c[1] for c in Interest.interest.field.choices]
    context = {
        'profile': profile,
        'choices': choices,
    }
    return render(request, 'match/addInterests.html', context)

def EditInterestsView(request):
    profile = Profile.objects.get(user=request.user)
    interests = Interest.objects.filter(profile=profile)
    if request.method == 'POST':
        interests.delete()
        for choice in request.POST:
            interest = Interest(profile=profile,interest=choice)
            interest.save()
        return HttpResponseRedirect(reverse('HomeView'))

    interestsList = [i.interest for i in interests]
    print(interestsList)
    choices = [ c[1] for c in Interest.interest.field.choices]
    print(choices)
    context = {
        'profile': profile,
        'choices': choices,
        'interests': interestsList,
    }
    return render(request, 'match/addInterests.html', context)

def ProfileSearchView(request):
    """
    The idea here is that you look at every profile in the platform.
    You can then "like"/"unlike" people while looking at all of their info.
    You will have a list of people that you like, and list you unlike, and filter your search so
        you can see only people you like, unlike, or have not seen yet.
    There is an option to show only people who like you.
    """
    uprofile = Profile.objects.get(user=request.user)
    profiles = Profile.objects.all()
    relationships = Relationship.objects.filter(profileUser=uprofile)
    likes = [ r.profileOther.user.username for r in relationships.filter(relationship="like")]
    unlikes = [ r.profileOther.user.username for r in relationships.filter(relationship="unlike")]

    for profile in profiles:
        profile.age = (date.today() - profile.dob).days//365
        profile.save()

    if request.method == "POST":
        try: #In this case, the user is trying to like/unlike someone
            profileOther = Profile.objects.get(user__username=request.POST['username'])
            if request.POST['relationship'] == 'delete':
                relationship = Relationship.objects.get(profileOther=profileOther)
                relationship.delete()
            else:
                relationship = Relationship(profileUser=uprofile, profileOther=profileOther,
                                            relationship=request.POST['relationship'])
                relationship.save()
            return JsonResponse({'profileUser': relationship.profileUser, 'profileOther': relationship.profileOther,
                                'relationship': relationship.relationship})
        except: #In this case, the user is trying to search/filter their list
            """
            Let's say i have a profileUser already. And I want to get all relationships that associate with the profile:
                relationships = Relationship.objects.filter(profileUser=profileUser)
            Now we want to get all of the relationships in that QuerySet such that "relationship = 'like'"
                relationships = relationships.filter(relationship='like')
            Now we want to get all of the "profileOther" objects from the remaining relationships
                relationships.profileOther
            But now how do we combine the profiles that we filtered from the search: profiles, with the profiles that we-
            -just got from relationships.profileOther?
                profiles = relationships.profileOther & profiles  
            """
            form = request.POST
            if form['search'] != "": 
                profiles = profiles.filter(user__username__icontains=form['search'])
            #In this case, either they are not searcing for a profile, or they are not, so we will filter further
                crelationships = Relationship.objects.filter(profileUser=uprofile)
            match form['filter']:
                case "all": pass
                case 'likes': 
                    crelationships = crelationships.filter(relationship='like')
                case 'unlikes':
                    crelationships = crelationships.filter(relationship='not like')
                case 'unseen':
                    """
                    I have all relationships that currently are associated with 'profileUser'. Now how do I find all-
                    -profiles that are not "related" to profileUser?
                        profiles = [profile for profile in allProfiles: if not profile in crelationships.profileOther: return profile]
                    """
                    #oprofiles = [profile for profile in allProfiles: if not profile in crelationships.profileOther: return profile]
            profiles = crelationships.profileOther & profiles

    context = {
        'uprofile': uprofile,
        'profiles': profiles,
        'relationships': relationships,
        'likes': likes,
        'unlikes': unlikes,
    }

    return render(request, 'match/profileSearch.html', context)