from django.shortcuts import render

# Create your views here.

def front(request):
    context = {}
    return render(request, "ui/index.html", context)
