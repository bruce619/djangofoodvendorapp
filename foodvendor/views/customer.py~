from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.urls import reverse_lazy
from django.shortcuts import redirect, get_object_or_404
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import CreateView, ListView, View
from django.conf import settings
from django.contrib import messages
from ..models import Menu, MenuItem, Order, OrderStatus


@login_required(login_url=reverse_lazy('login'))
def add_to_cart(request, id=None):
    menu = get_object_or_404(Menu, id=id)
    order_item, created = MenuItem.objects.get_or_create(
        menu=menu,
        user=request.user,
        ordered=False
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the ordered menu is in the order
        if order.itemsordered.filter(menu__id=menu.id).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "This menu quantity was updated.")
            return redirect("order-summary")
        else:
            order.itemsordered.add(order_item)
            messages.success(request, "This menu was added to your cart.")
            return redirect("order-summary")
    else:
        dateandtimeoforder = timezone.now()
        order = Order.objects.create(user=request.user,
                                     dateandtimeoforder=dateandtimeoforder
                                     )
        order.itemsordered.add(order_item)
        messages.success(request, "This menu was added to your cart.")
        return redirect("order-summary")


@login_required(login_url=reverse_lazy('login'))
def remove_from_cart(request, id=None):
    menu = get_object_or_404(Menu, id=id)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.itemsordered.filter(menu__id=menu.id).exists():
            order_item = MenuItem.objects.filter(
                menu=menu,
                user=request.user.id,
                ordered=False
            )[0]
            order.itemsordered.remove(order_item)
            order_item.delete()
            messages.info(request, "This menu was removed from your cart.")
            return redirect("order-summary")
        else:
            messages.info(request, "This item was not in your cart")
            return redirect("menu-detail", id=id)
    else:
        messages.info(request, "You do not have an active order")
        return redirect("menu-detail", id=id)


@login_required(login_url=reverse_lazy('login'))
def remove_single_item_from_cart(request, id=None):
    menu = get_object_or_404(Menu, id=id)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.itemsordered.filter(menu__id=menu.id).exists():
            order_item = MenuItem.objects.filter(
                menu=menu,
                user=request.user,
                ordered=False
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.itemsordered.remove(order_item)
            messages.info(request, "This menu quantity was updated.")
            return redirect("order-summary")
        else:
            messages.info(request, "This menu was not in your cart")
            return redirect("menu-detail", id=id)
    else:
        messages.info(request, "You do not have an active order")
        return redirect("menu-detail", id=id)
