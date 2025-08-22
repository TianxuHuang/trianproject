from django.urls import path
from . import views

urlpatterns = [
    path('', views.draw_index, name='draw_index'),
]