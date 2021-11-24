from django.shortcuts import render
from django.http import HttpResponse
import numpy as np
import math

#Defining several global variables
pow3 = np.zeros(20,dtype=np.longlong)
ways = np.zeros(20,dtype=np.longlong)
prob = np.zeros(shape=(20,20),dtype=np.double)
dp1 = np.zeros(50000000,dtype=np.double)
dp2 = np.zeros(50000000,dtype=np.double)
ans = np.zeros(20,dtype=np.double)

#Functions needed for our code
def valid_mask(mask):
    i = bin(mask).count('1')
    if (i == 0):
        return False

    while i > 1:
        if (i % 2 == 1):
            return False  # number of bits not a power of 2
        i = i // 2

    # mask is a valid mask
    return True


def get_bit(mask, i):
    # this function is for getting value of bit in dp2
    # normal bitwise operators don't work
    # since we have 3 possible values - 0,1 and 2
    mask = mask % pow3[i + 1]
    b = mask // pow3[i]
    return b


def calculate_Probability(mask, n):
    # Don't Recalculate if already memoised
    if dp2[mask] != -1:
        return dp2[mask]

    p = 0.0

    for i in range(n - 1, -1, -1):
        b1 = get_bit(mask, i)  # last losing bit
        if b1 == 2:
            for j in range(n):
                b2 = get_bit(mask, j)
                if b2 == 1:
                    new_mask = mask - 1 * pow3[j] - 2 * pow3[i]
                    p += prob[j][i] * calculate_Probability(new_mask, n)
            break

    # memoise the answer for dp2
    dp2[mask] = p
    return p


def Prob_Mask_To_Submask(mask, submask, n):
    # 0 bit --> team already eliminated
    # 1 bit --> team expected to win
    # 2 bit --> team expected to loose

    new_mask = 0
    for i in range(n):
        if (((mask & (1 << i)) != 0) and ((submask & (1 << i)) != 0)):
            # team i wins
            new_mask += 1 * pow3[i]

        elif (((mask & (1 << i)) != 0) and ((submask & (1 << i)) == 0)):
            # team i loses
            new_mask += 2 * pow3[i]

        else:
            # team i inactive or has already lost
            new_mask += 0 * pow3[i]

    p = calculate_Probability(new_mask, n)
    return p


def solve(n):
    # store powers of 3 for future use
    pow3[0] = 1
    for i in range(1, n + 1):
        pow3[i] = pow3[i - 1] * 3

    # storing ways to play games with 2*i teams for future use
    ways[1] = 1
    for i in range(2, n // 2 + 1):
        ways[i] = ways[i - 1] * (2 * i - 1)

    # initalize dp1 for bottom-up approach
    for i in range(1 << n):
        dp1[i] = 0.00

    # Base case for dp1, initally all teams are in game
    dp1[(1 << n) - 1] = 1.00

    # initalize dp2 for top-down approach
    for i in range(pow3[n]):
        dp2[i] = -1.00  # initialize with some dummy value

    # Base case for dp2, finally all players will be either winners or loosers
    dp2[0] = 1.00

    # 0 bit --> team already eliminated
    # 1 bit --> team still in tournament

    for i in range((1 << n) - 1, -1, -1):
        if valid_mask(i):
            # enumerating the submasks optimally
            j = i
            while (j > 0):
                if (bin(i).count('1') == 2 * bin(j).count('1')):
                    m = bin(i).count('1')  # counts total set bits in i
                    k = ways[m // 2]
                    d = 1 / k
                    dp1[j] += d * dp1[i] * Prob_Mask_To_Submask(i, j, n)
                j = (j - 1) & i

    # store final answer
    for i in range(n):
        ans[i] = dp1[(1 << i)]

#View
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

        #create a mapping between team and number/index for further part of the code
        my_dict={}
        for i in range(len(list_of_teams)):
            my_dict[i]=list_of_teams[i]

        #Create probability matrix
        #prob[i][j] = probability of team i winning over team j
        '''
        for i in range(no_of_teams):
            for j in range(no_of_teams):
                tmp=my_dict[i].objects.all().filter(opp_team_name=my_dict[j])
                for x in tmp: #Not to be mislead by loop, tmp will have only 1 entry
                    prob[i][j]=x.no_of_wins/x.tot_matches
        '''
        for i in range(no_of_teams):
            for j in range(no_of_teams):
                if prob[j][i] != 0:
                    prob[i][j] = 1 - prob[j][i]
                else:
                    prob[i][j] = (i + 1) * (j + 1) * 0.01

        print("Number of teams are: ", end=" ")
        print(no_of_teams)
        print("The probability table is as follows: ")
        for i in range(no_of_teams):
            my_list = []
            for j in range(no_of_teams):
                my_list.append(prob[i][j])
            print(my_list)

        # solve the question for n teams with given probability table
        solve(no_of_teams)

        # print answer
        win_list={}
        for i in range(no_of_teams):
            win_list[my_dict[i]]=ans[i]

        return render(request,'display_output.html',context=win_list)
    return render(request,'index.html')

