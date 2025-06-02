from django.urls import path

from . import views

urlpatterns = [
    path('', views.ads_list, name='ads_list'),
    path('ads/create/', views.create_ad, name='create_ad'),
    path('ads/my/', views.my_ads, name='my_ads'),
    path('ads/<int:ad_id>/edit/', views.edit_ad, name='edit_ad'),
    path('ads/<int:ad_id>/delete/', views.delete_ad, name='delete_ad'),
    path('ads/create_exchange_proposal/', views.create_exchange_proposal,
         name='create_exchange_proposal'),
    path('exchange_proposals/', views.exchange_proposals_list,
         name='exchange_proposals_list'),
    path('update/<int:proposal_id>/', views.update_proposal_status,
         name='update_proposal_status'),
]
