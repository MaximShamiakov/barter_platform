from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
     path('register/', views.register, name='register'),
     path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
     path('logout/', auth_views.LogoutView.as_view(), name='logout'),
     path('password-reset/', 
          auth_views.PasswordResetView.as_view(template_name='users/password_reset.html'), 
          name='password_reset'),
     path('password-reset/done/', 
          auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'), 
          name='password_reset_done'),
     path('password-reset-confirm/<uidb64>/<token>/', 
          auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'), 
          name='password_reset_confirm'),
     path('password-reset-complete/', 
          auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'), 
          name='password_reset_complete'),
     path('', views.ads_list, name='ads_list'),
     path('ads/create/', views.create_ad, name='create_ad'),
     path('ads/my/', views.my_ads, name='my_ads'),
     path('ads/<int:ad_id>/edit/', views.edit_ad, name='edit_ad'),
     path('ads/<int:ad_id>/delete/', views.delete_ad, name='delete_ad'),
     path('ads/create_exchange_proposal/', views.create_exchange_proposal, name='create_exchange_proposal'),
     path('exchange_proposals/', views.exchange_proposals_list, name='exchange_proposals_list'),
]
