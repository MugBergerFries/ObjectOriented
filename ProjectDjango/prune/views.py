from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect


def choose(request):
    context = request.GET.get('context')
    print("HERE IS CONTEXT",context)
    return render(request, 'prune/choose.html')

def magic(request):
    print("TEST123")
    #if request.method == 'POST':
    #print("LOOK HERE", request.POST.get())
    return render(request, 'prune/magic.html')
