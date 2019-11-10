from yokohama_api import views
from django.conf.urls import url

urlpatterns = [
    url(r'^connect/$', views.Connect.as_view()),
    url(r'^disconnect/$', views.Disconnect.as_view()),
    url(r'^info/$', views.GetInfo.as_view()),
    url(r'^metrics/$', views.GetMetrics.as_view()),
]