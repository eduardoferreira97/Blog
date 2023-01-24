from django.urls import path

from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.index, name="index"),
    path('detail/<int:pk>/<slug:slug>', views.detail, name="details"),
    path('post/novo/', views.post, name="new_post"),
    path('edit/post/<int:pk>', views.edit, name="edit"),
    path('filter/<int:pk>/<str:username>', views.filter, name="filter")
]
