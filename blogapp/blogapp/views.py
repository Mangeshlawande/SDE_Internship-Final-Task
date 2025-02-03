from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def home(request):
    # return HttpResponse(request, "welcome to tweets page ")
    return render(request, 'layout.html', {})
