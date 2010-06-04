from django.conf.urls.defaults import *
from flashcards.views import main

urlpatterns = patterns('',
    url(r'^$', main.play, name="play"),
    
    url(r'^id/(?P<id>[\d]+)$', main.flashcard_by_id, name="flashcard_by_id"),
    url(r'^w/(?P<word>[^/]+)/$', main.flashcard_by_word, name="flashcard_by_word"),
    
    url(r'^right/(?P<id>[\d]+)$', main.right, name="right"),
    url(r'^wrong/(?P<id>[\d]+)$', main.wrong, name="wrong"),
)
