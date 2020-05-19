from django.db import models

# Create your models here.
class Product(models.Model):
    product_name = models.CharField(max_length=100, default="")
    product_description = models.TextField()
    date = models.DateField(auto_now_add=True)
    category = models.CharField(max_length=50, default="")
    sub_category = models.CharField(max_length=50,default="")
    price = models.IntegerField(default=0)
    image = models.ImageField(default="")

    def __str__(self):
        return self.product_name

class Contact(models.Model):
    name = models.CharField(max_length=50)
    phone = models.CharField(max_length=10)
    email = models.EmailField()
    desc = models.TextField()

    def __str__(self):
        return self.name

class Order(models.Model):
    items_json = models.CharField(max_length=5000)
    camount = models.IntegerField(default=0)
    fname = models.CharField(max_length=255)
    lname = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=10, default='')
    address = models.CharField(max_length=255)
    address2 = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    zipcode = models.CharField(max_length=10)

    def __str__(self):
        return self.fname + ' ' + self.phone

class OrderUpdate(models.Model):
    order_id = models.IntegerField()
    update_desc = models.CharField(max_length=5000)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.update_desc



