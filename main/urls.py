from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("login/", views.login, name="login"),
    path("signup/", views.signup, name="signup"),
    path("logout/", views.logout, name="logout"),
    path("createsheet/", views.createsheet, name="createsheet"),
    path('get_topics/', views.get_topics, name='get_topics'),
    path('get_subtopics/', views.get_subtopics, name='get_subtopics'),
    path('viewsheet/<int:sheet_id>/', views.viewsheet, name='viewsheet'),
    path('sheet/<int:sheet_id>/toggle-like/', views.toggle_like, name='toggle_like'),
    path('editsheet/<int:sheet_id>/', views.editsheet, name='editsheet'),
]