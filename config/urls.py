from django.urls import include, path

from practice.views import health


urlpatterns = [
    path('health/', health, name='health'),
    path('', include('practice.urls')),
]
