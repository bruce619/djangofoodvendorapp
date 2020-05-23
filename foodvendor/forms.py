from django import forms
from .models import Menu, Notification
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget

PAYMENT_CHOICES = (
    ('S', 'Stripe'),
    ('P', 'PayPal')
)


class CheckoutForm(forms.Form):
    shipping_address = forms.CharField(required=False)
    shipping_address2 = forms.CharField(required=False)
    shipping_country = CountryField(blank_label='(select country)').formfield(
        required=False,
        widget=CountrySelectWidget(attrs={
            'class': 'custom-select d-block w-100',
        }))
    shipping_zip = forms.CharField(required=False)

    billing_address = forms.CharField(required=False)
    billing_address2 = forms.CharField(required=False)
    billing_country = CountryField(blank_label='(select country)').formfield(
        required=False,
        widget=CountrySelectWidget(attrs={
            'class': 'custom-select d-block w-100',
        }))
    billing_zip = forms.CharField(required=False)

    same_billing_address = forms.BooleanField(required=False)
    set_default_shipping = forms.BooleanField(required=False)
    use_default_shipping = forms.BooleanField(required=False)
    set_default_billing = forms.BooleanField(required=False)
    use_default_billing = forms.BooleanField(required=False)

    payment_option = forms.ChoiceField(
        widget=forms.RadioSelect, choices=PAYMENT_CHOICES)


class RefundForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super(RefundForm, self).__init__(*args, **kwargs)

        self.fields['ref_code'].widget.attrs.update(
            {
                'placeholder': 'Input Order Reference Code',
            }
        )
        self.fields['message'].widget.attrs.update(
            {
                'placeholder': 'Your Message',
            }
        )
        self.fields['email'].widget.attrs.update(
            {
                'placeholder': 'Input Vendor Email',
            }
        )

    ref_code = forms.CharField()
    message = forms.CharField(widget=forms.Textarea(attrs={
        'rows': 4
    }))
    email = forms.EmailField()


class PaymentForm(forms.Form):
    stripeToken = forms.CharField(required=False)
    save = forms.BooleanField(required=False)
    use_default = forms.BooleanField(required=False)


class CreateMenuForm(forms.ModelForm):
    class Meta:
        model = Menu
        exclude = ('vendor', 'datetimecreated',)
        labels = {
            "name": "Food/Menu name",
            "image": "Upload Image",
            "isrecurring": "Is this item a Recurring item? check(✓) for yes, leave uncheck if No",
            "frequencyofreocurrence": "Frequency Of Reocurrence",
        }
        widgets = {
            'isrecurring': forms.CheckboxInput(attrs={
                'class': 'form-control',
            }
            ),
            'frequencyofreocurrence': forms.Select(attrs={
                'class': 'form-control',
            }
            ),
        }

    def is_valid(self):
        valid = super(CreateMenuForm, self).is_valid()

        # if already valid, then return True
        if valid:
            return valid
        return valid

    def save(self, commit=True):
        menu = super(CreateMenuForm, self).save(commit=False)
        if commit:
            menu.save()
        return menu


class UpdateMenuForm(forms.ModelForm):
    class Meta:
        model = Menu
        exclude = ('vendor', 'datetimecreated',)
        labels = {
            "name": "Edit Food/Menu name",
            "price": "Edit Price",
            "discount_price": "Discount Price",
            "isrecurring": "Is this item a Recurring item? check(✓) for yes, leave uncheck if No",
            "frequencyofreocurrence": "Frequency Of Reocurrence"
        }
        widgets = {
            'isrecurring': forms.CheckboxInput(attrs={
                'class': 'form-control',
            }
            ),
            'frequencyofreocurrence': forms.Select(attrs={
                'class': 'form-control',
            }
            ),
        }


class CreateOrderForm(forms.ModelForm):
    class Meta:
        model = Menu
        exclude = ('vendor', 'customer', 'dateAndTimeOfOrder',)
        labels = {
            "amountpaid": "Amount paid",
            "amountdue": "Total Amount of Item",
            "amountoutstanding": "Amount yet to be paid",
        }

    def is_valid(self):
        valid = super(CreateOrderForm, self).is_valid()

        # if already valid, then return True
        if valid:
            return valid
        return valid

    def save(self, commit=True):
        order = super(CreateOrderForm, self).save(commit=False)
        if commit:
            order.save()
        return order


class NotificationForm(forms.ModelForm):
    message = forms.CharField(widget=forms.Textarea(attrs={
        'rows': 4
    }))

    def __init__(self, *args, **kwargs):
        super(NotificationForm, self).__init__(*args, **kwargs)

        self.fields['message'].widget.attrs.update(
            {
                'placeholder': 'Your Message',
            }
        )

    class Meta:
        model = Notification
        fields = ('sender', 'receiver', 'order', 'message', 'messagestatus', 'dateTimeCreated',)
        exclude = ('sender', 'receiver', 'order', 'messagestatus', 'dateTimeCreated')





