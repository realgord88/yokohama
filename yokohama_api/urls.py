from yokohama_api import views
from django.conf.urls import url

urlpatterns = [
    url(r'^connect/$', views.Connect.as_view()),
    url(r'^disconnect/$', views.Disconnect.as_view()),
    url(r'^info/$', views.GetInfo.as_view()),
    url(r'^metrics/$', views.GetMetrics.as_view()),
    url(r'^setlenght/$', views.SetLenght.as_view()),
    url(r'^setaveraging/$', views.SetAveraging.as_view()),
    url(r'^infoslots/$', views.InfoSlots.as_view()),
    url(r'^setdate/$', views.SetDate.as_view()),
    url(r'^settime/$', views.SetTime.as_view()),
    url(r'^errors/$', views.CheckErrors.as_view()),
    url(r'^setoffset/$', views.SetOffset.as_view()),
]
