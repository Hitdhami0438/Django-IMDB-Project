
from django.urls import path, include
from . import views
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.routers import DefaultRouter



router = DefaultRouter()
router.register(r'list', views.WatchViewSet, basename='watchlist')
router.register(r'stream', views.streamPlatformViewSet, basename='streamplatform')
router.register(r'review', views.ReviewViewSet, basename='review')



urlpatterns = [
    # path('list/', views.movie_list.as_view(), name='watch-list'),
    # path('list/<int:pk>', views.movie_detail.as_view(), name='watchlist-detail'),
    path('list/<int:pk>/review/', views.ReviewListView.as_view(), name='review-list'),
    # path('list/review/<int:pk>', views.ReviewListView.as_view(), name='review-list'),
    path('list/<int:pk>/review-create/', views.ReviewCreate.as_view(), name='reviewcreate-list'),

    # path('stream/', views.stream_list.as_view(), name='streamplatform-detail'),
    # path('stream/<int:pk>', views.stream_detail.as_view(), name='streamplatform-detail'),

    # path('review/', views.ReviewListView.as_view(), name='review-list'),
    # path('review/<int:pk>', views.ReviewDetailView.as_view(), name='review-detail'),

    path('', include(router.urls)),

    path('', views.api_root),

]

# urlpatterns = format_suffix_patterns(urlpatterns)