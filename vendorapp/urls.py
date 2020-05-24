from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from foodvendor.views import home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('accounts.urls')),
    path('', include('foodvendor.urls'))
]


