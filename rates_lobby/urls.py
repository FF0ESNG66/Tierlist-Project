from django.urls import path
from . import views

app_name = "rates_lobby"

urlpatterns = [
    path('', views.lobby, name='home'),
    path('about/', views.about, name='about'),
    path('templates-list/', views.templates_list_view, name='templates-list-view'),
    path('tierlist-list/', views.tierlist_list_view, name='tierlist-list-view')
]