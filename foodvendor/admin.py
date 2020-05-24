from django.contrib import admin
from .models import Menu, MenuItem, Order, OrderStatus, Notification, MessageStatus, Address, Payment, Refund
from accounts.models import User


def make_refund_accepted(modeladmin, request, queryset):
    queryset.update(refund_requested=False, refund_granted=True)


make_refund_accepted.short_description = 'Update orders to refund granted'


class MenuAdmin(admin.ModelAdmin):
    list_display = ('vendor', 'name', 'price', 'discount_price', 'isrecurring', 'datetimecreated')
    search_fields = ('vendor', 'name',)
    readonly_fields = ('datetimecreated',)

    filter_horizontal = ()
    list_filter = ()
    ordering = ('vendor',)

    fieldsets = (
        (None,
         {'fields': ('vendor',)}),
        ('Food info', {'fields': ('name', 'description', 'price', 'discount_price', 'datetimecreated')}),
        ('Frequency', {'fields': ('isrecurring', 'frequencyofrecurrence',)}),
    )


class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('user', 'menu', 'quantity', 'ordered')
    search_fields = ('user', 'menu',)
    readonly_fields = ()

    filter_horizontal = ()
    list_filter = ()
    ordering = ('user',)

    fieldsets = (
        (None,
         {'fields': ('user',)}),
        ('info', {'fields': ('menu', 'quantity')}),
        ('Ordered', {'fields': ('ordered',)}),
    )


class OrderAdmin(admin.ModelAdmin):
    list_display = ['user',
                    'ordered',
                    'shipping_address',
                    'billing_address',
                    'payment',
                    ]
    list_display_links = [
        'user',
        'shipping_address',
        'billing_address',
        'payment'
    ]
    list_filter = ['ordered']

    search_fields = [
        'user',
        'ref_code'
    ]
    actions = [make_refund_accepted]


class AddressAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'street_address',
        'apartment_address',
        'country',
        'zip',
        'address_type',
        'default'
    ]
    list_filter = ['default', 'address_type', 'country']
    search_fields = ['user', 'street_address', 'apartment_address', 'zip']


admin.site.register(Menu, MenuAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(MenuItem, MenuItemAdmin)
admin.site.register(OrderStatus)
admin.site.register(Address, AddressAdmin)
admin.site.register(Payment)
admin.site.register(Refund)
admin.site.register(Notification)
admin.site.register(MessageStatus)
