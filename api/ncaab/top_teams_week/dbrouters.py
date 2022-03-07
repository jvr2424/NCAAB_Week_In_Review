from .models import Teams, Team_Week_Rankings, Team_Schedule, Weeks, TopWeekResults, Inter_WeekResults
    
class TopTeamsDBRouter:
    def db_for_read (self, model, **hints):
        if (model in [Teams, Team_Week_Rankings, Team_Schedule, Weeks, TopWeekResults, Inter_WeekResults]):
            # your model name as in settings.py/DATABASES
            return 'top_teams_db'
        return None
    
    def db_for_write (self, model, **hints):
        if (model in [Teams, Team_Week_Rankings, Team_Schedule, Weeks, TopWeekResults, Inter_WeekResults]):
            # your model name as in settings.py/DATABASES
            return 'top_teams_db'
        return None



