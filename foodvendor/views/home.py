from django.contrib import messages
from django.conf import settings
from vendorapp.settings import STRIPE_PUBLIC_KEY
from django.http import Http404,HttpResponse
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
from ..filters import MenuFilter
from django_filters.views import FilterView
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView, View
from ..models import Menu, Order, Payment, Refund, Address, OrderStatus, MessageStatus, Notification
from ..forms import CheckoutForm, RefundForm, PaymentForm, NotificationForm
from django.utils import timezone
from django.core.mail import send_mail, BadHeaderError
from django.template.loader import get_template
import random
import string
import stripe
stripe.api_key = settings.STRIPE_SECRET_KEY


def create_ref_code():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=20))


class HomeView(ListView):
    model = Menu
    template_name = 'home.html'
    context_object_name = 'menus'

    def get_queryset(self):
        return self.model.objects.all()[:6]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['trendings'] = self.model.objects.filter(datetimecreated__month=timezone.now().month)[:3]
        return context


class MenuListView(FilterView, ListView):
    model = Menu
    template_name = 'foodvendor/menus.html'
    context_object_name = 'menus'
    filterset_class = MenuFilter
    ordering = ['-datetimecreated']
    paginate_by = 5
    strict = False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = MenuFilter(self.request.GET, queryset=self.get_queryset())
        query = self.request.GET.copy()
        if 'page' in query:
            del query['page']
        context['queries'] = query
        return context


class MenuDetailsView(DetailView):
    model = Menu
    template_name = 'foodvendor/details.html'
    context_object_name = 'menu'
    pk_url_kwarg = 'id'

    @method_decorator(login_required(login_url=reverse_lazy('login')))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(self.request, *args, **kwargs)

    def get_object(self, queryset=None):
        obj = super(MenuDetailsView, self).get_object(queryset=queryset)
        if obj is None:
            raise Http404("Menu doesn't exists")
        return obj

    def get(self, request, *args, **kwargs):
        try:
            self.object = self.get_object()
        except Http404:
            # redirect here
            raise Http404("Menu doesn't exists")
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)


class OrderSummaryView(LoginRequiredMixin, View):

    @method_decorator(login_required(login_url=reverse_lazy('login')))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(self.request, *args, **kwargs)

    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user,
                                      ordered=False)
            context = {
                'object': order
            }
            return render(self.request, 'foodvendor/customer/order_summary.html', context)
        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have an active order")
            return redirect("home")


def is_valid_form(values):
    valid = True
    for field in values:
        if field == '':
            valid = False
    return valid


class CheckoutView(View):

    @method_decorator(login_required(login_url=reverse_lazy('login')))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(self.request, *args, **kwargs)

    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            form = CheckoutForm()
            context = {
                'form': form,
                'order': order,
            }

            shipping_address_qs = Address.objects.filter(
                user=self.request.user,
                address_type='S',
                default=True
            )
            if shipping_address_qs.exists():
                context.update(
                    {'default_shipping_address': shipping_address_qs[0]})

            billing_address_qs = Address.objects.filter(
                user=self.request.user,
                address_type='B',
                default=True
            )
            if billing_address_qs.exists():
                context.update(
                    {'default_billing_address': billing_address_qs[0]})

            return render(self.request, "foodvendor/checkout.html", context)
        except ObjectDoesNotExist:
            messages.info(self.request, "You do not have an active order")
            return redirect("checkout")

    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            if form.is_valid():

                use_default_shipping = form.cleaned_data.get(
                    'use_default_shipping')
                if use_default_shipping:
                    print("Using the defualt shipping address")
                    address_qs = Address.objects.filter(
                        user=self.request.user,
                        address_type='S',
                        default=True
                    )
                    if address_qs.exists():
                        shipping_address = address_qs[0]
                        order.shipping_address = shipping_address
                        order.save()
                    else:
                        messages.info(
                            self.request, "No default shipping address available")
                        return redirect('checkout')
                else:
                    print("User is entering a new shipping address")
                    shipping_address1 = form.cleaned_data.get(
                        'shipping_address')
                    shipping_address2 = form.cleaned_data.get(
                        'shipping_address2')
                    shipping_country = form.cleaned_data.get(
                        'shipping_country')
                    shipping_zip = form.cleaned_data.get('shipping_zip')

                    if is_valid_form([shipping_address1, shipping_country, shipping_zip]):
                        shipping_address = Address(
                            user=self.request.user,
                            street_address=shipping_address1,
                            apartment_address=shipping_address2,
                            country=shipping_country,
                            zip=shipping_zip,
                            address_type='S'
                        )
                        shipping_address.save()

                        order.shipping_address = shipping_address
                        order.save()

                        set_default_shipping = form.cleaned_data.get(
                            'set_default_shipping')
                        if set_default_shipping:
                            shipping_address.default = True
                            shipping_address.save()

                    else:
                        messages.info(
                            self.request, "Please fill in the required shipping address fields")

                use_default_billing = form.cleaned_data.get(
                    'use_default_billing')
                same_billing_address = form.cleaned_data.get(
                    'same_billing_address')

                if same_billing_address:
                    billing_address = shipping_address
                    billing_address.pk = None
                    billing_address.save()
                    billing_address.address_type = 'B'
                    billing_address.save()
                    order.billing_address = billing_address
                    order.save()

                elif use_default_billing:
                    print("Using the defualt billing address")
                    address_qs = Address.objects.filter(
                        user=self.request.user,
                        address_type='B',
                        default=True
                    )
                    if address_qs.exists():
                        billing_address = address_qs[0]
                        order.billing_address = billing_address
                        order.save()
                    else:
                        messages.info(
                            self.request, "No default billing address available")
                        return redirect('checkout')
                else:
                    print("User is entering a new billing address")
                    billing_address1 = form.cleaned_data.get(
                        'billing_address')
                    billing_address2 = form.cleaned_data.get(
                        'billing_address2')
                    billing_country = form.cleaned_data.get(
                        'billing_country')
                    billing_zip = form.cleaned_data.get('billing_zip')

                    if is_valid_form([billing_address1, billing_country, billing_zip]):
                        billing_address = Address(
                            user=self.request.user,
                            street_address=billing_address1,
                            apartment_address=billing_address2,
                            country=billing_country,
                            zip=billing_zip,
                            address_type='B'
                        )
                        billing_address.save()

                        order.billing_address = billing_address
                        order.save()

                        set_default_billing = form.cleaned_data.get(
                            'set_default_billing')
                        if set_default_billing:
                            billing_address.default = True
                            billing_address.save()

                    else:
                        messages.info(
                            self.request, "Please fill in the required billing address fields")

                payment_option = form.cleaned_data.get('payment_option')

                if payment_option == 'S':
                    return redirect('payment', payment_option='stripe')
                elif payment_option == 'P':
                    return redirect('payment', payment_option='paypal')
                else:
                    messages.warning(
                        self.request, "Invalid payment option selected")
                    return redirect('checkout')
        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have an active order")
            return redirect("order-summary")


class PaymentView(View):

    @method_decorator(login_required(login_url=reverse_lazy('login')))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(self.request, *args, **kwargs)

    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            if order.billing_address:
                context = {
                    'order': order,
                    'STRIPE_PUBLIC_KEY': STRIPE_PUBLIC_KEY
                }
                userprofile = self.request.user
                if userprofile.one_click_purchasing:
                    # fetch the users card list
                    cards = stripe.Customer.list_sources(
                        userprofile.stripe_customer_id,
                        limit=3,
                        object='card'
                    )
                    card_list = cards['data']
                    if len(card_list) > 0:
                        # update the context with the default card
                        context.update({
                            'card': card_list[0]
                        })
                return render(self.request, "foodvendor/payment.html", context)
            else:
                messages.warning(
                    self.request, "You have not added a billing address")
                return redirect("checkout")
        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have an active order")
            return redirect("home")

    def post(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            form = PaymentForm(self.request.POST)
            userprofile = self.request.user
            if form.is_valid():
                token = form.cleaned_data.get('stripeToken')
                save = form.cleaned_data.get('save')
                use_default = form.cleaned_data.get('use_default')

                if save:
                    if userprofile.stripe_customer_id != '' and userprofile.stripe_customer_id is not None:
                        customer = stripe.Customer.retrieve(
                            userprofile.stripe_customer_id)
                        customer.sources.create(source=token)

                    else:
                        customer = stripe.Customer.create(
                            email=self.request.user.email,
                        )
                        customer.sources.create(source=token)
                        userprofile.stripe_customer_id = customer['id']
                        userprofile.one_click_purchasing = True
                        userprofile.save()

                amount = int(order.get_total() * 100)

                try:

                    if use_default or save:
                        # charge the customer because we cannot charge the token more than once
                        charge = stripe.Charge.create(
                            amount=amount,  # cents
                            currency="usd",
                            customer=userprofile.stripe_customer_id
                        )
                    else:
                        # charge once off on the token
                        charge = stripe.Charge.create(
                            amount=amount,  # cents
                            currency="usd",
                            source=token
                        )

                    # create the payment
                    payment = Payment()
                    payment.stripe_charge_id = charge['id']
                    payment.user = self.request.user
                    payment.amount = order.get_total()
                    payment.save()

                    # assign the payment to the order

                    order_items = order.itemsordered.all()
                    order_items.update(ordered=True)
                    for item in order_items:
                        item.save()

                    order.ordered = True
                    order.payment = payment
                    order.ref_code = create_ref_code()
                    order.orderstatus = OrderStatus.objects.get(name="being delivered")
                    order.save()

                    messages.success(self.request, "Your order was successful!")
                    return redirect("home")

                except stripe.error.CardError as e:

                    body = e.json_body

                    err = body.get('error', {})

                    messages.warning(self.request, f"{err.get('message')}")

                    return redirect("home")

                except stripe.error.RateLimitError as e:
                    # Too many requests made to the API too quickly
                    messages.warning(self.request, "Rate limit error")
                    return redirect("home")

                except stripe.error.InvalidRequestError as e:
                    # Invalid parameters were supplied to Stripe's API
                    print(e)
                    messages.warning(self.request, "Invalid parameters")
                    return redirect("home")

                except stripe.error.AuthenticationError as e:
                    # Authentication with Stripe's API failed
                    # (maybe you changed API keys recently)
                    messages.warning(self.request, "Not authenticated")
                    return redirect("home")

                except stripe.error.APIConnectionError as e:
                    # Network communication with Stripe failed
                    messages.warning(self.request, "Network error")
                    return redirect("home")

                except stripe.error.StripeError as e:
                    # Display a very generic error to the user, and maybe send
                    # yourself an email
                    messages.warning(
                        self.request, "Something went wrong. You were not charged. Please try again.")
                    return redirect("home")

                except Exception as e:
                    # send an email to ourselves
                    messages.warning(
                        self.request, "A serious error occurred. We have been notifed.")
                    return redirect("home")

            messages.warning(self.request, "Invalid data received")
            return redirect("/payment/stripe/")
        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have an active order")
            return redirect("home")


class RequestRefundView(View):

    @method_decorator(login_required(login_url=reverse_lazy('login')))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(self.request, *args, **kwargs)

    def get(self, *args, **kwargs):
        form = RefundForm()
        context = {
            'form': form
        }
        return render(self.request, "foodvendor/request_refund.html", context)

    def post(self, *args, **kwargs):
        form = RefundForm(self.request.POST)
        if form.is_valid():
            ref_code = form.cleaned_data.get('ref_code')
            message = form.cleaned_data.get('message')
            email = form.cleaned_data.get('email')
            template = get_template('contact_template.txt')
            sender_email = self.request.user.email
            context = {
                'ref_code': ref_code,
                'message': message,
                'sender_email': sender_email
            }
            content = template.render(context)
            # edit the order
            try:
                order = Order.objects.get(ref_code=ref_code)
                order.orderstatus = OrderStatus.objects.get(name="refund requested")
                order.save()

                # store the refund
                refund = Refund()
                refund.order = order
                refund.reason = message
                refund.email = email
                refund.save()

                try:
                    send_mail(
                        "Refund Request",
                        content,
                        'Mad Til Dohren' + '',
                        [email],
                        fail_silently=False,
                    )
                except BadHeaderError:
                    return HttpResponse('Invalid header found.')

                messages.info(self.request, "Your request has been sent.")
                return redirect("home")

            except ObjectDoesNotExist:
                messages.warning(self.request, "Invalid reference code, order does not exist.")
                return redirect("request-refund")


def send_notification(request, id=None):
    template_name = 'foodvendor/send_notification.html'
    form = NotificationForm(request.GET or None)
    order = get_object_or_404(Order, id=id)
    if request.method == 'GET':
        context = {
            'form': form
        }
        return render(request, template_name, context)
    elif request.method == 'POST':
        form = NotificationForm(request.POST)
        if form.is_valid():
            message = form.cleaned_data.get('message')
            try:
                datetimecreated = timezone.now()
                messagestatus = MessageStatus.objects.get(name="message sent")
                receiver = order.user
                ref_code = order.ref_code

                notification = Notification()
                notification.sender = request.user
                notification.receiver = receiver
                notification.order = Order.objects.get(ref_code=ref_code)
                notification.message = message
                notification.messagestatus = messagestatus
                notification.dateTimeCreated = datetimecreated
                notification.save()

                messages.success(request, "Your message has been sent.")
                return redirect("home")

            except ObjectDoesNotExist:
                messages.warning(request, "Message not sent")
                return redirect("send-notification", id=id)

    return render(request, template_name, {form: 'form'})


def reply_message(request, id=None):
    template_name = 'foodvendor/send_notification.html'
    form = NotificationForm(request.GET or None)
    notification = get_object_or_404(Notification, id=id)
    if request.method == 'GET':
        context = {
            'form': form
        }
        return render(request, template_name, context)
    elif request.method == 'POST':
        form = NotificationForm(request.POST)
        if form.is_valid():
            message = form.cleaned_data.get('message')
            try:
                datetimecreated = timezone.now()
                messagestatus = MessageStatus.objects.get(name="message sent")
                receiver = notification.sender
                ref_code = notification.order.ref_code

                notification = Notification()
                notification.sender = request.user
                notification.receiver = receiver
                notification.order = Order.objects.get(ref_code=ref_code)
                notification.message = message
                notification.messagestatus = messagestatus
                notification.dateTimeCreated = datetimecreated
                notification.save()

                messages.success(request, "Your message has been sent.")
                return redirect("home")

            except ObjectDoesNotExist:
                messages.warning(request, "Message not sent")
                return redirect("send-notification", id=id)

    return render(request, template_name, {form: 'form'})


def mark_as_read(request, id=None):
    notification = get_object_or_404(Notification, id=id)
    notification.messagestatus = MessageStatus.objects.get(name="message seen")
    notification.save()
    return redirect('notifications')


class NotificationView(ListView):
    model = Notification
    template_name = 'foodvendor/notifications.html'
    context_object_name = 'notifications'
    ordering = ['-dateTimeCreated']
    paginate_by = 7

    @method_decorator(login_required(login_url=reverse_lazy('login')))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(self.request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sent'] = MessageStatus.objects.get(name="message sent")
        context['seen'] = MessageStatus.objects.get(name="message seen")
        return context

    def get_queryset(self):
        user = self.request.user
        return Notification.objects.filter(receiver=user).order_by('-dateTimeCreated')


class OrderViewList(ListView, LoginRequiredMixin):
    model = Order
    template_name = 'foodvendor/customer/user_order_list.html'
    context_object_name = 'order'
    ordering = ['-dateandtimeoforder']
    paginate_by = 3

    @method_decorator(login_required(login_url=reverse_lazy('login')))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(self.request, *args, **kwargs)

    def get_queryset(self):
        user = self.request.user
        return Order.objects.filter(user=user, ordered=True).distinct().order_by('-dateandtimeoforder')


def error_404(request, exception):
    data = {}
    return render(request, 'error_404.html', data)


def error_500(request):
    data = {}
    return render(request, 'error_500.html', data)
