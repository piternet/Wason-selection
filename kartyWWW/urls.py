from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.home, name='homePage'),
    url(r'^game/(?P<sessionId>[0-9]+)$', views.game, name='game'),
    url(r'^trainingMode/$', views.trainingMode, name='trainingMode'),
    url(r'^adminPanel/$', views.adminPanel, name='adminPanel'),
    url(r'^signUp/$', views.signUp, name='signUp'),
    url(r'^gilSession/(?P<sessionId>[0-9]+)$', views.GILSession, name='gilSession'),
    url(r'^thanks/$', views.thanks, name='thanks'),
    url(r'^exportCSV/$', views.exportCSV, name='exportCSV'),
    url(r'^exportCSVPlayers/$', views.exportCSVPlayers, name='exportCSVPlayers'),
    
]