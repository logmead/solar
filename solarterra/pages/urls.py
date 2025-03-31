from django.urls import path
from pages import views
from pages import search_views
import uuid

urlpatterns = [
    path('', views.main_page, name="main_page"),
 
    path('data_info', views.data_info, name="data"),
    path('data_technical/<uuid:exp_id>', views.technical_data, name="data_tech"),
    path('system_data', views.system_data, name="system_data"),
    path('logs', views.logs, name="logs"),

    path('search', search_views.search, name="search"),
    path('search/variables', search_views.variables, name="variables"),
    path('search/plot', search_views.plot, name="plot"),
]