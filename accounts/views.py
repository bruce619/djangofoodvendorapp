from django.contrib import messages, auth
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, UpdateView, FormView, RedirectView
from accounts.forms import *
from accounts.models import User
from .decorators import user_is_vendor, user_is_customer


class VendorRegisterView(CreateView):
    model = User
    form_class = VendorRegistrationForm
    template_name = 'accounts/vendor/register.html'
    success_url = reverse_lazy('home')

    extra_context = {
        'title': 'Register'
    }

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(self.request, *args, **kwargs)

    def post(self, request, *args, **kwargs):

        form = self.form_class(data=request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data.get("password1")
            user.set_password(password)
            user.save()
            messages.success(request, 'Your account has been created!!')
            return redirect('login')
        else:
            return render(request, 'accounts/vendor/register.html', {'form': form})


class CustomerRegisterView(CreateView):
    model = User
    form_class = CustomerRegistrationForm
    template_name = 'accounts/customer/register.html'
    success_url = reverse_lazy('home')

    extra_context = {
        'title': 'Register'
    }

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(self.request, *args, **kwargs)

    def post(self, request, *args, **kwargs):

        form = self.form_class(data=request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data.get("password1")
            user.set_password(password)
            user.save()
            messages.success(request, 'Your account has been created!!')
            return redirect('login')
        else:
            return render(request, 'accounts/customer/register.html', {'form': form})


class LoginView(FormView):
    """
        Provides the ability to login as a user with an email and password
    """
    success_url = reverse_lazy('home')
    form_class = UserLoginForm
    template_name = 'accounts/login.html'

    extra_context = {
        'title': 'Login'
    }

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(self.request, *args, **kwargs)

    def get_success_url(self):
        if 'next' in self.request.GET and self.request.GET['next'] != '':
            return self.request.GET['next']
        else:
            return self.success_url

    def get_form_class(self):
        return self.form_class

    def form_valid(self, form):
        auth.login(self.request, form.get_user())
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        """If the form is invalid, render the invalid form."""
        return self.render_to_response(self.get_context_data(form=form))


class LogoutView(RedirectView):
    """
    Provides users the ability to logout
    """
    url = '/login'

    def get(self, request, *args, **kwargs):
        auth.logout(request)
        messages.success(request, 'You are now logged out')
        return super(LogoutView, self).get(request, *args, **kwargs)


class EditVendorProfileView(UpdateView):
    model = User
    form_class = VendorUpdateForm
    context_object_name = 'vendor'
    template_name = 'accounts/edit-profile.html'
    success_url = reverse_lazy('vendor-profile-update')

    @method_decorator(login_required(login_url=reverse_lazy('login')))
    @method_decorator(user_is_vendor)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(self.request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        try:
            self.object = self.get_object()
        except Http404:
            raise Http404("User doesn't exists")
        return self.render_to_response(self.get_context_data())

    def get_object(self, queryset=None):
        obj = self.request.user
        print(obj)
        if obj is None:
            raise Http404("doesn't exists")
        return obj

    def get_success_url(self):
        messages.success(self.request, 'Update successful')
        return reverse_lazy('home')


class EditCustomerProfileView(UpdateView):
    model = User
    form_class = CustomerUpdateForm
    context_object_name = 'customer'
    template_name = 'accounts/edit-profile.html'
    success_url = reverse_lazy('customer-profile-update')

    @method_decorator(login_required(login_url=reverse_lazy('login')))
    @method_decorator(user_is_customer)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(self.request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        try:
            self.object = self.get_object()
        except Http404:
            raise Http404("User doesn't exists")
        return self.render_to_response(self.get_context_data())

    def get_object(self, queryset=None):
        obj = self.request.user
        print(obj)
        if obj is None:
            raise Http404("doesn't exists")
        return obj

    def get_success_url(self):
        messages.success(self.request, 'Update successful')
        return reverse_lazy('home')

