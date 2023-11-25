from django.urls import path
from . import views

app_name = "rates_lobby"

urlpatterns = [
    path('', views.lobby, name='home'),
    path('about/', views.about, name='about'),
    path('templates-list/', views.templates_list_view, name='templates-list-view'),
    path('tierlist-list/', views.tierlist_list_view, name='tierlist-list-view'),
    path('tierlist-list/view/<str:tierlist_name>', views.tierlist_single_view, name='tierlist-single'),
    path('tierlist-list/view/<str:tierlist_name>/statistics', views.tierlist_single_view_statistics, name='statistics'),
]