from django.conf import settings
from settings import pathify
from django.conf.urls.defaults import *

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',)

urlpatterns += patterns('',
  (r'^admin/doc/', include('django.contrib.admindocs.urls')),
  url(r'^admin/(.*)', admin.site.root, name="admin"),
  
  (r'^', include('flashcards.views.urls')),
)

if settings.DJANGO_SERVER:
  urlpatterns += patterns('',
    (r'^%s(?P<path>.*)$' % settings.MEDIA_URL[1:], 'django.views.static.serve',
      {'document_root': settings.MEDIA_ROOT, 'show_indexes':True}),
  )

CUSTOM_URLS_APPS = ('flashcards',)

for app in settings.APPS:
  if app not in CUSTOM_URLS_APPS and os.path.exists(pathify([settings.PROJECT_PATH, app, 'views'])):
    urlpatterns += patterns('',
      (r'^%s/' % app, include('%s.views.urls' % app)),
    )
