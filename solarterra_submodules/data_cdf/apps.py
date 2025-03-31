from django.apps import AppConfig
import os


class DataCdfConfig(AppConfig):
    name = "data_cdf"
    path = os.path.abspath(__file__)
    verbose_name = "Solarterra Submodules"
