from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def home(request):
    if request.method=="POST":
        return render(request,'display_output.html')
    return render(request,'index.html')

