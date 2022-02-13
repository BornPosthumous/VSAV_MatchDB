from django.urls import path
from . import views

# will be imported into main urls.py
urlpatterns = [
    path('matches/', views.save_match),
]