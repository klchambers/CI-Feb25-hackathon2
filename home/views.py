from django.shortcuts import render

def home(request):
    '''
    Render Homepage
    '''
    return render(request, 'home/index.html')