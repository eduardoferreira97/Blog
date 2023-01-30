from django.urls import path

from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.index, name="index"),
    path('detalhes/<int:pk>/<slug:slug>', views.detail, name="details"),
    path('post/novo/', views.post, name="new_post"),
    path('editar/post/<int:pk>', views.edit, name="edit"),
    path('filter/<int:pk>/<str:username>', views.filter, name="filter"),
    path('search/', views.search, name="search"),
    path('delete/<int:pk>', views.delete, name="delete_post"),
    path('contato/', views.contato, name="contato"),
]
