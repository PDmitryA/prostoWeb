from django.conf.urls import url

# import my views
from ask.views import helloWorld

urlpatterns = [
    url(r'^$', helloWorld, name='hello'),
]