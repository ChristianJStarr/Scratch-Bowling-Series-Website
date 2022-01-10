import string
import random

from django import template
from django.contrib.auth import get_user_model
from django.utils.safestring import mark_safe

from scoreboard.models import Statistics
from tournaments.models import Tournament

register = template.Library()
User = get_user_model()



@register.simple_tag
def session_id(input):
    return '#' + ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(5))

@register.simple_tag
def web_version(input):
    return ''

@register.filter()
def badge(badge):
    diamond_icon = 'shield2'
    diamond_color = '#8AD2E2'
    gold_icon = 'shield2'
    gold_color = '#f5d442'
    silver_icon = 'shield2'
    silver_color = '#c2c2c2'
    bronze_icon = 'shield2'
    bronze_color = '#d7995b'
    icon = ''
    color = ''
    if badge == 1:
        icon = diamond_icon
        color = diamond_color
    elif badge == 2:
        icon = gold_icon
        color = gold_color
    elif badge == 3:
        icon = silver_icon
        color = silver_color
    elif badge == 4:
        icon = bronze_icon
        color = bronze_color

    output_str = '<i class="icon-' + icon + ' rank-color" style="color:' + color + ';"></i>'

    return mark_safe(output_str)


@register.inclusion_tag('snippets/basic/recentWinners.html')
def basic_recent_winners():
    # [0]tournament id
    # [1]tournament name
    # [2]tournament date
    # [3]winner id
    # [4]winner first_name
    # [5]winner last_name
    datas = []
    tournament_datas = Tournament.past_winners(10)
    for data in tournament_datas:
        datas.append([
            data.tournament.id,
            data.tournament.name,
            data.tournament.datetime,
            data.user.id,
            data.user.first_name,
            data.user.last_name,
        ])
    return {'datas': datas}


@register.inclusion_tag('snippets/basic/topRankings.html')
def basic_top_ranks():
    # [0]winner id
    # [1]winner first_name
    # [2]winner last_name
    # [3]rank badge
    # [4]user rank
    datas = []
    statistics = Statistics.get_top(10)
    for stat in statistics:
        datas.append([
            stat.user.id,
            stat.user.first_name,
            stat.user.last_name,
            stat.user.rank_badge,
            stat.user.rank_ordinal,
        ])
    return {'datas': datas}


@register.inclusion_tag('snippets/basic/bowlerOfMonth.html')
def basic_bowler_of_month():
    user = User.objects.all().first()
    return {'bom': user}


@register.inclusion_tag('snippets/basic/upcomingTournaments.html')
def basic_upcoming_tournaments():
    tournaments = Tournament.get_upcoming(10)
    return {'tournaments': tournaments}

