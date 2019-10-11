# urls.py - App URLs Map to App Views
from django.urls import path, re_path

from systemlist import views

urlpatterns = [
    # /systemlist/  -  All Devices, All Environments (the index)
    path("", views.index, name="index"),
    # /systemlist/stats  -  All Devices, Statistics
    path("stats/", views.stats, name="stats"),
    # /systemlist/env/<env_name>  -  All Devices, Specific Environment
    path("env/<str:env_name>/", views.env, name="env"),
    # /systemlist/type/<device_type>/  - Specific Device, All Environments
    path("type/<str:device_type>/", views.type_all_env, name="type_all_env"),
    # /systemlist/type/device_type/env/env_name  -  Specific Device, Specific Environment
    path("type/<str:device_type>/env/<str:env_name>/", views.type_env, name="type_env"),
    # /systemlist/hw/<asset_hardware> - Physical or Virtual
    path("hw/<str:asset_hardware>/", views.asset_hardware, name="asset_hardware"),
]
