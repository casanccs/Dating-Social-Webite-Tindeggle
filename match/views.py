from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import *
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from datetime import date
from django.http import JsonResponse
import json
from django.core.paginator import Paginator
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

def ProfileView(request, username):
    uprofile = Profile.objects.get(user=request.user)
    profile = Profile.objects.get(user__username=username)
    profile.age = (date.today() - profile.dob).days//365
    profile.save()
    interests = Interest.objects.filter(profile=profile)

    relationship12 = Relationship.objects.filter(profileUser=uprofile).filter(profileOther=profile)
    relationship21 = Relationship.objects.filter(profileUser=profile).filter(profileOther=uprofile)
    toChat = False
    if relationship12 and relationship21:
        toChat = True
    context = {
        'profile': profile,
        'interests': interests,
        'uprofile': uprofile,
        'toChat': toChat,
    }
    return render(request, 'match/profile.html', context)

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
            if choice != 'csrfmiddlewaretoken':
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
             if choice != 'csrfmiddlewaretoken':
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

def ChatView(request, username1, username2):
    uprofile = Profile.objects.get(user=request.user)
    if ChatRoom.objects.filter(room_name=username1+username2):
        print("Chat room found!")
        chatRoom = ChatRoom.objects.get(room_name=username1+username2)
    elif ChatRoom.objects.filter(room_name=username2+username1):
        print("Chat room found, usernames reversed!")
        return HttpResponseRedirect(reverse('chatView', kwargs={'username1': username2, 'username2': username1}))
    else: #Create chat room with username1 as the first one
        chatRoom = ChatRoom(room_name=username1+username2)
        chatRoom.save()
        print("Chat room created!")
    messages = Message.objects.filter(chatRoom=chatRoom)
    ousername = username1 if uprofile.user.username != username1 else username2
    context = {
        'messages': messages,
        'profile': uprofile,
        'ousername': ousername, 
        'room_name': username1+username2,
    }
    return render(request, 'match/chat.html', context)

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
                    #crelationships = crelationships.filter(relationship='like')
                    profilesC = Profile.objects.filter(profileOther__relationship='like').filter(profileOther__profileUser=uprofile)
                    profiles = profilesC & profiles
                case 'unlikes':
                    #crelationships = crelationships.filter(relationship='not like')
                    profilesC = Profile.objects.filter(profileOther__relationship='unlike').filter(profileOther__profileUser=uprofile)
                    profiles = profilesC & profiles
                case 'unseen':
                    """
                    I have all relationships that currently are associated with 'profileUser'. Now how do I find all-
                    -profiles that are not "related" to profileUser?
                        profiles = [profile for profile in allProfiles: if not profile in crelationships.profileOther: return profile]
                    I tried creating an "unseen" relationship, but the issue is that when a new user creates an account, you would-
                    -have to make ALL of the CURRENT users have a new relationship with that person.
                    Instead we use the "difference" method:
                    """
                    profilesC = Profile.objects.all().difference(Profile.objects.filter(profileOther__profileUser=uprofile))
                    profiles = profilesC & profiles
                case 'liked':
                    profiles = Profile.objects.filter(profileUser__relationship="like") & profiles

    uinterests = [interest.interest for interest in uprofile.interest_set.all()]
    count = 0
    for profile in profiles:
        for interest in profile.interest_set.all():
            if interest.interest in uinterests:
                count += 1
        profile.count = count
        profile.save()
        count = 0
    profiles = profiles.order_by('-count')

    paginator = Paginator(profiles, 20) #Show only 20 profiles per
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'uprofile': uprofile,
        'profiles': profiles,
        'relationships': relationships,
        'likes': likes,
        'unlikes': unlikes,
        'uinterests': uinterests,
        'page_obj': page_obj,
    }

    return render(request, 'match/profileSearch.html', context)


from django.db.models import Count
from django.db.models import Max
from django.db.models import Min
from random import randint
def StartChatView(request):
    uprofile = Profile.objects.get(user=request.user)
    interests = Interest.objects.filter(profile=uprofile)
    context = {
        'uprofile': uprofile,
        'interests': interests,
    }
    if request.method == "POST":
        form = request.POST
        """
        Once the user presses "StartChatView", they will do these steps:
        1. Find out if there is an available room that fits these settings
        2. If there is, change the url and join that one
        3. If there is none, create the room that others can join
        """
        #Here we will try to find rooms that match their "1on1" or "group" option, and see if there are any available
        chatRooms = GroupChatRoom.objects.filter(num=form['num']) #Finds rooms that are either 1-on-1 or group
        count = 5 if form['num'] == 'group' else 2
        chatRooms = chatRooms.annotate(participant_count=Count('participant')) #annotates number of participants in each chatRoom
        chatRooms = chatRooms.filter(participant_count__lt=count)
        if chatRooms: #There are rooms with their 'num' selection
            #At this point, we have all rooms that match the correct participant limit
            if form['prio'] == 'prio': #The person is looking for a room whose GroupChat.interest is what they put
                chatRooms = chatRooms.filter(interest=form['interest'])
            if chatRooms: #This is after either a filter from an interest, or not filtering
                #We must filter from age now
                """
                I want to get a new chatRooms QuerySet.
                There are two different approaches that are possible here:
                    1. The QuerySet contains chatRooms where all participants are aged: 
                            form['min'] <= profile.age <= form['max']
                    2. Get chatRooms where the:
                        form['min'] <= chatRoom.mini and chatRoom.maxi <= form['max']
                        If your age does not fall within range, you will not be allowed in.
                    The second method is easier to implement
                """
                chatRooms = chatRooms.filter(mini__gte=form['min']).filter(maxi__lte=form['max'])
                if chatRooms:
                    chatRoom = chatRooms[randint(0,chatRooms.count()-1)]
                    print("Joined Room!")
                else:
                    chatRoom = GroupChatRoom(num=form['num'], mini=form['min'], maxi=form['max'], prio=form['prio'], interest=form['interest'], npart=0)
                    chatRoom.save()
                    print("New Room!")
            else: #could not find any chat rooms with this prio
                chatRoom = GroupChatRoom(num=form['num'], mini=form['min'], maxi=form['max'], prio=form['prio'], interest=form['interest'], npart=0)
                chatRoom.save()
                print("New Room!")
        else: #There is not an available room
            chatRoom = GroupChatRoom(num=form['num'], mini=form['min'], maxi=form['max'], prio=form['prio'], interest=form['interest'], npart=0)
            chatRoom.save()
            print("New Room!")

        return HttpResponseRedirect(reverse('RandomChat', kwargs={'id': chatRoom.id})) #Sends you to the chatRoom
    
    return render(request, 'match/startChat.html', context)

def RandomChatView(request, id):
    uprofile = Profile.objects.get(user=request.user)
    chatRoom = GroupChatRoom.objects.get(id=id)
    oprofiles = [p.profile for p in Participant.objects.filter(groupChatRoom=chatRoom)]
    messages = Message.objects.filter(groupChatRoom=chatRoom)
    context = {
        'profile': uprofile,
        'oprofiles': oprofiles,
        'messages': messages,
        'chatRoom': chatRoom,
        'room_id': id,
    }
    #CREATE PARTICIPANT HERE INSTEAD
    if request.method == "GET":
        Participant(profile=uprofile, groupChatRoom=chatRoom).save()
        print('New Participant')
    if request.method == "POST":
        print("I am leaving")
        Participant.objects.filter(profile=uprofile).get(groupChatRoom=chatRoom).delete()
        print("Deleted Participant")
        if chatRoom.participant_set.count() == 0:
            chatRoom.delete()

    return render(request, 'match/randomChat.html', context)