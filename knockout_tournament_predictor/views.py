from django.shortcuts import render
from django.http import HttpResponse
import math

# Create your views here.

def home(request):
    if request.method=="POST":
        no_of_teams=int(request.POST.get('no_of_teams'))
        string_of_teams_list=request.POST.get('string_of_teams_list')

        # Declare invalid input if number of teams greater than 16 or less than 0
        if no_of_teams>16 or no_of_teams<0:
            context={'out_of_domain':no_of_teams}
            return render(request, 'validation_error.html',context)

        # Declare invalid input if number of teams not a power of 2
        if math.ceil(math.log2(no_of_teams)) != math.floor(math.log2(no_of_teams)):
            context={'not_power_2':no_of_teams}
            return render(request, 'validation_error.html',context)

        #Split the input string by , to make a list of participating teams
        list_of_teams=string_of_teams_list.split(",")

        #Count a team only once even if it has been entered multiple times in input string
        #i.e. remove duplicates from list_of_teams
        list_of_teams=list(set(list_of_teams))

        #If the number of distinct teams entered in list is not equal to number of teams provided
        if len(list_of_teams) != no_of_teams:
            context = {'list_team_inconsistent': no_of_teams}
            return render(request,'validation_error.html',context)

        


        return render(request,'display_output.html')
    return render(request,'index.html')

