from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import HttpResponse, render, redirect
from django.contrib import messages
from django.utils.decorators import method_decorator
from ..forms import CreateMenuForm, UpdateMenuForm
from django.views.generic import CreateView, View, ListView, UpdateView, DeleteView
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from accounts.models import Vendor
from ..models import Menu, Order, MenuItem
from accounts.decorators import user_is_vendor
from django.http import JsonResponse
from django.core import serializers


class MenuCreateView(SuccessMessageMixin, CreateView):
    model = Menu
    template_name = 'foodvendor/vendor/create-menu.html'
    form_class = CreateMenuForm
    extra_context = {
        'title': 'Post New Food'
    }
    success_url = reverse_lazy('home')
    success_message = "Menu Successfully Created!!"

    @method_decorator(login_required(login_url=reverse_lazy('login')))
    @method_decorator(user_is_vendor)
    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return reverse_lazy('login')
        if self.request.user.is_authenticated and self.request.user.is_customer and self.request.user.is_superuser:
            return reverse_lazy('login')
        return super().dispatch(self.request, *args, **kwargs)

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.vendor = Vendor.objects.get(user_id=self.request.user.id)
        instance.save()
        return super(MenuCreateView, self).form_valid(form)

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class MenuUpdateView(SuccessMessageMixin, UserPassesTestMixin, UpdateView):
    model = Menu
    template_name = 'foodvendor/vendor/update-menu.html'
    form_class = UpdateMenuForm
    pk_url_kwarg = 'id'
    slug_field = 'id'
    success_message = "Menu Successfully Updated!!"

    @method_decorator(login_required(login_url=reverse_lazy('login')))
    @method_decorator(user_is_vendor)
    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return reverse_lazy('login')
        if self.request.user.is_authenticated and self.request.user.is_customer and self.request.user.is_superuser:
            return reverse_lazy('login')
        return super().dispatch(self.request, *args, **kwargs)

    def get_form(self, **kwargs):
        form = super().get_form(**kwargs)
        return form

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def test_func(self):
        menu = self.get_object()
        if self.request.user == menu.vendor.user:
            return True
        return False

    def get_success_url(self):
        return reverse_lazy('menu-detail', kwargs={'id': self.kwargs['id']})


class MenuDeleteView(UserPassesTestMixin, DeleteView):
    model = Menu
    template_name = 'foodvendor/vendor/menu-delete.html'
    success_url = reverse_lazy('menus')

    @method_decorator(login_required(login_url=reverse_lazy('login')))
    @method_decorator(user_is_vendor)
    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return reverse_lazy('login')
        if self.request.user.is_authenticated and self.request.user.is_customer and self.request.user.is_superuser:
            return reverse_lazy('login')
        return super().dispatch(self.request, *args, **kwargs)

    def test_func(self):
        menu = self.get_object()
        # Only users that created the post are permitted to delete the post
        if self.request.user == menu.vendor.user:
            return True
        return False


class DashboardView(ListView):
    model = Menu
    template_name = 'foodvendor/vendor/dashboard.html'
    context_object_name = 'menus'
    ordering = ['-datetimecreated']
    paginate_by = 4

    @method_decorator(login_required(login_url=reverse_lazy('login')))
    @method_decorator(user_is_vendor)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(self.request, *args, **kwargs)

    def get_queryset(self):
        vendor = Vendor.objects.get(user=self.request.user)
        return self.model.objects.filter(vendor=vendor).order_by('-datetimecreated')


class CustomersListView(ListView):
    model = MenuItem
    template_name = 'foodvendor/vendor/customers.html'
    context_object_name = 'customers'
    paginate_by = 5

    @method_decorator(login_required(login_url=reverse_lazy('login')))
    @method_decorator(user_is_vendor)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(self.request, *args, **kwargs)

    def get_queryset(self):
        menu = Menu.objects.get(id=self.kwargs['id'])
        return MenuItem.objects.filter(menu=menu, ordered=True).order_by('id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = Menu.objects.get(id=self.kwargs['id'])
        return context









