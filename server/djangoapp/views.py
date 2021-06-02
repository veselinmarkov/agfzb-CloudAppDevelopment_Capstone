from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404, render, redirect
# from .models import 
# from .restapis import related methods
from .restapis import get_dealers_from_cf
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
# from django.views.generic import TemplateView
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.

# Create an `about` view to render a static about page
def about(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/static_aboutus.html', context)

# Create a `contact` view to return a static contact page
def contact(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/static_contactus.html', context)

# Create a `login_request` view to handle sign in request
def login_request(request):
    context = {}
    if request.method == 'POST':
        username = request.POST['username']
        psw = request.POST['psw']
        # print(username, psw)
        user = authenticate(username=username, password=psw)
        # print(user)
        if user is not None:
            login(request, user)
            return redirect('djangoapp:index')
        else:
            context['message'] = 'Invalid username or password'
            return render(request, 'djangoapp/registration.html', context)
    else:
        return render(request, 'djangoapp/registration.html', context)


# Create a `logout_request` view to handle sign out request
def logout_request(request):
    logout(request)
    return redirect('djangoapp:index')

# Create a `registration_request` view to handle sign up request
def registration_request(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context)
    else:
        # in case of POST mothod
        username = request.POST['username']
        user_ok = False
        try:
            user = User.objects.get(username=username)
        except ObjectDoesNotExist:
            user_ok = True
        if user_ok:
            user = User.objects.create_user(first_name=request.POST['firstname'], last_name=request.POST['lastname'],
                username=username, password=request.POST['psw'])
            login(request, user)
            logger.error('New user created: ' +username)
            return redirect('djangoapp:index')
        else:
            context['message'] = 'The user {} already exists'.format(username)
            return render(request, 'djangoapp/registration.html', context)

# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    #context = {}
    if request.method == "GET":
        #return render(request, 'djangoapp/index.html', context)
        url = 'https://11ab05d1.eu-gb.apigw.appdomain.cloud/bestcars/dealership'
        dealerships, stat = get_dealers_from_cf(url)
        if stat['status'] !=200:
            return HttpResponse(json.dumps(result))    
        dealer_names = ' '.join([dealer['city'] for dealer in dealerships])
        return HttpResponse(dealer_names)


# Create a `get_dealer_details` view to render the reviews of a dealer
# def get_dealer_details(request, dealer_id):
# ...

# Create a `add_review` view to submit a review
# def add_review(request, dealer_id):
# ...

