from django.urls import path
from .views import IndexList, MainList, DetailHos, SearchList

app_name = 'infos'

urlpatterns = [
    path('', IndexList.as_view(), name='index'),
    path('list/<str:region>/', MainList.as_view(), name='list'),
    path('detail/<str:pk>/', DetailHos.as_view(), name='detail'),
    path('search/', SearchList.as_view(), name='search'),
]