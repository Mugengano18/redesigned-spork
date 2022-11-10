from django.http import HttpResponse
import requests
import json
import folium
from folium import plugins
from .models import Retail_information
from .forms import Retail_info, UserRegisterForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, reverse


# Create your views here.
def home(request):
    return render(request, "index.html")


def signUser(request):
    if request.method == "POST":
        fname = request.POST['fname']
        lname = request.POST['lname']
        phone = request.POST['phone']
        pswd1 = request.POST['pass1']
        pswd2 = request.POST['pass2']

        user_create = User.objects.create_user(phone, pswd1)
        user_create.first_name = fname
        user_create.last_name = lname

        user_create.save()

        messages.success(request, "Successfully created account.")

        return redirect('Home')
    return render(request, 'user_registration.html')


def loginUser(request):
    if request.user.is_authenticated:
        return redirect(reverse("index"))
    if request.method == 'POST':
        phone = request.POST['phone']
        pswd1 = request.POST['pass1']

        user_login = authenticate(username=phone, password=pswd1)

        if user_login is not None:
            login(request, user_login)
            request.session['phone'] = phone
            fname = user_login.first_name
            return redirect('Home')
        else:
            messages.error(request, "phone or password incorrect!!")
            return redirect('login')
    return render(request, 'user_registration.html')


def logoutUser(request):
    logout(request)
    messages.success(request, 'Logged out successfully!')
    return redirect('login')


def retail_registration(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse('login')
    else:
        form = UserRegisterForm()
    return render(request, 'shop_register.html', {'form': form})



def get_retail_information(request):
    if request.method == 'POST':
        # make requests from api.ipify.org
        ip = requests.get('https://api.ipify.org?format=json')
        ip_data = json.loads(ip.text)
        # make requests from ip-api.com
        res = requests.get('http://ip-api.com/json/' + ip_data["ip"])
        data_one = json.loads(res.text)

        ret = Retail_information(fullname=request.POST['fullname'], company_name=request.POST['company'],
                                 latitude=data_one['lat'], longitude=data_one['lon'], city=data_one['city'],
                                 sector=data_one['sector'], cell=data_one['cell'])
        ret.save()
        return HttpResponse('Successfully registered your business')
    else:
        form = Retail_info()

    return render(request, 'shop_register.html', context={'form': form})


@login_required(login_url='login')
def map_detail(request):
    data_list = Retail_information.objects.values_list('latitude', 'longitude')

    map1 = folium.Map(location=[-1.952183, 30.054957], tiles='OpenStreetMap', zoom_start=9.5)

    plugins.FastMarkerCluster(data_list, icon=None).add_to(map1)

    map1 = map1._repr_html_()

    context = {
        'map1': map1,
    }

    return render(request, 'map.html', context)
