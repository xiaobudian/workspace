# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from django.shortcuts import render, render_to_response
from django.http import HttpResponse
import requests
from .models import Province, City, Town, Air, History
import json
import re
import os
from xml.dom.minidom import Document

# Create your views here.
baseUri = "http://apis.baidu.com/3023/weather/"

def getareadata(url):

    headers = {
        'apikey':'fb655c55aed101b68d2e1f3bf5534738',
    }

    response = requests.get(url, headers=headers)

    return response

def updatearea(model, url, parent):

    data = getareadata(baseUri+url)
    all = ""
    for d in data.json():
        m = model()
        m.name = d[0]
        m.code = d[1]
        m.parent = parent
        m.save()
        all += m.__str__() + " "

    return all

def index(request):

    return HttpResponse("Welcome to ls weather info services.")

def getweather(request, code):

    airs = Air.objects.filter(code=code)
    needupdate = True
    air = None
    if (airs.count() > 0):
        air = airs.first()
    if (air is not None):
        if(air.time == '000'):
            needupdate = False
    else:   #if not exist create a empty 
        air = Air()
        air.code = code
        air.save()
    if (needupdate):
        url = baseUri + "weather?id=" + code
        weather = getareadata(url)
        
        times = re.findall('"time":([0-9]{10}),',weather.text, re.S)
        air.time = times[0]
        air.weather = weather.text
        air.code = code
        air.save()
        history = History()
        history.time = air.time
        history.code = air.code
        history.weather = air.weather
        history.save()
        return HttpResponse(air.weather+" updated")
    return HttpResponse(air.weather+" not update")

def updateprovince(request):
    Province.objects.all().delete()

    url = "province"

    return HttpResponse(updatearea(Province, url, '0'))

def updatecity(request):
    City.objects.all().delete()

    all = ""
    for p in Province.objects.all():
        url = "city?id=" + p.code
        all += updatearea(City, url, p.code)

    return HttpResponse(all)

def updatetown(request):
    Town.objects.all().delete()

    all = ""
    for c in City.objects.all():
        url = "town?id=" + c.code
        all += updatearea(Town, url, c.code)

    return HttpResponse(all)

def _createNode(doc, name, model):
    node = doc.createElement(name)
    node.setAttribute('name', model.name)
    node.setAttribute('code', model.code)
    return node

def _createDoc():
    doc = Document()
    body = doc.createElement('body')
    doc.appendChild(body)
        
    for p in Province.objects.all():
        province = _createNode(doc, 'province', p)
        for c in City.objects.filter(parent=p.code):
            city = _createNode(doc, 'city', c)
            for t in Town.objects.filter(parent=c.code):
                town = _createNode(doc, 'town', t)
                city.appendChild(town)
            province.appendChild(city)
        body.appendChild(province)
    return doc        

def getareaxml(request):
    
    filename = os.path.dirname(__file__) + "/area.xml"
    if not os.path.exists(filename):
        doc = _createDoc()        
        f = open(filename,'w')
        f.write(doc.toprettyxml(indent = ''))
        f.close()        
        
    file = open(filename, 'rb')
    data = file.read()
    return HttpResponse(data, content_type="application/xml")
    
