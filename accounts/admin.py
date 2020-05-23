from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Vendor, Customer


class AccountAdmin(UserAdmin):
    list_display = ('first_name', 'last_name', 'email', 'phonenumber', 'datetimecreated', 'last_login', 'is_vendor', 'is_customer', 'is_admin', 'is_staff')
    search_fields = ('phonenumber', 'email',)
    readonly_fields = ('datetimecreated', 'last_login')

    filter_horizontal = ()
    list_filter = ()
    ordering = ('email',)
    fieldsets = (
        (None,
         {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('last_name', 'first_name', 'phonenumber', 'stripe_customer_id', 'one_click_purchasing', 'datetimecreated')}),
        ('Permissions', {'fields': ('is_admin', 'is_staff', 'is_vendor', 'is_customer')}),
                 )


admin.site.register(User, AccountAdmin)
admin.site.register(Vendor)
admin.site.register(Customer)


