from django.shortcuts import render


def home(request):
    # als je nog geen Page met slug 'home' hebt, gebruik een tijdelijke placeholder
    return render(request, 'website/page.html', {'page': {'title': 'Welkom', 'body': 'Dit is de homepage'}})
