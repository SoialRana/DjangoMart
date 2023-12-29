from django.db import models
from django.contrib.auth.models import User
# Create your models here.
from store.models import Product
from accounts.models import Account
# Here we perform our payment task 
class Payment(models.Model):# Through the model we store our database that our user payment the money which medium , and 
    # how much money he pay,and when and how she payment everything.so we need a model.
    # user = models.ForeignKey(User, on_delete=models.CASCADE) # A user can perform many transaction 
    user = models.ForeignKey(Account, on_delete=models.CASCADE) # A user can perform many transaction
    payment_id = models.CharField(max_length= 100) # we use the payment id and find when and how much money we payment
    payment_method = models.CharField(max_length=100)
    amount_paid = models.IntegerField()
    status = models.CharField(max_length = 100)
    created_at = models.DateTimeField(auto_now_add=True)

class Order(models.Model):
    STATUS = (
        ('New', 'New'),
        ('Accepted', 'Accepted'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    )
    # user = models.ForeignKey(User, on_delete= models.CASCADE)
    user = models.ForeignKey(Account, on_delete= models.CASCADE)
    # payment = models.ForeignKey(Payment, on_delete=models.CASCADE)
    # A user can perform multiple payment
    order_number = models.CharField(max_length=30) # As user can show his order number in dashboard so need order number
    first_name = models.CharField(max_length=100)# If he wants to try another person order so again need first name
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=12)
    email = models.EmailField(max_length=50)
    address_line1 = models.CharField(max_length=100)
    address_line2 = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    order_note = models.CharField(max_length=100)
    
    # Here above we set user details now below we set product details
    order_total = models.FloatField()
    tax = models.FloatField()
    status = models.CharField(max_length=10, choices = STATUS, default='New')# As user perform a order so it is approved or accept ? 
    # We use max_length must be for charField
    ip = models.CharField(max_length=100, blank=True, null = True) # We can track user ip address if user address have 
    # some mistake. Blank=True means if we don't push or give any data still save it backend and don't show any error
    # Null means we can blank it. 
    is_ordered = models.BooleanField(default=False) # We check that a product ordered or not
    created_at = models.DateTimeField(auto_now_add = True)


class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete= models.CASCADE) # A product can be ordered in multiple time. A product must have ordered details when we ordered a product
    payment = models.ForeignKey(Payment, on_delete= models.CASCADE)
    # user = models.ForeignKey(User, on_delete= models.CASCADE)
    user = models.ForeignKey(Account, on_delete= models.CASCADE)
    product = models.ForeignKey(Product, on_delete= models.CASCADE)
    quantity = models.IntegerField() # How many product we purchase this product
    ordered = models.BooleanField(default=False)# First time the product ordered or not default it is false
    created = models.DateTimeField(auto_now_add=True)

class PaymentGateWaySettings(models.Model): 
    store_id = models.CharField(max_length=500, blank=True, null=True)
    store_pass = models.CharField(max_length=500, blank=True, null = True)
    # Our store id and password don't change repeatedly so this task we done from backend