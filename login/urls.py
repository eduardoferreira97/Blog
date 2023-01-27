from django.urls import path

from . import views

app_name = 'login'

urlpatterns = [
    path('registro/', views.register_view, name="register"),
    path('registro/criar/', views.register_create, name="register_create"),
    path('login/', views.login_view, name="login"),
    path('login/criar/', views.login_create, name="login_create"),
    path('logout/', views.logout_view, name="logout"),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
]
