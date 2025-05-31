from django.contrib import admin
from django.urls import path, include
from ads.views import custom_permission_denied_view, custom_page_not_found_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('ads.urls')),
    path('api/', include('ads.urls_api'))
]

handler403 = custom_permission_denied_view
handler404 = custom_page_not_found_view