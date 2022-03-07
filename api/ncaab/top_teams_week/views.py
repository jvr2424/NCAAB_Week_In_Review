

# Create your views here.
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from top_teams_week.models import Teams, Team_Week_Rankings, Team_Schedule, Weeks, TopWeekResults
from top_teams_week.serializers import TeamsSerializer, Team_Week_RankingsSerializer, Team_ScheduleSerializer, WeeksBasicSerializer, WeeksFullSerializer, TopWeekResultsSerializer


@api_view(['GET'])
def top_week_results(request, week_number):
    ''' LIST all joined results for a specific week'''
    if request.method == 'GET':
        weeks_exists = len(Weeks.objects.filter(week_number=week_number)) > 0

        if weeks_exists:
            query = f""" SELECT 1 as id,
            t.espn_team_id,
            t.team_name as team_name,
            ts.opponent_espn_team_id,
            opp_t.team_name as opponent_team_name,
            ts.game_date,
            ts.final_score,
            ts.opponent_final_score,
            ts.is_win,
            ts.is_home,
            ts.is_neutral_court,
            ts.is_overtime,
            ts.cancelled_or_postponed,
            ts.game_time,
            ts.tv,
            w.week_number,
            w.start_date_inclusive,
            w.end_date_exclusive,
            w.is_current_week,
            twr.ranking,
            opp_twr.ranking as opponent_ranking,
            t.logo_url,
            opp_t.logo_url as opponent_logo_url

            FROM team_schedule as ts

            LEFT JOIN teams as t 
            ON t.espn_team_id = ts.espn_team_id

            LEFT JOIN teams as opp_t
            on opp_t.espn_team_id = ts.opponent_espn_team_id

                
            LEFT JOIN weeks as w
            ON ts.game_date >= w.start_date_inclusive and ts.game_date < end_date_exclusive
            

            LEFT JOIN team_week_rankings as twr
            on w.week_number = twr.week_number and 
            ts.espn_team_id = twr.espn_team_id

            LEFT JOIN team_week_rankings as opp_twr
            on w.week_number = opp_twr.week_number and 
            ts.opponent_espn_team_id = opp_twr.espn_team_id

            WHERE w.week_number={week_number} and
                  twr.ranking is not null

            ORDER BY twr.ranking
            """

            serializer = TopWeekResultsSerializer(TopWeekResults.objects.raw(query), many=True)
            return Response(serializer.data)





@api_view(['GET'])
def team_week_rankings(request):
    """
    List all team_week_rankings
    """
    if request.method == 'GET':
        rankings = Team_Week_Rankings.objects.all()
        serializer = Team_Week_RankingsSerializer(rankings, many=True)
        return Response(serializer.data)


@api_view(['GET'])
def schedule(request, week_number):
    """
    List shedule for a given week number
    Team_Schedule
    Team_ScheduleSerializer
    """
    if request.method == 'GET':
        serializer = Team_ScheduleSerializer(Team_Schedule.objects.filter(week=week_number), many=True)
        return Response(serializer.data)


@api_view(['GET'])
def weeks(request):
    """
    List all weeks
    """
    if request.method == 'GET':
        serializer = WeeksBasicSerializer(Weeks.objects.all(), many=True)
        return Response(serializer.data)


@api_view(['GET'])
def weeks_detail(request, pk):
    """
    List all weeks
    """
    if request.method == 'GET':
        serializer = WeeksBasicSerializer(Weeks.objects.get(pk=pk), many=True)
        return Response(serializer.data)



@api_view(['GET'])
def weeks_full(request):
    """
    List all weeks
    """
    if request.method == 'GET':
        serializer = WeeksFullSerializer(Weeks.objects.all(), many=True)
        return Response(serializer.data)


@api_view(['GET'])
def weeks_full_detail(request, pk):
    """
    List all weeks
    """
    if request.method == 'GET':
        serializer = WeeksFullSerializer(Weeks.objects.get(pk=pk))
        return Response(serializer.data)