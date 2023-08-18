from django.urls import path
from . import views
urlpatterns = [
    path('',views.home, name='home'),
    path('create/', views.create, name='create'),
    path('vote/<poll_id>/', views.vote, name='vote'),
    path('results/<poll_id>/', views.results, name='results'),
    path('search_polls', views.search_polls, name='search-polls'),
    path('update/<poll_id>/', views.update_polls, name='update'),
    path('delete/<poll_id>/', views.delete_polls, name='delete'),
    path('resultdata/<str:poll_id>/', views.resultData, name='resultdata'),
    path('my_polls', views.my_polls, name='my-polls'),
]