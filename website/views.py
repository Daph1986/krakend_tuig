from django.shortcuts import render


def home(request):
    return render(request, 'index.html')


def zing_mee(request):
    return render(request, 'zing_mee.html')
