from django.shortcuts import render_to_response, redirect, render
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
# from django.template.context import RequestContext
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from forms import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth.forms import UserCreationForm
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from league.models import Player, League, SpecialUser, Trade_Notification, History, Match_Pairings, User_Match_Details
from django.core.context_processors import csrf
from django.contrib.auth.models import User
import datetime
from .forms import S3DirectUploadForm
from django.views.generic import FormView
import numpy as np
import itertools
import boto3
from django.core.files.storage import FileSystemStorage

class MyView(FormView):
    template_name = 'form.html'
    form_class = S3DirectUploadForm

# def home(request):
#    context = RequestContext(request,
#                            {'request': request,
#                             'user': request.user})
#    return render_to_response('home.html',
#                              context_instance=context)
@csrf_exempt
def handler404(request):
    response = render_to_response('404.html', {},
                                  context_instance=RequestContext(request))
    response.status_code = 404
    return response

def test_404(request):
    return render(request, '404.html')

@csrf_exempt
def handler500(request):
    response = render_to_response('404.html', {},
                                  context_instance=RequestContext(request))
    response.status_code = 500
    return response

@csrf_exempt
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/profile')

    else:
        form = UserCreationForm()
    token = {}
    token.update(csrf(request))
    token['form'] = form

    return render_to_response('registration/registration_form.html', token)

@csrf_exempt
def registration_complete(request):
    return redirect('/profile')

# @csrf_exempt
# def register_success(request):
#     return render_to_response(
#         'success.html',
#     )

@csrf_exempt
def logout_page(request):
    logout(request)
    return HttpResponseRedirect('/')


@login_required
@csrf_exempt
def home(request):
    if request.user.is_authenticated():
        player = Player.objects.filter(user=request.user)
        league = League.objects.filter(players=request.user)
        context = {'user': request.user,
                   'player': player,
                   'league': league}
        return redirect('/profile')
        # return render_to_response('home.html', context)
    else:
        context = {'user': request.user,
                   }
        return redirect('/login')

@csrf_exempt
def profile(request):
    if request.user.is_authenticated():
        player = Player.objects.filter(user=request.user)
        num_players = len(player)
        league = League.objects.filter(players=request.user)
        history = History.objects.filter(user=request.user)
        # print(history)
        if not history and league:
            history = History.objects.create(user=request.user,
                                             league=league[0])
            history.save()
        # print(history)
        num_leagues = len(league)
        if num_leagues == 0:
            num_leagues = False
        else:
            num_leagues = True
        something = False
        notification = []
        valid_notification = []
        valid = False
        for players in player:
            trade_notification_exists = Trade_Notification.objects.filter(player_traded=players)
            for notify in trade_notification_exists:
                valid = False
                if notify.user_requesting_trade != request.user:
                    valid = True
                # for play in notify.player_traded.all():
                if len(notify.player_traded.all())>1 and valid:
                    valid_notification.append(notify)
        # print(num_leagues)
        form = S3DirectUploadForm()
        context = {'user': request.user,
                   'player': player,
                   'num_players': num_players,
                   'league': league,
                   'num_leagues': num_leagues,
                   'something': something,
                   'trade_notification': valid_notification,
                   'form': form}

        return render_to_response('profile.html', context)
    else:
        return redirect('/login')
    return render_to_response('home.html', context)

@csrf_exempt
def add_player(request):
    if request.user.is_authenticated():
        if request.method == 'POST':
            num_league = None
            something = False
            context = {'user': request.user,
                       'num_league': num_league,
                       'something': something}
            player_name = request.POST.get('add_player')
            player_name = str(player_name)
            player_name = player_name.split()
            first_name = player_name[0]

            if len(player_name)>1:
                last_name = player_name[1]
            else:
                last_name = 'lol you should have put in a last name'
            player = Player.objects.create(user=request.user,
                            first_name=first_name, last_name=last_name,
                            rating=0, league=League.objects.filter(players=request.user)[0])
            player.save()
            # file = request.FILES['myfile']
            # print(file)
            # file_name = str(player.id) + '.png'
            # file_name = 'what_is_going_on_in_here.png'
            # print(file_name)
            # image_result = open(file_name, 'wb')  # create a writable image and write the decoding result
            # image_result.write(file.read())
            # myfile = request.FILES['myfile']
            # myfile = request.POST.get('myfile')
            # fs = FileSystemStorage()
            # filename = fs.save('what_is_going_on_in_here.png', myfile)
            # uploaded_file_url = fs.url(filename)

            # path = '/Users/Aansh/Documents/Side Projects/'
            # s3 = boto3.resource('s3')
            # s3.meta.client.upload_file(path + file_name, 'fantleague', file_name)
            # os.remove(path + file_name)
            # return HttpResponse("success")

            # S3_SECRET_KEY = ''
            # S3_ACCESS_KEY = ''
            return redirect('/profile')
        else:
            return redirect('/profile')


@csrf_exempt
def delete_player(request):
    if request.user.is_authenticated():
        num_league = None
        something = False
        context = {'user': request.user,
                   'num_league': num_league,
                   'something': something}
        if request.method=='GET':
            first_name = request.GET.get('first_name')
            last_name = request.GET.get('last_name')
            player = Player.objects.filter(first_name=first_name, last_name=last_name)
            player.delete()
            return redirect('/profile')
        if request.method=='POST':
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            Player.objects.filter(user=request.user, first_name=first_name, last_name=last_name).delete()
            return redirect('/profile')
        else:
            return redirect('/profile')

@csrf_exempt
def create_league(request):
    if request.user.is_authenticated():
        prior_leagues = League.objects.filter(players=request.user)
        if len(prior_leagues) == 0:
            if request.method == "POST":
                user = request.user
                league_name = request.POST.get('create_league')
                league_password = request.POST.get('league_password')
                special_user = SpecialUser.objects.create(user=user, admin=True, rater=False)
                league = League.objects.create(name=league_name, password=league_password, special_users=special_user)
                league.save()
                league.players.add(user)
                league.save()
                return redirect('/league/'+str(league.id))
        else:
            num_leagues = 1
            something = False
            context = {'num_leagues': num_leagues,
                       'something': something}
            return render(request, 'profile.html', context)
    else:
        profile(request)

def file_upload_handler_view(request):
    if request.method == "POST":
        file_uploaded = request.FILES["name_of_file_input"]
        # print (file_uploaded.read())
        # Helpful attribute to get dropbox file metadata
        # like path on the server, size, thumbnail etc
        # print(file_uploaded.dropbox_metadata)

@csrf_exempt
def search_league(request):
    if request.GET.get('search_league'):
        search = request.GET.get('search_league')
        league_search = League.objects.filter(name__contains=search)
        num_league = len(league_search)
        something = True
        player = Player.objects.filter(user=request.user)
        num_players = len(player)
        league = League.objects.filter(players=request.user)
        history = History.objects.filter(user=request.user)
        # print(history)
        if not history and league:
            history = History.objects.create(user=request.user,
                                             league=league[0])
            history.save()
        # print(history)
        num_leagues = len(league)
        if num_leagues == 0:
            num_leagues = False
        else:
            num_leagues = True
        something = False
        notification = []
        valid_notification = []
        valid = False
        for players in player:
            trade_notification_exists = Trade_Notification.objects.filter(player_traded=players)
            for notify in trade_notification_exists:
                valid = False
                if notify.user_requesting_trade != request.user:
                    valid = True
                # for play in notify.player_traded.all():
                if len(notify.player_traded.all()) > 1 and valid:
                    valid_notification.append(notify)
        # print(num_leagues)
        form = S3DirectUploadForm()
        context = {'user': request.user,
                   'player': player,
                   'num_players': num_players,
                   'league': league,
                   'num_leagues': num_leagues,
                   'trade_notification': valid_notification,
                   'form': form,
                    'league_search': league_search,
                   'num_league': num_league,
                   'something': something}
        return render(request, 'profile.html', context)

@csrf_exempt
def search_player(request):
    if request.GET.get('search_player'):
        user = request.user
        league = League.objects.filter(players=user)[0]
        search = request.GET.get('search_player')
        user = User.objects.get(id=search)
        player_search = Player.objects.filter(user=user)
        num_league = 1
        league = League.objects.filter(id=league.id)[0]
        players = Player.objects.filter(league=league)
        users = league.players.all()
        user_in = []
        # num_league = None
        update_ranking(league)
        for user in users:
            user_in.append(User.objects.get(id=user.id))
            update_history(user)
        history = History.objects.filter(league_id=league.id).order_by('current_ranking')
        match_detail = Match_Pairings.objects.filter(league_id=league.id)
        detail = []
        for info in match_detail:
            # print (info.user)
            match_info = User_Match_Details.objects.filter(match_pairing=info)
            # for match_info in match_info:
            # print(match_info.user.id)
            detail.append(match_info)
        # print(detail)
        # match = User_Match_Details.objects.filter(match_pairing=match_detail)
        # print(match)

        context = {'league': league,
                   'players': players,
                   'user_in': user_in,
                   'num_league': num_league,
                   'history': history,
                   'match_detail': match_detail,
                   'player_search': player_search,
                   'specific_detail': detail
                   }
        # return HttpResponseRedirect('/searching/')
        return render(request, 'league.html', context)

@csrf_exempt
def join_league(request):
    if request.user.is_authenticated():
        if request.POST.get('join_league'):
            user = request.user.id
            league_id = request.POST.get('league_id')
            password = request.POST.get('join_league')
            league_requested = League.objects.filter(id=league_id, password=password)[0]
            success = False
            if league_requested:
                success = True
            if success:
                special_user = SpecialUser.objects.create(user=request.user, admin=False, rater=False)
                league_requested.players.add(user)
                league_requested.special_users = special_user
                league_requested.save()
    return redirect('/profile/')

@csrf_exempt
def get_league_page(request, league_id):
    if request.user.is_authenticated():
        # print(request.user.id)
        try:
            league = League.objects.filter(id=league_id)[0]
            players = Player.objects.filter(league=league)
            users = league.players.all()
            user_in = []
            num_league = None
            update_ranking(league)
            for user in users:
                user_in.append(User.objects.get(id=user.id))
                update_history(user)
            history = History.objects.filter(league_id=league_id).order_by('current_ranking')
            match_detail = Match_Pairings.objects.filter(league_id=league_id)
            detail = []
            for info in match_detail:
                # print (info.user)
                match_info = User_Match_Details.objects.filter(match_pairing=info)
                # for match_info in match_info:
                    # print(match_info.user.id)
                detail.append(match_info)
            # print(detail)
            # match = User_Match_Details.objects.filter(match_pairing=match_detail)
            # print(match)
            
            context = {'league': league,
                       'players': players,
                       'user_in': user_in,
                       'num_league': num_league,
                       'history': history,
                       'match_detail': match_detail,
                       'specific_detail': detail
                       }
            return render(request, 'league.html', context)
        except League.DoesNotExist:
            return redirect('/profile')
@csrf_exempt
def admin_page(request):
    if request.user.is_authenticated():
        user = request.user
        try:
            is_admin = SpecialUser.objects.filter(user=user)[0]
            # print(is_admin.user)
            player_admin = is_admin.admin
            # print(is_admin.admin)
            all_users = []
            if player_admin:
                users_in_league = League.objects.filter(players=user).all()
                for use in users_in_league:
                    # print(use.name)
                    all_users.append(use)
                # print(all_users)
                # all_users = users_in_league.players
                isa_rater = False
                rater = None
                for using in all_users:
                    for person in using.players.all():
                    # print(using.players.all())
                        check_user = SpecialUser.objects.filter(user=person)
                        for users in check_user:
                            if users.rater:
                                isa_rater = True
                                rater = users
                # print(len(all_users))
                league = League.objects.filter(players=user)[0]
                all_match_pairings = Match_Pairings.objects.filter(league=league)
                context = {'all_users': all_users,
                           'isa_rater': isa_rater,
                           'rater': rater,
                           'pairings': all_match_pairings}
                return render(request, 'admin.html', context)
            else:
                return redirect('/profile')
        except SpecialUser.DoesNotExist:
            return redirect('/profile')

@csrf_exempt
def make_rater(request):
    if request.user.is_authenticated():
        user = request.user
        try:
            is_admin = SpecialUser.objects.filter(user=user)[0]
            player_admin=is_admin.admin
            if player_admin:
                if request.POST.get('make_rater'):
                    # print('start')
                    new_rater = request.POST.get('make_rater')
                    # for users in new_rater:
                    #     print(users)
                    new_rater = User.objects.get(username=new_rater)
                    # print (new_rater)
                    rater = SpecialUser.objects.filter(user=new_rater)[0]
                    # print(rater)
                    rater.rater = True
                    rater.save()
                    # print('end')
                    return redirect('/admin')
                elif request.POST.get('delete_rater'):
                    # print('delete')
                    delete_rater = request.POST.get('delete_rater')
                    # print(delete_rater)
                    delete_rater = User.objects.get(username=delete_rater)
                    rater = SpecialUser.objects.filter(user=delete_rater)[0]
                    rater.rater = False
                    rater.save()
                    # print(rater.rater)
                    return redirect('/admin')
                return redirect('/admin')
            else:
                return redirect('/profile')
        except SpecialUser.DoesNotExist:
            return redirect('/profile')
    else:
        return redirect('/profile')

@csrf_exempt
def rater_page(request):
    if request.user.is_authenticated():
        user = request.user
        try:
            is_rater = SpecialUser.objects.filter(user=user)[0]
            player_rater = is_rater.rater
            if player_rater:
                league = League.objects.get(players=user)
                try:
                    all_players = Player.objects.filter(league=league).all()
                    # print(all_players)
                except Player.DoesNotExist:
                    all_players = None
                context = {'all_players': all_players,
                           'league': league}
                return render(request, 'rater.html', context)
            else:
                return redirect('/profile')
        except SpecialUser.DoesNotExist:
            return redirect('/profile')
    else:
        return redirect('/profile')

@csrf_exempt
def modify_rating(request):
    if request.method == 'POST':
        user = request.user
        ratings_list = request.POST.getlist('modify_rating')
        league = League.objects.get(players=user)
        all_players = Player.objects.filter(league=league).all()
        num_players = len(all_players)
        counter = 0
        for player in all_players:
            player.rating = ratings_list[counter]
            player.save()
            counter = counter + 1
        # if ratings_list == None:
        #     print('none')
        # else:
        #     print(len(ratings_list))
        # for rating in ratings_list:
        #     print(rating)
        # print(ratings_list)
        # return render(request, 'rater.html')
        return redirect('/profile/')
    else:
        return redirect('/profile/')

@csrf_exempt
def request_trade(request):
    if request.method == 'POST':
        user = request.user
        print('hit')
        if request.POST.get('trade_request') and request.POST.get('trade_player'):
            print('hit 1')
            date_requested = datetime.datetime.now()
            trade_request = request.POST.get('trade_request')
            player_trade = request.POST.getlist('trade_player')
            # print(len(player_trade))
            user_requesting_trade = user
            notification = Trade_Notification.objects.create(user_requesting_trade=user_requesting_trade,
                                              date_requested = date_requested,
                                              date_accepted = date_requested,
                                              trade_status = False)
            notification.save()
            for players in player_trade:
                traded_player = Player.objects.get(id=players)
                # print(traded_player.first_name)
                notification.player_traded.add(traded_player)
                notification.save()
        elif request.POST.get('trade_reject') and request.POST.get(
                'trade_requesting_user'):
            print('hit 2')
            trade_reject = request.POST.get('trade_reject')
            player_trade = request.POST.getlist('trade_player')[0]
            user_requesting_trade = request.POST.get('trade_requesting_user')
            user_requesting_trade = User.objects.get(id=user_requesting_trade)
            notification = Trade_Notification.objects.get(player_traded=player_trade, trade_status=False,
                                                          notification_active=True,
                                                          user_requesting_trade=user_requesting_trade)
            notification.trade_status = True
            notification.notification_active = False
            notification.rejected = True
            notification.accepted = False
            notification.save()
        elif request.POST.get('trade_accept') and request.POST.get(
                'trade_requesting_user'):
            print('hit 3')
            trade_accept = request.POST.get('trade_accept')
            player_trade = request.POST.getlist('trade_player')
            user_requesting_trade = request.POST.get('trade_requesting_user')
            user_requesting_trade = User.objects.get(id=user_requesting_trade)
            # for user in user_requesting_trade:
            #     user_request = user
            # print(user_request)


            notification = Trade_Notification.objects.get(player_traded=player_trade[0], trade_status=False,
                                                          notification_active=True,
                                                          user_requesting_trade=user_requesting_trade)
            notification.trade_status = True
            notification.notification_active = False
            notification.accepted = True
            notification.rejected = False
            notification.date_accepted = datetime.datetime.now()
            for player in player_trade:
                player = Player.objects.get(id=player)
                if player.user == user:
                    player.user = user_requesting_trade
                    player.save()
                elif player.user == user_requesting_trade:
                    player.user = user
                    player.save()
            notification.save()
        return redirect('/profile')
    else:
        return redirect('/profile')

@csrf_exempt
def trade_page(request):
    if request.user.is_authenticated():
        try:
            league = League.objects.get(players=request.user)
            players_in_league = Player.objects.filter(league=league).all()
            players_in_team = Player.objects.filter(user=request.user).all()
            context = {'players_in_league': players_in_league,
                       'players_in_team': players_in_team
                       }
            return render(request, 'trade.html', context)
        except League.DoesNotExist:
            return redirect('/profile')
    else:
        return redirect('/profile')

@csrf_exempt
def league(request):
    if request.user.is_authenticated():
        league = League.objects.filter(players=request.user)
        if league:
            try:
                league = League.objects.filter(players=request.user)[0]
                id = league.id
                return get_league_page(request, id)
            except League.DoesNotExist:
                return redirect('/profile')
        else:
            return redirect('/profile')
    else:
        return redirect('/profile')

@csrf_exempt
def create_pairings(request):
    if request.user.is_authenticated():
        user = request.user
        if request.method == 'POST':
            league = League.objects.get(players=user)
            num_pairings = league.games_in_season
            num_pairings = 7
            list_users = league.players.all()
            # print(list_users)
            # list_users = []
            # for play in league.players:
                # list_users.append(play)
            num_users = len(list_users)
            userid_list = []
            for user in list_users:
                # print(user)
                userid_list.append(user.id)
            if num_users % 2 == 1:
                userid_list.append(0)
            for times in range(0, num_pairings):
                counter = times
                if times != 0:
                    # print(userid_list)
                    userid_list = rotate_pairing(userid_list)
                    # print(userid_list)
                first_half = userid_list[:len(userid_list)/2]
                second_half = userid_list[len(userid_list)/2:]
                num_in_list = len(first_half)
                new_pairing = Match_Pairings(league = league,
                                             number = counter)
                new_pairing.save()
                # new_detail.save()
                for x in range(0, num_in_list):
                    user_one = first_half[x]
                    # print(user_one)
                    user_two = second_half[x]
                    # print(user_two)
                    if user_one == 0:
                        new_detail = User_Match_Details(match_number=counter,
                                    total_points=0,
                                    match_pairing=new_pairing,
                                    user_id = 2,
                                    bye=True           )
                        user_two = User.objects.get(id=user_two)
                        new_pairing.users.add(user_two)
                        new_pairing.save()
                        new_detail.user = user_two
                        new_detail.save()
                    elif user_two == 0:
                        new_detail = User_Match_Details(match_number=counter,
                                    total_points=0,
                                    match_pairing=new_pairing,
                                    user_id = 2,
                                    bye = True          )
                        user_one = User.objects.get(id=user_one)
                        new_pairing.users.add(user_one)
                        new_pairing.save()
                        new_detail.user = user_one
                        new_detail.save()
                    else:
                        new_detail = User_Match_Details(match_number=counter,
                                    total_points=0,
                                    match_pairing=new_pairing,
                                    user_id = 2)
                        new_detail_two = User_Match_Details(match_number=counter,
                                                    total_points=0,
                                                    match_pairing=new_pairing,
                                                    user_id=2)
                        user_one = User.objects.get(id=user_one)
                        user_two = User.objects.get(id=user_two)
                        new_pairing.users.add(user_one)
                        new_pairing.users.add(user_two)
                        new_pairing.save()
                        new_detail.user = user_one
                        # new_detail.user.add(user_two)
                        # new_detail_two.user.add(user_one)
                        new_detail_two.user = user_two
                        new_detail.save()
                        new_detail_two.save()
        return redirect('/admin')

@csrf_exempt
def rotate_pairing(list_users):
    pivot = list_users[0]
    x = np.array(list_users)
    x = np.reshape(x, (2, len(list_users)/2))
    x = np.roll(x, 1)
    new_list = list(itertools.chain.from_iterable(x))
    new_list.remove(pivot)
    new_list = [pivot] + new_list
    return new_list

def total_points(user):
    all_players = Player.objects.filter(user=user)
    sum = 0
    for player in all_players:
        sum = player.rating + sum
    return sum

@csrf_exempt
def calculate_winner(request):
    if request.user.is_authenticated():
        user = request.user
        if request.method == 'POST':
            number = request.POST.get('match_number')
            league = League.objects.filter(players=user)
            match_details = User_Match_Details.objects.filter(match_number=number)
            counter = 1
            user_one_points = 0
            user_two_points = 0
            for match in match_details:
                if match.bye == False:
                    if counter == 1:
                        user_one = match.user
                        user_one_points = total_points(user_one)
                        first_match = match
                        first_match.total_points = user_one_points
                        first_match.save()
                        counter = counter + 1
                    elif counter == 2:
                        user_two = match.user
                        user_two_points = total_points(user_two)
                        match.total_points = user_two_points
                        match.save()
                        if user_one_points > user_two_points:
                            first_match.winner = True
                            first_match.tie = False
                            first_match.save()
                            match.winner = False
                            match.tie = False
                            match.save()
                        elif user_two_points > user_one_points:
                            first_match.winner = False
                            first_match.tie = False
                            first_match.save()
                            match.winner = True
                            match.tie = False
                            match.save()
                        elif user_one_points == user_two_points:
                            first_match.winner = False
                            first_match.tie = True
                            first_match.save()
                            match.winner = False
                            match.tie = True
                            match.save()
                        counter = 1
                elif match.bye == True:
                    user = match.user
                    user_points = total_points(user)
                    match.total_points = user_points
                    match.winner = True
                    match.tie = False
                    match.save()
    return redirect('/admin')

def update_history(user):
    user_history = History.objects.filter(user=user)[0]
    matches = User_Match_Details.objects.filter(user=user)
    counter_wins = 0
    counter_losses = 0
    counter_ties = 0
    for match in matches:
        if match.winner == True:
            counter_wins = counter_wins + 1
        elif match.tie == True:
            counter_ties = counter_ties + 1
        # elif match.tie == False and match.winner == False:
        #     print('loss')
        #     counter_losses = counter_losses + 1
    # print(user_history.wins)
    user_history.wins = counter_wins
    user_history.ties = counter_ties
    user_history.save()

def update_ranking(league):
    all_players = league.players
    player_list = []
    # calculate wins and ties and losses and order the users respectively
    for players in all_players.all():
        user_history = History.objects.filter(user=players)[0]
        score = 0
        wins = user_history.wins
        # print(wins)
        ties = user_history.ties
        score = wins + 0.5 * ties
        temp = []
        temp.append(players.id)
        temp.append(score)
        player_list.append(temp)
    player_list.sort(key=lambda x: x[1])
    player_list.reverse()
    # length = len(player_list)
    counter = 0
    for lister in player_list:
        # print(lister)
        # print(counter)
        # print(lister)
        userid = lister[0]
        # print(userid)
        # print(sub_list)/
        # try:
        history = History.objects.get(user_id=userid)
        # except History.DoesNotExist:
        #     print(userid)
        #     print('hello')
        # print(history.user)
        counter = counter + 1
        history.current_ranking = counter
        history.save()

@csrf_exempt
def recent_page(request):
    if request.user.is_authenticated():
        league = League.objects.filter(players=request.user)[0]
        match_detail = Match_Pairings.objects.filter(league_id=league.id)
        detail = []
        for info in match_detail:
            # print (info.user)
            match_info = User_Match_Details.objects.filter(match_pairing=info)
            # for match_info in match_info:
            # print(match_info.user.id)
            detail.append(match_info)
        context = {'league': league,
                   'match_detail': match_detail,
                   'specific_detail': detail}
        return render(request, 'recent.html', context)

def about(request):
    if request.user.is_authenticated():
        # return redirect('/profile')
        print('logged in')
        return redirect('/profile')
    elif request.user.is_anonymous():
        print('anonymous')
        # return redirect('/profile')
        return render(request, 'about.html')