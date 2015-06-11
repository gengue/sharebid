from django.conf.urls import include, url
from django.contrib import admin
from search import views

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.Home.as_view(), name='home'),
    url(r'^accounts/login/$', views.Login.as_view(), name='login'),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', name="logout"),
    
]
