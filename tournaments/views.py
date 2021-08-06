import json
import uuid
from urllib.request import urlopen
from bs4 import BeautifulSoup
from dal import autocomplete
from datetime import datetime
from uuid import UUID
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.defaulttags import register
from centers.models import Center
from accounts.forms import User
from oils.oil_pattern import update_oil_pattern_library, get_oil_display_data
from tournaments.forms import CreateTournament, ModifyTournament, TournamentDataRow
from tournaments.models import Tournament
from oils.oil_pattern_scraper import get_oil_colors
from tournaments.tournament_scraper import scrape_tournaments, scrape_bowlers


@register.filter
def get_center_data(value):
    if validate_uuid4(value):
        center = get_object_or_404(Center, center_id=value)
        if center is not None:
            centers_string = center.location_city + center.location_state
            return centers_string

@register.filter
def placer(value):
    return value.text

@register.filter
def firstplace(tournament):
    placements = get_placements(tournament)
    return placements[0].user_id

@register.filter
def get_bowler_from_place(tournament, place):
    placements = get_placements(tournament)
    if placements is None:
        return None
    for placement in placements:
        if placement.place == place:
            return placement.user_id
    return None

@register.filter
def qualifyings(tournament):
    qualifyings = get_qualifying_object(tournament)
    return qualifyings

@register.filter
def qualifying(tournament):
    qualifying = get_qualifying(tournament)
    if qualifying is None:
        return None
    data = []
    for qual in qualifying:
        uu = is_valid_uuid(qual[1])
        if uu is not None:
            place = 'DNF'
            try:
                place = int(qual[0])
            except TypeError:
                print(qual[0])
                place = 'DNF'
            name = User.objects.get(user_id=uu)
            name = name.first_name + ' <span>' + name.last_name + '</span>'
            link = str(uu)
            total = 0
            scores = []
            for x in range(2, len(qual) - 1):
                score = 0
                try:
                    score = int(qual[x])
                except TypeError:
                    score = 0
                scores.append(score)
                total = total + score
            data.append([place, name, scores, total, link])
    return data

@register.filter
def winner(tournament):
    matchplay = get_matchplay(tournament)
    if matchplay is None:
        return None
    data = []
    for qual in matchplay:
        if qual is None or qual[1] is None or qual[0] is None:
            continue
        uu = is_valid_uuid(qual[1])
        if uu is not None:
            place = int(qual[0])
            if place == 1:
                return str(uu)

@register.filter
def getaverage(uuid, tournament):
    qualifying = get_qualifying(tournament)
    if qualifying is None:
        return None
    totalscore = 0
    amount = 0
    for qual in qualifying:
        uu = is_valid_uuid(qual[1])
        if uu is not None and str(uu) == str(uuid):
            for x in range(2, len(qual) - 1):
                score = int(qual[x])
                totalscore = totalscore + score
                amount = amount + 1
            avg = totalscore / amount
            avg = '{:0.1f}'.format(avg)
            return avg

@register.filter
def participants(tournament):
    qualifying = get_qualifying(tournament)
    if qualifying is None:
        return 0
    return len(qualifying)

@register.filter
def bowler_name(uuid, bold_last=False):
    uuid = is_valid_uuid(uuid)
    if uuid is not None:
        name = User.objects.get(user_id=uuid)
        truncate = False
        if truncate is True:
            if bold_last is True:
                return name.first_name + '&nbsp;<span class="bold">' + name.last_name[0] + '.</span>'
            else:
                return name.first_name + ' ' + name.last_name[0] + '.'
        else:
            if bold_last is True:
                return name.first_name + '&nbsp;<span class="bold">' + name.last_name + '</span>'
            else:
                return name.first_name + ' ' + name.last_name

@register.filter
def bowler_location(uuid):
    uuid = is_valid_uuid(uuid)
    if uuid is not None:
        user = User.objects.get(user_id=uuid)
        if user.location_city is '':
            return ''
        else:
            return '(' + user.location_city + ' ' + user.location_state + ')'


@register.filter
def tournament_date(tournament_id):
    tournament_id = is_valid_uuid(tournament_id)
    if tournament_id is not None:
        tournament = Tournament.objects.filter(tournament_id=tournament_id).first()
        if tournament is not None:
            return tournament.tournament_date


@register.filter
def tournament_name(tournament_id):
    tournament_id = is_valid_uuid(tournament_id)
    if tournament_id is not None:
        tournament = Tournament.objects.filter(tournament_id=tournament_id).first()
        if tournament is not None:
            return tournament.tournament_name


@register.filter
def ordinal(value):
    return make_ordinal(value)


class Qualifying:
    user_id = None;
    place = 0
    scores = 0

class MatchPlay:
    user_id = None
    place = 0
    scores = 0


def get_placements(tournament):
    qualifyings = get_qualifying_object(tournament)
    if qualifyings is None:
        return None
    match_plays = get_matchplay_object(tournament)
    if match_plays is None:
        return None

    for match_play in match_plays:
        qualifying = qualifyings[match_play.place - 1]
        qualifying.place = match_play.place
        qualifying.scores += match_play.scores
    return qualifyings


def get_qualifying_object(tournament):
    import_data = tournament.qualifiers.replace("'", '"')
    try:
        import_data = json.loads(import_data)
    except ValueError:
        return None
    if import_data is None:
        return None

    qualifyings = []
    for data in import_data:
        user_id = is_valid_uuid(data[1])
        if user_id is not None:
            qualifying = Qualifying()
            qualifying.user_id = user_id
            # set place
            qualifying.place = 0
            try:
                qualifying.place = int(data[0])
            except TypeError:
                qualifying.place = 0

            # set scores
            qualifying.scores = []
            for x in range(2, len(data) - 1):
                score = 0
                try:
                    score = int(data[x])
                except TypeError:
                    score = 0
                qualifying.scores.append(score)
            qualifyings.append(qualifying)
    return qualifyings


def get_matchplay_object(tournament):
    import_data = tournament.matchplay.replace("'", '"')
    try:
        import_data = json.loads(import_data)
    except ValueError:
        return None
    if import_data is None:
        return None

    matchplays = []
    for data in import_data:
        user_id = is_valid_uuid(data[1])
        if user_id is not None:
            matchplay = MatchPlay()
            matchplay.user_id = user_id
            # set place
            matchplay.place = 0
            try:
                matchplay.place = int(data[0])
            except TypeError:
                matchplay.place = 0

            # set scores
            matchplay.scores = []
            for x in range(2, len(data) - 1):
                score = 0
                try:
                    score = int(data[x])
                except TypeError:
                    score = 0
                qualifying.scores.append(score)
            matchplays.append(matchplay)
    return matchplays




def get_qualifying(tournament):
    qualifying = tournament.qualifiers.replace("'", '"')
    try:
        return json.loads(qualifying)
    except ValueError:
        return None


def get_matchplay(tournament):
    matchplay = tournament.matchplay.replace("'", '"')
    try:
        return json.loads(matchplay)
    except ValueError:
        return None



def is_valid_uuid(val):
    try:
        return uuid.UUID(str(val))
    except ValueError:
        return None


def make_ordinal(n):
    n = int(n)
    if n == 0:
        return '0'
    suffix = ['th', 'st', 'nd', 'rd', 'th'][min(n % 10, 4)]
    if 11 <= (n % 100) <= 13:
        suffix = 'th'
    return str(n) + suffix


def tournaments_results_views(request):
    selected_upcoming = False
    tournaments_past = Tournament.objects.filter(tournament_date__lte=datetime.now().date()).exclude(tournament_date=datetime.now().date(), tournament_time__gt=datetime.now().time())
    return render(request, 'tournaments/main-tournaments.html', {'nbar': 'tournaments', 'tournaments_past': tournaments_past, 'selected_upcoming':selected_upcoming})


def tournaments_upcoming_views(request):

    selected_upcoming = True
    tournaments_upcoming = Tournament.objects.filter(tournament_date__gte=datetime.now().date()).exclude(tournament_date=datetime.now().date(), tournament_time__lt=datetime.now().time())
    return render(request, 'tournaments/main-tournaments.html', {'nbar': 'tournaments', 'tournaments_upcoming': tournaments_upcoming, 'selected_upcoming':selected_upcoming})


def tournaments_view_views(request, id):
    tournament = Tournament.objects.get(tournament_id=id)

    oil_pattern = get_oil_display_data(879)
    oil_colors = get_oil_colors()

    return render(request, 'tournaments/view-tournament.html', {'nbar': 'tournaments', 'tournament': tournament, 'oil_pattern': oil_pattern, 'oil_colors': oil_colors})


def get_oil():
    return scrape_oil(1)





def tournaments_modify_views(request, id):
    if request.user.admin is True and validate_uuid4(id) is True:
        tournament = get_object_or_404(Tournament, tournament_id=id)
        if tournament is None:
            redirect('/')
        if request.method == 'POST':
            form = ModifyTournament(request.POST)
            if form.is_valid():
                testform = TournamentDataRow(request.POST)

                tournament.tournament_name = form.cleaned_data.get('tournament_name')
                tournament.tournament_description = form.cleaned_data.get('tournament_description')
                tournament.entry_fee = form.cleaned_data.get('entry_fee')
                tournament.total_games = form.cleaned_data.get('total_games')
                tournament.tournament_date = form.cleaned_data.get('tournament_date')
                tournament.tournament_time = form.cleaned_data.get('tournament_time')
                tournament.sponsor_image = '/media/sponsors/sponsor-image-03.png'
                tournament.save(force_update=True)
                if tournament.tournament_id != id:
                    return redirect('/')
                return redirect('/tournaments/')
        else:
            testform = TournamentDataRow()
            form = ModifyTournament(initial={'tournament_name': tournament.tournament_name,'tournament_description': tournament.tournament_description,'entry_fee': tournament.entry_fee,'total_games': tournament.total_games, 'tournament_date': tournament.tournament_date.strftime('%d-%m-%Y'), 'tournament_time': tournament.tournament_time})
        return render(request, 'tournaments/modify-tournament.html', {'nbar': 'tournaments', 'form': form, 'tournament': tournament, 'testform':testform})
    else:
        return redirect('/')


def validate_uuid4(uuid_string):

    try:
        val = UUID(uuid_string, version=4)
    except ValueError:
        # If it's a value error, then the string
        # is not a valid hex code for a UUID.
        return False

    return True


def tournaments_create_views(request):
    if request.method == 'POST':
        form = CreateTournament(request.POST)
        if form.is_valid():
            tournament = Tournament.objects.create()
            tournament.tournament_name = form.cleaned_data.get('tournament_name')
            tournament.tournament_description = form.cleaned_data.get('tournament_description')
            tournament.tournament_date = form.cleaned_data.get('tournament_date')
            tournament.tournament_time = form.cleaned_data.get('tournament_time')
            tournament.save()
            return redirect('/tournaments/view/' + str(tournament.tournament_id))
    else:
        form = CreateTournament()

    return render(request, 'tournaments/create-tournament.html', {'form': form, 'nbar': 'tournaments'})


def get_date_time(date, time):
    if date is not None and time is not None:
        date_str = date + ' ' + time
        return datetime.datetime.strptime(date_str, "%Y-%m-%d %H:%M")
    else:
        return datetime.now()


def get_place(tournament_uuid, user):
    place = 0
    tournament = get_tournament(tournament_uuid)
    if tournament is not None and user is not None:
        qualifying = tournament.qualifiers.replace("'", '"')
        try:
            qualifying = json.loads(qualifying)
        except ValueError:
            return 0
        for qual in qualifying:
            uu = is_valid_uuid(qual[1])
            if uu is not None and uu == user.user_id:
                place = qual[0]
    return make_ordinal(place)


def get_tournament(uuid):
    return Tournament.objects.filter(tournament_id=uuid).first()


class BowlerAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated:
            return User.objects.none()

        qs = User.objects.all()

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs


def scrape_old_site():

    names = []
    page = 1
    for x in range(1, 39):
        with urlopen('https://www.scratchbowling.com/tournament-results?page=' + str(x)) as response:
            soup = BeautifulSoup(response, 'html.parser')
            names.extend(soup.find_all(class_='field field--name-title field--type-string field--label-hidden'))
    return names


def scraper_views(request):
    return HttpResponse(scrape_tournaments())


def scraper_bowlers_views(request):
    return HttpResponse(scrape_bowlers())













