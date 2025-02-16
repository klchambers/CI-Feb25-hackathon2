from django.shortcuts import render


def home(request):
    '''
    Render Homepage
    '''
    return render(request, 'home/index.html')


def team(request):
    return render(request, 'home/team.html')


def privacy(request):
    return render(request, 'home/privacy.html')


def cookies(request):
    return render(request, 'home/cookies.html')


def service(request):
    return render(request, 'home/service.html')
  

def safety(request):
    return render(request, 'home/safety.html')

def success_stories(request):
    return render(request, 'home/success_stories.html')

