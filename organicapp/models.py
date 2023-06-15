from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):
    CAT=((1,'Fruits'),(2,'Vegetables'))
    name=models.CharField(max_length=50,verbose_name="Product Name")
    cat=models.IntegerField(verbose_name="Category",choices=CAT)
    price=models.FloatField(verbose_name="Product Price")
    status=models.BooleanField(default=True)
    pimage=models.ImageField(upload_to="image")

class Cart(models.Model):
    uid=models.ForeignKey(User,on_delete=models.CASCADE,db_column='uid')
    pid=models.ForeignKey(Product,on_delete=models.CASCADE,db_column='pid')
    qty=models.IntegerField(default=1)

class Order(models.Model):
    order_id=models.IntegerField()
    uid=models.ForeignKey(User,on_delete=models.CASCADE,db_column='uid')
    pid=models.ForeignKey(Product,on_delete=models.CASCADE,db_column='pid')
    qty=models.IntegerField()

    def __str__(self):

        return self.order_id
    
class OrderHistory(models.Model):
    order_id=models.CharField(max_length=400)
    pay_id=models.CharField(max_length=400)
    sign=models.CharField(max_length=400)
    uid=models.ForeignKey(User,on_delete=models.CASCADE,db_column='uid')
 
    def __str__(self):

        return self.order_id
    
class Contact(models.Model):
    name=models.CharField(max_length=400)
    email=models.CharField(max_length=400)
    mobile=models.CharField(max_length=400)
    message=models.CharField(max_length=1000)