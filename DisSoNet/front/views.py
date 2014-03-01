from django.shortcuts import render

# Create your views here.

def home(request):
    context = {'state':'none'}
    return render(request, 'index.html', context)
