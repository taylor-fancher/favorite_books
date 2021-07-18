from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('create_user', views.create_user),
    path('login', views.login),
    path('logout', views.logout),
    path('dashboard', views.dashboard),
    path('create_book', views.create_book),
    path('book/<int:id>', views.one_book),
    path('book/<int:id>/edit', views.edit_book),
    path('edit', views.edit),
    path('book/<int:id>/favorite', views.favorite),
    path('book/<int:id>/delete', views.delete),
    path('your_favorites', views.your_favorites),
    path('book/<int:id>/unfavorite', views.unfavorite)
]