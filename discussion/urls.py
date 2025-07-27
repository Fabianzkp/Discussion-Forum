from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views

urlpatterns = [
    path('', views.topic_list, name='topic_list'),
    path('topic/<int:pk>/', views.topic_detail, name='topic_detail'),
    path('register/', views.register, name='register'),
    path('topic/<int:pk>/delete/', views.delete_topic, name='delete_topic'),
    path('comment/<int:pk>/delete/', views.delete_comment, name='delete_comment'),
    path('comment/<int:pk>/edit/', views.edit_comment, name='edit_comment'),
    path('comment/<int:pk>/user_delete/', views.user_delete_comment, name='user_delete_comment'),
    path('topic/<int:pk>/edit/', views.edit_topic, name='edit_topic'),
    path('topic/<int:pk>/user_delete/', views.user_delete_topic, name='user_delete_topic'),
    path('accounts/login/', LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('accounts/logout/', LogoutView.as_view(), name='logout'),
    
]