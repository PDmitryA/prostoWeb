from django.conf.urls import url

# import my views
from questions.views import *

app_name = 'questions'

urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^answer/(?P<qid>\d+)/$', answer, name='answer'),
    url(r'^login/$', login, name='login'),
    url(r'^new/$', newQuestion, name='newQuestion'),
    url(r'^signup/$', register, name='register'),
    url(r'^settings/$', settings, name='settings'),
    url(r'^tag/(?P<findTag>\w+)/$', tagged, name='tagged'),
    url(r'^hot/$', hot, name='hot'),
    url(r'^logout/$', logout, name='logout')
]