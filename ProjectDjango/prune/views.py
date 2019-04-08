from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect


def choose(request):
    context = request.GET.get('context')
    print(context)
    return render(request, 'prune/choose.html')
