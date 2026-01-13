from django.shortcuts import render


def about(request):
    """
    View to return about page
    """
    return render(request, 'about.html')
