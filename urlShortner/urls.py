from django.urls import path
from . import views

app_name = 'urlShortner'

urlpatterns = \
    [
        path('tiny-url', views.get_tiny_url, name='get_tiny_url'),
        path('long-url', views.get_long_url, name='get_long_url')
    ]
