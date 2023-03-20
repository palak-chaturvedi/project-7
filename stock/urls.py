from django.conf.urls import include
from django.urls import re_path
from django.contrib import admin
from . import views

admin.autodiscover()

urlpatterns = [
    # Examples:
    # url(r'^$', 'try.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    re_path(r'^$', views.index, name='index'),
    re_path(r'^dashboard/$', views.dashboard, name='dashboard'),
    re_path(r'^reports/$', views.reports, name='reports'),
    re_path(r'^topg/$', views.topg, name='topg'),
    re_path(r'^current/$', views.current, name='current'),
    re_path(r'^today/$', views.today, name='today'),
    re_path(r'^experts$', views.experts, name='experts'),
    re_path(r'^company_reviews$', views.company_reviews, name='company_reviews'),
    re_path(r'^todays_comments$', views.todays_comments, name='todays_comments'),
    re_path(r'^try_python/$', views.try_python, name='try_python'),
    re_path(r'^graph$', views.graph, name='graph'),
]
