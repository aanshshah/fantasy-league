from league.models import Player, League, SpecialUser, Trade_Notification, History, Match_Pairings, User_Match_Details
from django.contrib.auth.models import User
import datetime
from itertools import combinations


def make_pairings(request, league_id):
    '''

    :param request:
    :param league_id:
    :return:
    '''
    league = League.objects.get(id=league_id)
    users_league = league.players
    id_users = []
    pairing_combos = []
    for user in users_league:
        id_users.append(user.id)
    for comb in combinations(id_users, 2):
        pairing_combos.append(comb)
    games_in_season = league.games_in_season
    duration_between_games = league.duration_between_games
    if len(pairing_combos) < games_in_season:
        difference =  games_in_season - len(pairing_combos)
        if difference <= len(pairing_combos):
            difference = pairing_combos[:difference]
            for comb in difference:
                pairing_combos.append(comb)
        else:
            counter = 0
            temp_combo = pairing_combos
            while(counter != difference):
                for game in temp_combo:
                    pairing_combos.append(game)
                    counter = counter + 1
            if counter > difference:
                pairing_combos = pairing_combos[:len(pairing_combos)-(counter-difference)]
    elif len(pairing_combos) > games_in_season:
        pairing_combos = pairing_combos[:games_in_season]
    league.pairings = pairing_combos
    league.save()
    for pair in pairing_combos:
        match = Match_Pairings(league = league)
        for id in pair:
            user = User.objects.get(id=id)
            match.users.add(user)
            match.save()
    pass

def compute_winner(request):
    player_one_sum = 0
    player_two_sum = 0

    pass

def compete(request):
    
    pass
'''
DONE
Pairing Mechanism:
1) find a unique combination that doesn't exist
    a) first find all the possible unique combinations
    [",".join(map(str,comb)) for comb in combinations(L, 3)]
    L is the list of all the id numbers separated by commas
    b) second compare that to the list of combinations that already exist
    c) third pick one element that does not overlap the two sets
    d) use that pairing
2) if there are no unique pairings left, then randomly generate a pairing

Competition:
1) Sum up the ratings for each player on a user's team
2) Compare that to the player's opponent and compute a winner
3) Update the user database
'''

'''
- Allow users to pick the start date of the competition
- Allow users to choose how many games before the playoffs
- You can store these values in the database for the league preference
and only allow the admin to edit these values
    - Don't allow the admin to change these variables after the first game
    of the season starts
- Maybe also let the admin decide how frequently the games in the league
take place
- Use celery as a task manager - run them for a certain duration that
each league manager specifies
'''