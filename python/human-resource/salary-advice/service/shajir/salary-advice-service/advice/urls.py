from django.urls import path, include
from .views import advice


urlpatterns = [
    path('advice/', advice),
]