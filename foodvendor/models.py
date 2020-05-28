from django.conf import settings
from django.db import models
from accounts.models import Vendor
from PIL import Image
from django_countries.fields import CountryField
from django.core.files.storage import default_storage as storage
from django.utils import timezone


ADDRESS_CHOICES = (
    ('B', 'Billing'),
    ('S', 'Shipping'),
)


class Menu(models.Model):
    none = 0
    Daily = 1
    Weekly = 7
    EVERY_2_WEEK = 14
    EVERY_4_WEEK = 30

    Frequency_Of_Recurrence = (
        (none, "None"),
        (Daily, "Daily"),
        (Weekly, "Weekly"),
        (EVERY_2_WEEK, "Every 2 week"),
        (EVERY_4_WEEK, "Monthly"),
    )
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    name = models.CharField(verbose_name="food name", null=False, blank=False, max_length=100)
    description = models.TextField(verbose_name="Food Description", max_length=350, null=False, blank=False)
    price = models.FloatField(verbose_name="Price ($)", default=0.00)
    discount_price = models.FloatField(blank=True, null=True)
    image = models.ImageField(upload_to='images/', default='veggies.jpg')
    isrecurring = models.BooleanField(default=False)
    frequencyofrecurrence = models.IntegerField(choices=Frequency_Of_Recurrence)
    datetimecreated = models.DateTimeField(verbose_name='date-time-created', default=timezone.now)

    def __str__(self):
        return self.name + " by " + f'{self.vendor.user.first_name}'

    def save(self, *args, **kwargs):
        super(Menu, self).save(*args, **kwargs)

        img = Image.open(self.image)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size, Image.ANTIALIAS)
            fh = storage.open(self.image.name, "w")
            ext = 'jpeg'
            format = 'JPEG' if ext.lower() == 'jpg' else ext.upper()
            img.save(fh, format)
            fh.close()


class MenuItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.menu.name}"

    def get_total_item_price(self):
        return self.quantity * self.menu.price

    def get_total_discount_item_price(self):
        return self.quantity * self.menu.discount_price

    def get_amount_saved(self):
        return self.get_total_item_price() - self.get_total_discount_item_price()

    def get_final_price(self):
        if self.menu.discount_price:
            return self.get_total_discount_item_price()
        return self.get_total_item_price()


class OrderStatus(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    itemsordered = models.ManyToManyField(MenuItem, verbose_name="menuitem", default=None, blank=True)
    ref_code = models.CharField(max_length=20, blank=True, null=True)
    start_date = models.DateTimeField(auto_now_add=True)
    dateandtimeoforder = models.DateTimeField(verbose_name='date-time-ordered')
    ordered = models.BooleanField(default=False)
    shipping_address = models.ForeignKey(
        'Address', related_name='shipping_address', on_delete=models.SET_NULL, blank=True, null=True)
    billing_address = models.ForeignKey(
        'Address', related_name='billing_address', on_delete=models.SET_NULL, blank=True, null=True)
    payment = models.ForeignKey(
        'Payment', on_delete=models.SET_NULL, blank=True, null=True)
    orderstatus = models.ForeignKey(OrderStatus, on_delete=models.SET_NULL, blank=True, null=True)

    '''
        1. Item added to cart
        2. Adding a billing address
        (Failed checkout)
        3. Payment
        (Preprocessing, processing, packaging etc.)
        4. Orderstatus
        (being delivered, received, refund_requested, refund granted)
        '''

    def __str__(self):
        return '{}'.format(self.user.email)

    def get_total(self):
        total = 0
        for order_item in self.itemsordered.all():
            total += order_item.get_final_price()
        return total


class Address(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    street_address = models.CharField(max_length=100)
    apartment_address = models.CharField(max_length=100)
    country = CountryField(multiple=False)
    zip = models.CharField(max_length=100)
    address_type = models.CharField(max_length=1, choices=ADDRESS_CHOICES)
    default = models.BooleanField(default=False)

    def __str__(self):
        return str(self.street_address) + ", " + str(self.country)

    class Meta:
        verbose_name_plural = 'Addresses'


class Payment(models.Model):
    stripe_charge_id = models.CharField(max_length=50)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)
    amount = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name


class Refund(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    reason = models.TextField()
    accepted = models.BooleanField(default=False)
    email = models.EmailField()

    def __str__(self):
        return f"{self.pk}" + self.order.ref_code


class MessageStatus(models.Model):
    name = models.CharField(max_length=15)

    def __str__(self):
        return self.name


class Notification(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='receiver')
    order = models.ForeignKey(Order, verbose_name="order id", on_delete=models.CASCADE)
    message = models.TextField(max_length=None)
    messagestatus = models.ForeignKey(MessageStatus, on_delete=models.CASCADE)
    dateTimeCreated = models.DateTimeField(verbose_name='sent_date', auto_now_add=True)

    def __str__(self):
        return str(self.sender) + " to " + str(self.receiver) + " for " + str(self.order.ref_code)

    '''
        Orderstatus
        (being delivered, received, refund_requested, refund granted)
    '''










