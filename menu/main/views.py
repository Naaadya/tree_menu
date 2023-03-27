from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.db import connection
from django.db import reset_queries

from datetime import datetime
from django.utils import timezone



# Create your views here.



def index(request, path):
    return render(request,"main/index.html")
