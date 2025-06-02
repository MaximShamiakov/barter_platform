from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from apps.ads.views import (custom_bad_request_view,
                            custom_page_not_found_view,
                            custom_permission_denied_view,
                            custom_server_error_view)

# Административная панель
admin.site.site_header = 'Barter Platform Администрирование'
admin.site.site_title = 'Barter Platform'
admin.site.index_title = 'Панель управления'

# Non-localized URLs (API, admin, media)
urlpatterns = [
    path('admin/', admin.site.urls),

    # API версии
    path('api/', include('api.urls')),

    # Internationalization
    path('i18n/', include('django.conf.urls.i18n')),
]

# Localized URLs with language prefix
urlpatterns += i18n_patterns(
    path('', include('apps.ads.urls')),
    path('users/', include('apps.users.urls')),
    prefix_default_language=True,
)

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )

    # Django Debug Toolbar URLs
    try:
        import debug_toolbar
        urlpatterns += [
            path('__debug__/', include(debug_toolbar.urls)),
        ]
    except ImportError:
        pass

# Custom error handlers
handler400 = custom_bad_request_view
handler403 = custom_permission_denied_view
handler404 = custom_page_not_found_view
handler500 = custom_server_error_view
