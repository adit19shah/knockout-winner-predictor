from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def home(request):
    if request.method=="POST":
        no_of_teams=request.POST.get('no_of_teams')
        string_of_teams_list=request.POST.get('string_of_teams_list')
        list_of_teams=string_of_teams_list.slice(",")

        #Count a team only once even if it has been entered multiple times in input string
        #i.e. remove duplicates from list_of_teams
        list_of_teams=list(set(list_of_teams))

        #If the number of distinct teams entered in list is not equal to number of teams provided
        if len(list_of_teams) != no_of_teams:
            return render(request,'validation_error.html')

        return render(request,'display_output.html')
    return render(request,'index.html')

