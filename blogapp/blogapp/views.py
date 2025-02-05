from django.shortcuts import render
# Create your views here.

def home(request):
    # return HttpResponse(request, "welcome to tweets page ")
    return render(request, 'layout.html', {})
