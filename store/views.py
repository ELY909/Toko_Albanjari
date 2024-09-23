from django.shortcuts import render

def index(request):
    return render(request, 'store/index.html')

def about(request):
    return render(request, 'store/about.html')
