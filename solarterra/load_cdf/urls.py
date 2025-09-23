from django.urls import path
from load_cdf import views


urlpatterns = [
    path('', include('pages.urls')),
]
