from django.urls import path
from . import views
from .views import VideoListView,VideoDetailView,VideoUpdateView

app_name ='video_app'

urlpatterns = [
    path('register/',views.register,name='register'),
    path('user_login',views.user_login,name='user_login'),
    path('videos/',views.showvideo,name='video'),
    path('videoslist',VideoListView.as_view(),name='videolist'),
    path('<int:pk>/',views.VideoDetailView.as_view(),name='detail'),
    path('update/<int:pk>/',views.VideoUpdateView.as_view(),name='update'),
]
