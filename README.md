# django-food-vendor-app.

Django Food Vendor App is mini ecommerce app mainly for food vendors and their customers, it can also be used to sell orther products.


Core Features
• Authentication and authorization
• Food purchase / pre-order
• Order management
• Notification
Users
This application has two types of users:
• The vendor
• The customer
Functional Requirements (Vendor)
• The vendor are able to sign up with name, email and phone number.
• The vendor are able to set a password.
• The vendor are able to log in with email and password.
• The vendor are able to create a menu.
• The vendor are able to update a menu.
• The vendor are able to view orders
• The vendor are able to update order status.
• The vendor are able to generate a daily report of sales.
• The vendor are able to send notifications to the customer on available menu or debts, order progress and other relevant information.
Functional Requirements (Customer)
• Customer are able to sign up with name, email and phone number.
• Customer are able to set a password.
• Customer are able to log in with email and password.
• Customer are able to order food from the available menu that has been put up by the vendor.
• Customer are able to add food to cart.
• Customer are able to cancel order.
• Payment for food purchased (stripe was integrated with this app).

NB: For development purpose only test credit cards can be used
e.g 
1. No authentication (default U.S. card): 4242 4242 4242 4242 (can be used with any future dates, cvv, and zipcode)
2. Authentication required: 4000 0027 6000 3184 (can be used with any future dates, cvv, and zipcode)

