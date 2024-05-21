from django.http import HttpResponse, HttpRequest
from django.shortcuts import render

def shop_index(request: HttpRequest):
    return HttpResponse('<h1>Hello World!</h1>')
