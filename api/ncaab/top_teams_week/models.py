from django.db import models

# Create your models here.
# DB Structure

## Tables and Column    
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

class Teams(models.Model):
    espn_team_id = models.IntegerField(primary_key=True)
    team_name = models.CharField(max_length=200)
    logo_url = models.TextField(null=True)
    team_page_url = models.TextField(null=True)

    class Meta:
        managed=False
        db_table = 'teams'


# - Weeks
#     - week_number
#     - start_date_inclusive
#     - end_date_exclusive
#     - is_current_week
class Weeks(models.Model):
    week_number = models.IntegerField(primary_key=True)
    start_date_inclusive = models.DateField()
    end_date_exclusive = models.DateField()
    is_current_week = models.BooleanField(default=False)

    class Meta:
        managed=False
        db_table = 'weeks'

# - Team_Week_Rankings
#     - espn_team_id
#     - week_number
#     - ranking
class Team_Week_Rankings(models.Model):
    id = models.IntegerField(primary_key=True)
    espn_team = models.ForeignKey(Teams, on_delete=models.DO_NOTHING, blank=True, null=True, db_column='espn_team_id')
    week = models.ForeignKey(Weeks, on_delete=models.DO_NOTHING, blank=True, null=True, db_column='week_number')
    ranking = models.IntegerField(blank=True, null=True)

    class Meta:
        managed=False
        db_table = 'team_week_rankings'


 # - Team_Schedule
#     - espn_team_id
#     - opponent_espn_team_id
#     - game_date
#     - is_home
#     - is_neutral_court
#     - is_win
#     - final_score
#     - is_overtime
#     - opponent_final_score
#     - game_time
#     - tv
#     - cancelled_or_postponed
    
class Team_Schedule(models.Model):
    class Meta:
        managed=False
        db_table = 'team_schedule'
        unique_together = (('espn_team_id', 'game_date'),)
    
    id = models.IntegerField(primary_key=True)
    espn_team = models.ForeignKey(Teams, on_delete=models.DO_NOTHING, related_name='espn_team')
    opponent_espn_team = models.ForeignKey(Teams, on_delete=models.DO_NOTHING,  related_name='opponent_espn_team')
    game_date = models.DateField()
    week = models.ForeignKey(Weeks, on_delete=models.DO_NOTHING, db_column='week_number')
    week_ranking = models.ForeignKey(Team_Week_Rankings,on_delete=models.DO_NOTHING,  null=True, db_column='team_week_rankings_id')
    opponent_week_ranking = models.ForeignKey(Team_Week_Rankings,on_delete=models.DO_NOTHING,  null=True,related_name='opponent_team_schedule', db_column='opponent_team_week_rankings_id')
    final_score = models.IntegerField(null=True)
    opponent_final_score = models.IntegerField(null=True)
    is_win = models.BooleanField(default=False, null=True)
    is_home = models.BooleanField(default=False, null=True)
    is_neutral_court = models.BooleanField(default=False, null=True)
    is_overtime = models.BooleanField(default=False, null=True)
    cancelled_or_postponed = models.BooleanField(null=True)
    game_time = models.CharField(max_length=200, null=True)
    tv = models.CharField(max_length=200, null=True)
    


class Inter_WeekResults(models.Model):
    class Meta:
        managed=False
        #unique_together = (('espn_team_id', 'opponent_espn_team_id','week_number', 'game_date' ),)

    espn_team = models.ForeignKey(Teams, on_delete=models.CASCADE)
    week = models.ForeignKey(Weeks, on_delete=models.CASCADE)
    ranking = models.IntegerField()
    schedule = models.ForeignKey(Team_Schedule, on_delete=models.CASCADE)
    
    

    


class TopWeekResults(models.Model):
    class Meta:
        managed=False
        unique_together = (('espn_team_id', 'opponent_espn_team_id','week_number', 'game_date' ),)

    espn_team_id = models.IntegerField()
    team_name = models.CharField(max_length=200)
    opponent_espn_team_id = models.IntegerField()
    opponent_team_name = models.CharField(max_length=200)
    game_date = models.CharField(max_length=200)
    final_score = models.IntegerField(null=True)
    opponent_final_score = models.IntegerField(null=True)
    is_win = models.BooleanField(default=False, null=True)
    is_home = models.BooleanField(default=False, null=True)
    is_neutral_court = models.BooleanField(default=False, null=True)
    is_overtime = models.BooleanField(default=False, null=True)
    cancelled_or_postponed = models.BooleanField(null=True)
    game_time = models.CharField(max_length=200, null=True)
    tv = models.CharField(max_length=200, null=True)
    week_number = models.IntegerField()
    start_date_inclusive = models.CharField(max_length=200)
    end_date_exclusive = models.CharField(max_length=200)
    is_current_week = models.BooleanField(default=False)
    ranking = models.IntegerField()
    opponent_ranking = models.IntegerField()
    logo_url = models.TextField(null=True)
    opponent_logo_url = models.TextField(null=True)








# #DATE_FORMAT(date,'%Y-%m-%d')