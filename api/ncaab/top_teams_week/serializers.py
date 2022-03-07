from .models import Teams, Team_Week_Rankings, Team_Schedule, Weeks, TopWeekResults
from rest_framework import serializers

# - Teams
#     - espn_team_id
#     - team_name
#     - logo_url
#     - team_page_url 
# - Team_Week_Rankings
#     - espn_team_id
#     - week_number
#     - ranking
# - Team_Schedule
#     - espn_team_id
#     - opponent_espn_team_id
#     - game_date
#     - is_home
#     - is_neutral_court
#     - is_win
#     - is_overtime
#     - final_score
#     - opponent_final_score
#     - game_time
#     - tv
#     - cancelled_or_postponed
# - Weeks
#     - week_number
#     - start_date_inclusive
#     - end_date_exclusive
#     - is_current_week

class WeeksBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Weeks
        fields = ['week_number','start_date_inclusive','end_date_exclusive','is_current_week']


class TeamsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teams
        fields = ['espn_team_id','team_name','logo_url','team_page_url']

class Team_ScheduleSerializer(serializers.ModelSerializer):
    espn_team = TeamsSerializer(many=False, read_only=True)
    opponent_espn_team = TeamsSerializer(many=False, read_only=True)
    week   =   WeeksBasicSerializer(many=False, read_only=True)
    opponent_week_ranking = serializers.SlugRelatedField(many=False, read_only=True, slug_field='ranking')

    class Meta:
        model = Team_Schedule
        fields = ['espn_team','opponent_espn_team','game_date', 'week', 'opponent_week_ranking','is_home','is_neutral_court','is_win','final_score', 'is_overtime', 'opponent_final_score','game_time','tv','cancelled_or_postponed']

class Team_Week_RankingsSerializer(serializers.ModelSerializer):
    espn_team = TeamsSerializer(many=False, read_only=True)
    schedule = Team_ScheduleSerializer(read_only=True, many=True, source= 'team_schedule_set')
    week_number = WeeksBasicSerializer(many=False, read_only=True)
    class Meta:
        model = Team_Week_Rankings
        fields = ['espn_team','week_number','ranking', 'schedule']

class WeeksFullSerializer(serializers.ModelSerializer):
    rankings = Team_Week_RankingsSerializer(read_only=True, many=True, source= 'team_week_rankings_set')
    class Meta:
        model = Weeks
        fields = ['week_number','start_date_inclusive','end_date_exclusive','is_current_week', 'rankings']








class TopWeekResultsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TopWeekResults
        fields = ['id', 'espn_team_id', 'team_name', 'opponent_espn_team_id', 'opponent_team_name', 'game_date', 'final_score', 'opponent_final_score', 'is_win', 'is_home', 'is_neutral_court', 'is_overtime', 
        'cancelled_or_postponed', 'game_time', 'tv', 'week_number', 'start_date_inclusive', 'end_date_exclusive', 'is_current_week', 'ranking',  'opponent_ranking','logo_url', 'opponent_logo_url']


