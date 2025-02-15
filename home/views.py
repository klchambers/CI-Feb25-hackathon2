from django.shortcuts import render

def home(request):
    '''
    Render Homepage
    '''
    return render(request, 'home/index.html')

def team(request):
    return render(request, 'home/team.html')