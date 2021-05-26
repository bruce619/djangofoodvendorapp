from django.conf import settings
from django.contrib import admin
from django.urls import path, include
import foodvendor.views.home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('', include('foodvendor.urls')),
]

#  Saves static files in static folder
if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    import debug_toolbar

    urlpatterns = urlpatterns + [
        path('__debug__/', include(debug_toolbar.urls))
    ]
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

handler404 = foodvendor.views.home.error_404
handler500 = foodvendor.views.home.error_500


