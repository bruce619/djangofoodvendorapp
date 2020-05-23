from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction

from accounts.models import User, Customer, Vendor


class CustomerRegistrationForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super(CustomerRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].label = "First Name"
        self.fields['last_name'].label = "Last Name"
        self.fields['password1'].label = "Password"
        self.fields['password2'].label = "Confirm Password"

        self.fields['first_name'].widget.attrs.update(
            {
                'placeholder': 'Enter First Name',
            }
        )
        self.fields['last_name'].widget.attrs.update(
            {
                'placeholder': 'Enter Last Name',
            }
        )
        self.fields['email'].widget.attrs.update(
            {
                'placeholder': 'Enter Email',
            }
        )
        self.fields['phonenumber'].widget.attrs.update(
            {
                'placeholder': 'Enter Phone number',
            }
        )
        self.fields['password1'].widget.attrs.update(
            {
                'placeholder': 'Enter Password',
            }
        )
        self.fields['password2'].widget.attrs.update(
            {
                'placeholder': 'Confirm Password',
            }
        )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'phonenumber', 'password1', 'password2']
        exclude = ['username']

    @transaction.atomic
    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.is_customer = True
        user.save()
        customer = Customer.objects.create(user=user)
        return user


class VendorRegistrationForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super(VendorRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].label = "Business Name"
        self.fields['last_name'].label = "Business Location(City, Country)"
        self.fields['password1'].label = "Password"
        self.fields['password2'].label = "Confirm Password"

        self.fields['first_name'].widget.attrs.update(
            {
                'placeholder': 'Enter Vendor Name',
            }
        )
        self.fields['last_name'].widget.attrs.update(
            {
                'placeholder': 'Location e.g (Lagos, Nigeria)',
            }
        )
        self.fields['email'].widget.attrs.update(
            {
                'placeholder': 'Enter Email',
            }
        )
        self.fields['phonenumber'].widget.attrs.update(
            {
                'placeholder': 'Enter Phone number',
            }
        )
        self.fields['password1'].widget.attrs.update(
            {
                'placeholder': 'Enter Password',
            }
        )
        self.fields['password2'].widget.attrs.update(
            {
                'placeholder': 'Confirm Password',
            }
        )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'phonenumber', 'password1', 'password2']
        exclude = ['username']

    @transaction.atomic
    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.is_vendor = True
        user.save()
        vendor = Vendor.objects.create(user=user)
        return user


class UserLoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = None
        self.fields['email'].widget.attrs.update({'placeholder': 'Enter Email'})
        self.fields['password'].widget.attrs.update({'placeholder': 'Enter Password'})

    def clean(self, *args, **kwargs):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")

        if email and password:
            self.user = authenticate(email=email, password=password)

            if self.user is None:
                raise forms.ValidationError("Email or Password Does not Match.")
            if not self.user.check_password(password):
                raise forms.ValidationError("Password Does not Match.")
            if not self.user.is_active:
                raise forms.ValidationError("User is not Active.")

        return super(UserLoginForm, self).clean(*args, **kwargs)

    def get_user(self):
        return self.user


class VendorUpdateForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(VendorUpdateForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].label = "Business Name"
        self.fields['last_name'].label = "Business Location(City, Country)"

        self.fields['first_name'].widget.attrs.update(
            {
                'placeholder': 'Update Business Name',
            }
        )
        self.fields['last_name'].widget.attrs.update(
            {
                'placeholder': 'Update Location',
            }
        )
        self.fields['email'].widget.attrs.update(
            {
                'placeholder': 'Update Email',
            }
        )
        self.fields['phonenumber'].widget.attrs.update(
            {
                'placeholder': 'Update Phone number',
            }
        )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'phonenumber']
        exclude = ['username']

    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            account = User.objects.exclude(pk=self.instance.pk).get(email=email)
        except User.DoesNotExist:
            return email
        raise forms.ValidationError('Email "%s" is already in use.' % account)

    def clean_phonenumber(self):
        phonenumber = self.cleaned_data['phonenumber']
        try:
            account = User.objects.exclude(pk=self.instance.pk).get(phonenumber=phonenumber)
        except User.DoesNotExist:
            return phonenumber
        raise forms.ValidationError('Phone Number "%s" is already in use.' % account)


class CustomerUpdateForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(CustomerUpdateForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].label = "First Name"
        self.fields['last_name'].label = "Last Name"

        self.fields['first_name'].widget.attrs.update(
            {
                'placeholder': 'Update First Name',
            }
        )
        self.fields['last_name'].widget.attrs.update(
            {
                'placeholder': 'Update Last Name',
            }
        )
        self.fields['email'].widget.attrs.update(
            {
                'placeholder': 'Update Email',
            }
        )
        self.fields['phonenumber'].widget.attrs.update(
            {
                'placeholder': 'Update Phone number',
            }
        )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'phonenumber']
        exclude = ['username']

    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            account = User.objects.exclude(pk=self.instance.pk).get(email=email)
        except User.DoesNotExist:
            return email
        raise forms.ValidationError('Email "%s" is already in use.' % account)

    def clean_phonenumber(self):
        phonenumber = self.cleaned_data['phonenumber']
        try:
            account = User.objects.exclude(pk=self.instance.pk).get(phonenumber=phonenumber)
        except User.DoesNotExist:
            return phonenumber
        raise forms.ValidationError('Phone Number "%s" is already in use.' % account)