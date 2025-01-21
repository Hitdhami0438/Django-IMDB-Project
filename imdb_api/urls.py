
from django.urls import path, include
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('list/', views.movie_list.as_view(), name='watchlist-detail'),
    path('list/<int:pk>', views.movie_detail.as_view(), name='watchlist-detail'),
    path('stream/', views.stream_list.as_view(), name='streamplatform-detail'),
    path('stream/<int:pk>', views.stream_detail.as_view(), name='streamplatform-detail'),
    path('', views.api_root),

]

urlpatterns = format_suffix_patterns(urlpatterns)