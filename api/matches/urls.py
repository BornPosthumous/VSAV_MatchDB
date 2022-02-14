from django.urls import path
from . import views

# will be imported into main urls.py
urlpatterns = [
    path('save_test', views.save_test_match),
    path('get_latest/<int:number_of_matches>', views.get_last_n_matches),
    path('seed_db_from_csv', views.seed_db_from_csv),
    path('delete_all', views.delete_all_matches),
    path('char/<str:charname>', views.get_matches_by_char),
    path('mu/<str:char_1>/<str:char_2>', views.get_matchup),
    path('id/<uuid:match_uuid>', views.get_match_by_id),
    path('uploader/<str:uploader>', views.get_matches_by_uploader),
    path('url', views.get_matches_from_video),
]