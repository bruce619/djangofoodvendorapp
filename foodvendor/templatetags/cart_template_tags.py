from django import template
from ..models import Order, MenuItem, Notification, MessageStatus, Refund
from django.db.models import Count

register = template.Library()


@register.filter
def cart_item_count(user):
    if user.is_authenticated:
        qs = Order.objects.filter(user=user, ordered=False)
        if qs.exists():
            return qs[0].itemsordered.count()
    return 0


@register.filter
def user_item_order_count(menu):
    qs = MenuItem.objects.filter(menu=menu, ordered=True).annotate(num_user=Count('user')).count()
    return qs


@register.filter
def unread_notification(user):
    qs = Notification.objects.filter(receiver=user, messagestatus=MessageStatus.objects.get(name='message sent')).annotate(num_user=Count('sender')).count()
    return qs


