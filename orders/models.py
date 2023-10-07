from django.db import models
from django.contrib.auth.models import User
# Create your models here.
from store.models import Product
# ekahne amra payment er kaj gulo korlam 
class Payment(models.Model):# model gulor maddhome ami amar database e oi user ki maddhome
    # taka ta payment korche kototaka payment korche ,kobe or kivabe korche sobkisu 
    # amra database e store korbo tar jonno amar model er dorkar hocche 
    user = models.ForeignKey(User, on_delete=models.CASCADE) # ekjon user many transaction korte pare
    payment_id = models.CharField(max_length= 100) # payment id diye ber kora jabe kokhon koto taka payment korchi
    payment_method = models.CharField(max_length=100)
    amount_paid = models.IntegerField()
    status = models.CharField(max_length = 100)
    created_at = models.DateTimeField(auto_now_add=True)
    # kon date time e se transaction create korche 

class Order(models.Model):
    STATUS = (
        ('New', 'New'),
        ('Accepted', 'Accepted'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    )
    user = models.ForeignKey(User, on_delete= models.CASCADE)
    # payment = models.ForeignKey(Payment, on_delete=models.CASCADE)
    # ekjon user multiple payment korte pare 
    order_number = models.CharField(max_length=30) # user jate tar order number er 
    # quantity dashboard e dekhte pare tar jonno order no lagbe 
    first_name = models.CharField(max_length=100)# jodi se onno karo order korte chay
    # tar jonno abar first name rakhtechi 
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=12)
    email = models.EmailField(max_length=50)
    address_line1 = models.CharField(max_length=100)
    address_line2 = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    order_note = models.CharField(max_length=100)
    # user er details gelo ekhon product details dibo
    order_total = models.FloatField()
    tax = models.FloatField()
    status = models.CharField(max_length=10, choices = STATUS, default='New')
    # user j order korlo eta ki approve /accept hoiche 
    # charField er khetre must be max langth dite hobe 
    ip = models.CharField(max_length=100, blank=True, null = True)
    # amra user er ip address k track rakhte pari jodi user er address vull hote pare 
    # blank hocche eta amra dibo na ar null hocche eta amra faka rakhte pari kono kisu
    # nao dite pari ...blank=true hocche amra jodi kono kichu nao diye thaki tarporo 
    # jate backend e save hoi kono error na dekhay 
    is_ordered = models.BooleanField(default=False) #ekta product order hocche ki na 
    # seta amra check kortechi 
    created_at = models.DateTimeField(auto_now_add = True)


class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete= models.CASCADE) # ekta product multiple
    # time order hote pare ...ekta product jokhon order kora hobe tar order detils and
    # payment details thakbe 
    payment = models.ForeignKey(Payment, on_delete= models.CASCADE)
    user = models.ForeignKey(User, on_delete= models.CASCADE)
    product = models.ForeignKey(Product, on_delete= models.CASCADE)
    quantity = models.IntegerField() # ei product koto quantity amra purchase kortechi
    ordered = models.BooleanField(default=False)# product ta order kora hoiche ki na 
    # first time false rakhbo j order kora hoi nie 
    created = models.DateTimeField(auto_now_add=True)

class PaymentGateWaySettings(models.Model): 
    store_id = models.CharField(max_length=500, blank=True, null=True)
    store_pass = models.CharField(max_length=500, blank=True, null = True)
    # amader store id and password jate bar bar na change korte hoi tar jonno amra 
    # ei kaj ta backend thake kortechi 