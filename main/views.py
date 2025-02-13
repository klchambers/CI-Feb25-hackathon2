from django.shortcuts import render

def matches(request):
    return render(request, 'main/match-making.html')
