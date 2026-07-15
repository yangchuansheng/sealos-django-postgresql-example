from django.urls import path

from practice.views import create_item, read_item


urlpatterns = [
    path('items/', create_item, name='create_item'),
    path('items/<int:item_id>/', read_item, name='read_item'),
]
