from django.urls import path
from . import views

urlpatterns = [
    path('lti/', views.index, name='lti_launch'),
]

