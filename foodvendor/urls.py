from django.urls import path, include
from django.conf.urls.static import static

from .views import *

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('create-menu/', MenuCreateView.as_view(), name='create-menu'),
    path('menu/<int:id>/update/', MenuUpdateView.as_view(), name='menu-update'),
    path('menu/<int:pk>/delete/', MenuDeleteView.as_view(), name='menu-delete'),
    path('menu-list/', MenuListView.as_view(), name='menus'),
    path('menu/<int:id>/', MenuDetailsView.as_view(), name='menu-detail'),
    path('add-to-cart/<int:id>/', add_to_cart, name='add-to-cart'),
    path('remove-from-cart/<int:id>/', remove_from_cart, name='remove-from-cart'),
    path('remove-menu-from-cart/<int:id>/', remove_single_item_from_cart, name='remove-single-item-from-cart'),
    path('order-summary/', OrderSummaryView.as_view(), name='order-summary'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('payment/<payment_option>/', PaymentView.as_view(), name='payment'),
    path('request-refund/', RequestRefundView.as_view(), name='request-refund'),
    path('ordered-items/', OrderViewList.as_view(), name='ordered-items'),
    path('vendor/dashboard/', include([
            path('', DashboardView.as_view(), name='vendor-dashboard'),
            path('all-customers/<int:id>/', CustomersListView.as_view(), name='all-customers'),
        ])),
    path('send-notification/<int:id>/', send_notification, name='send-notification'),
    path('reply-notification/<int:id>/', reply_message, name='reply-notification'),
    path('notifications/', NotificationView.as_view(), name='notifications'),
    path('mark-as-read/<int:id>/', mark_as_read, name='mark-as-read')
]

#  Saves static files in static folder
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
#  Saves media files in media folder
if settings.DEBUG:
   urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

