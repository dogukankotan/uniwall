from django.conf.urls import url
from main.views import login_view,register_view, logout_view, index_view, settings_view, create_picture, \
    create_entry, create_event, join_event

urlpatterns = [
    url(r'^login/$', login_view, name='login'),
    url(r'^register/$', register_view, name='register'),
    url(r'^logout/$',logout_view, name='logout'),
    url(r'^$', index_view, name='index'),
    url(r'^settings/$', settings_view, name='settings'),
    url(r'^picture/$', create_picture, name='picture'),
    url(r'^entry/$', create_entry, name='entry'),
    url(r'^event/$', create_event, name='event'),
    url(r'^join_event/(?P<event_id>.+?)/$', join_event, name='join_event'),
]