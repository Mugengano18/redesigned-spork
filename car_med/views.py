from django.http import HttpResponse
from django.shortcuts import render
import requests
import json
import folium
from folium import plugins
from .models import Retail_information
from .forms import Retail_info


# Create your views here.
def home(request):
    return render(request, "index.html")


def get_retail_information(request):
    if request.method == 'POST':
        # make requests from api.ipify.org
        ip = requests.get('https://api.ipify.org?format=json')
        ip_data = json.loads(ip.text)
        # make requests from ip-api.com
        res = requests.get('http://ip-api.com/json/' + ip_data["ip"])
        data_one = json.loads(res.text)

        ret = Retail_information(fullname=request.POST['fullname'], company_name=request.POST['company'],
                                 latitude=data_one['lat'], longitude=data_one['lon'], city=data_one['city'])
        ret.save()
        return HttpResponse('Successfully registered your business')
    else:
        form = Retail_info()

    return render(request, 'register.html', context={'form': form})


def map_detail(request):
    data_list = Retail_information.objects.values_list('latitude', 'longitude')

    map1 = folium.Map(location=[-1.952183, 30.054957], tiles='OpenStreetMap', zoom_start=9.5)

    plugins.FastMarkerCluster(data_list, icon=None).add_to(map1)

    map1 = map1._repr_html_()

    context = {
        'map1': map1,
    }

    return render(request, 'map.html', context)
