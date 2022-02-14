from django.urls import path
from . import views

# will be imported into main urls.py
urlpatterns = [
    path('save_test', views.save_test_match),
    path('get_last_five', views.get_last_five_matches),
    path('seed_db_from_csv', views.seed_db_from_csv),
    path('delete_all', views.delete_all_matches)
]