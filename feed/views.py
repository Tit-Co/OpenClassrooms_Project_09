from django.shortcuts import render


def feed_index(request):
    return render(request, 'feed/index.html')
