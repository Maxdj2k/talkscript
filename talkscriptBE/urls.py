from django.urls import path
from . import views 


urlpatterns = [
    path('openai-api-call/', views.openai_api_call, name='openai_api_call'),
]