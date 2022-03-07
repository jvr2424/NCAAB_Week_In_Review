from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from top_teams_week import views

urlpatterns = [
    path('schedule/<int:week_number>', views.schedule),
    path('top_week_results/<int:week_number>', views.top_week_results),
    path('team_week_rankings/', views.team_week_rankings),
    path('weeks_full/', views.weeks_full),
    path('weeks_full/<int:pk>', views.weeks_full_detail),
    path('weeks/', views.weeks),
    path('weeks/<int:pk>', views.weeks_detail),
]

urlpatterns = format_suffix_patterns(urlpatterns)