from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect


def choose(request):
    context = request.GET.get('context')
    print(context)
    return render(request, 'prune/choose.html')

def magic(request):
    print("TEST")
    if request.method == 'POST':
        form = PriceAssessmentSection1(request.POST)
        print("LOOK HERE", request.POST.get())
    return render(request, 'prune/magic.html')
