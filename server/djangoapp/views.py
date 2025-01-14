from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404, render, redirect
from django.views import View
from .models import CarModel
# from .restapis import related methods
from .restapis import * 
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
    context = {}
    if request.method == "GET":
        #return render(request, 'djangoapp/index.html', context)
        url = 'https://11ab05d1.eu-gb.apigw.appdomain.cloud/bestcars/dealership'
        try:
            dealerships = get_dealers_from_cf(url)
        except RestException as e1:
            return HttpResponse('Rest Exception \n' + str(e1))
        context['dealerships'] = dealerships
        #except Exception as e2:
        #    return HttpResponse('Network Exception \n' + str(e2))
        #dealer_names = ' '.join([dealer['city'] for dealer in dealerships])
        return render(request, 'djangoapp/index.html', context)


# Create a `get_dealer_details` view to render the reviews of a dealer
def get_dealer_details(request, dealer_id):
    context = {}
    if request.method == "GET":
        url = 'https://11ab05d1.eu-gb.apigw.appdomain.cloud/bestcars/review'
        try:
            reviews = get_dealer_reviews_from_cf(url, dealer_id)
        except RestException as e1:
            return HttpResponse('Rest Exception \n' + str(e1))
        # get the dealer object based on the dealer_id
        url = 'https://11ab05d1.eu-gb.apigw.appdomain.cloud/bestcars/dealership'
        try:
            dealer = get_dealers_from_cf(url, id=dealer_id)
        except RestException as e1:
            return HttpResponse('Rest Exception \n' + str(e1))
        if len(dealer) == 0:
            context['dealer'] = {'id': dealer_id, 'full_name': "No name found"}
        else:
            context['dealer'] = dealer[0]
        #print(dealer)
        context['reviews'] = reviews
        #print(reviews)
        return render(request, 'djangoapp/dealer_details.html', context)


def get_sentiment(request):
    if request.method == 'GET':
        label = analyze_review_sentiments('Great service!')
        return HttpResponse(label)

# Create a `add_review` view to submit a review
class Add_review(View):
#def add_review(request, dealer_id):
    def post(self, request, dealer_id, dealer_name):
        if not request.user.is_authenticated:
            return {'error': 'Add Review method: Not registered user'}
        review = {}
        review['name'] = request.user.first_name +' ' +request.user.first_name
        try:
            purch_date = datetime.strptime(request.POST['purchasedate'][:10], '%Y-%m-%d')
            review['purchase_date'] = purch_date.strftime('%m/%d/%Y')
        except ValueError as v1:
            print('In datetime conversion: ' + str(v1))
        review['dealership'] = int(dealer_id)
        review['review'] = request.POST['content']
        review['purchase'] = True if request.POST['purchasecheck'] == 'on' else False
        carmodel = CarModel.objects.get(id=request.POST['car'])
        review['car_make'] = carmodel.carmake.name
        review['car_model'] = carmodel.name
        review['car_year'] = carmodel.year.strftime("%Y")
        json_payload ={'review': review}
        url = 'https://11ab05d1.eu-gb.apigw.appdomain.cloud/bestcars/review'
        try:
            post_request(url, json_payload)
        except RestException as e1:
            return HttpResponse('Rest Exception \n' + str(e1))
        return redirect('djangoapp:dealer_details', dealer_id)

    def get(self, request, dealer_id, dealer_name):
        context = {'dealer_id': dealer_id, 'dealer_name': dealer_name}
        carmodels = CarModel.objects.filter(dealer=dealer_id)
        context['cars'] = carmodels
        return render(request, 'djangoapp/add_review.html', context)



