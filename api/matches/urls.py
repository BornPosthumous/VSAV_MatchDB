from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework import routers
from . import views

router = routers.SimpleRouter()
router.register(r'matches', views.MatchViewSet, 'matches')
# will be imported into main urls.py
urlpatterns = [
    path('', views.api_root),
    path('seed_db_from_csv', views.seed_db_from_csv),
    path('delete_all', views.delete_all_matches),
    path('url', views.get_matches_from_video),
    path('users/', views.UserList.as_view(), name='user-list'),
    path('users/<int:pk>/', views.UserDetail.as_view(), name='user-detail'),
]
urlpatterns = format_suffix_patterns(urlpatterns)
urlpatterns += router.urls