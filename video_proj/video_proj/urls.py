from django.contrib import admin
from django.urls import path,include
from video_app import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('',views.index,name ='index'),
    path('admin/', admin.site.urls),
    #path('special/', views.special,name='special'),
    path('video_app/', include('video_app.urls')),
    path('logout/', views.user_logout, name='logout'),
]+ static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)
