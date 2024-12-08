from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.models import User
from .models import SportsEvent,BettingLine,Portfolio,Wager
from .forms import UploadFileForm
import json

# Create your views here.

def home(request):

    # Can later filter by user-specific constraints (e.g., minimum hit probability, time range)

    n_events = SportsEvent.objects.count()
    n_port = Portfolio.objects.count()

    return render(request, 'home.html', {'n_events': n_events,'n_port':n_port})

def upcoming_events(request):

    # Can later filter by user-specific constraints (e.g., minimum hit probability, time range)
    events = list(SportsEvent.objects.all().order_by('game_datetime'))

    lines = [event.best_line() for event in events]
    roi = [line.expected_roi for line in lines]
    sorted_indices = sorted(range(len(roi)), key=lambda i: -1*roi[i])
    event_line_info = [(events[i],lines[i]) for i in sorted_indices]

    return render(request, 'upcoming_events.html', {'event_line_info': event_line_info})

def betting_portfolios(request):

    # Can later filter by user-specific constraints (e.g., minimum hit probability, time range)
    portfolios = Portfolio.objects.all().order_by('created_at')

    return render(request, 'portfolios.html', {'portfolios': portfolios})

def event_info(request,pk):
    event = SportsEvent.objects.get(pk=pk)
    lines = BettingLine.objects.filter(game=event).order_by('-expected_roi')
    return render(request, 'event_info.html', {'event': event,'lines': lines})

def upload_data(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():

            json_data = json.loads(request.FILES['file'].read())
            preexisting_events = SportsEvent.objects.values_list('name', flat=True).distinct()

            for game_data in json_data:

                if game_data['game_id'] not in preexisting_events:

                    new_event_params = {'name':game_data['game_id'],
                                        'game_datetime':game_data['game_datetime'],
                                        'observation_datetime':game_data['observation_datetime'],
                                        'league':game_data['league'],
                                        'home_team':game_data['home_team'],
                                        'away_team':game_data['away_team'],
                                        'home_win_prob':game_data['home_win_prob'],
                                        'away_win_prob':game_data['away_win_prob']}

                    new_event = SportsEvent(**new_event_params)
                    new_event.save()

                    for line_data in game_data['lines']:

                        line_params = {'game':new_event,
                                       'observation_datetime':game_data['observation_datetime'],
                                       'sportsbook':line_data['sportsbook'],
                                       'side':line_data['side'],
                                       'hit_prob':line_data['hit_prob'],
                                       'odds':line_data['odds'],
                                       'expected_roi':line_data['EROI']}

                        line = BettingLine(**line_params)
                        line.save()

            return redirect('home')
    else:
        form = UploadFileForm()
    return render(request, "upload_data.html", {"form": form})
