from django.shortcuts import render
from django.http import HttpResponse, HttpRequest


def shop_index(request: HttpRequest):
    return HttpResponse('Hello World!')

