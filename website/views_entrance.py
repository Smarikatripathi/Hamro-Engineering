from django.shortcuts import render

def entrance_page(request):
    return render(request, 'entrance.html')
