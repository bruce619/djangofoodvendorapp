# Django Food Vendor App
###### Django Food Vendor App is mini food ecommerce web app mainly for buying and selling of food/dishes.

[![Build Status](https://travis-ci.org/joemccann/dillinger.svg?branch=master)](https://travis-ci.org/joemccann/dillinger)

## Core Features

- Authentication and authorization
- Food purchase / pre-order
- Order management
- Notification

## Users
This application has two types of users:
- The vendor
- The customer

## Functional Requirements (Vendor)
- The vendor are able to sign up with name, email and phone number.
- The vendor are able to set a password.
- The vendor are able to log in with email and password.
- The vendor are able to create a menu.
- The vendor are able to update a menu.
- The vendor are able to view orders.
- The vendor are able to update order status.
- The vendor are able to generate a daily report of sales.
- The vendor are able to send notifications to the customer on available menu or debts, order progress and other relevant information.

## Functional Requirements (Customer)
- Customer are able to sign up with name, email and phone number.
- Customer are able to set a password.
- Customer are able to log in with email and password.
- Customer are able to order food from the available menu that has been put up by the vendor.
- Customer are able to add food to cart.
- Customer are able to cancel order.
- Payment for food purchased (stripe was integrated with this app).

NB: For development purpose only test credit cards can be used. Acquire test cards from
- [Stripe](https://stripe.com/docs/testing/)

## Tech

| Tool | URL |
| ------ | ------ |
| Django | [Django 3.0](https://docs.djangoproject.com/en/3.0/) |
| Stripe | [Stripe API](https://stripe.com/docs/api) |
| Python | [python 3.7.0](https://docs.python.org/3.7/tutorial/index.html) |
|Django-Heroku | [Heroku](https://www.dropbox.com/s/68sc3ihna7qdaiu/test.py?dl=0) |
| AWS | [Django-AWS S3](https://django-storages.readthedocs.io/en/latest/) |