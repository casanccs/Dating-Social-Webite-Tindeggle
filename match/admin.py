from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Profile)
admin.site.register(Interest)
admin.site.register(Relationship)
admin.site.register(Message)
admin.site.register(GroupChatRoom)
admin.site.register(Participant)