from django.db import models
from django.contrib.auth.models import User

class Interest(models.model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    interest = models.CharField(max_length=30)

    def __str__(self):
        return f"{self.user}: {self.interest}"

"""
Let's say we then have these interests:
    tester1: interest1
    tester1: interest2
    tester1: interest3
    tester2: interest2
    tester2: interest4
    tester3: interest1
    tester3: interest2
    tester4: interest1
    tester4: interest2
    tester4: interest3

Then there is a tester5 with no interests
"""

def SomeView(request):
    cuser = request.User #Assume you are "tester1"
    users = User.objects.all()
    """
    I want to sort the users to be put in an order such that the users you have more "common interests" in, are put ahead:
    (Assume you are tester1)
        <QuerySet [ <tester4>  ,  <tester3>  ,  <tester2>  ,  <tester5>  ]>
    """
