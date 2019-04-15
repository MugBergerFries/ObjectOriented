from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect


def choose(request):
    context = request.GET.get('context')
    print("HERE IS CONTEXT",context)
    if request.method == 'POST':
        if request.POST.get("id_7KCYH5sfijoldjichs8ff8"):
            print("It worked")
        elif request.POST.get("save_next"):  # You can use else in here too if there is only 2 submit types.
            return HttpResponseRedirect(reverse('portal_sec2'))

    print("IS THIS WORKING")
    return render(request, 'prune/choose.html')

def magic(request):
    print("TEST123")
    #if request.method == 'POST':
    #print("LOOK HERE", request.POST.get())
    return render(request, 'prune/magic.html')
