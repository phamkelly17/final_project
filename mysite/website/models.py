from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.

class User (AbstractUser):
    pass

class Home (models.Model):
    slide_img1 =  models.ImageField(upload_to='images/', blank = True, default = None)
    slide_img2 =  models.ImageField(upload_to='images/', blank = True, default = None)
    slide_img3 =  models.ImageField(upload_to='images/', blank = True, default = None)
    slide_img4 =  models.ImageField(upload_to='images/', blank = True, default = None)
    slide_img5 =  models.ImageField(upload_to='images/', blank = True, default = None)
    about_img =  models.ImageField(upload_to='images/', blank = True, default = None)
    menu_img =  models.ImageField(upload_to='images/', blank = True, default = None)

class MenuItem (models.Model):
    image = models.ImageField (upload_to = 'images/', blank = True, default = None)
    name = models.CharField(max_length = 100)
    price = models.DecimalField (max_digits = 4, decimal_places = 2, default = None)
    description = models.CharField(max_length = 200)
    vegan = models.BooleanField (default = None)

class Review (models.Model):
    user = models.ForeignKey (User, on_delete = models.CASCADE, related_name = "reviews")
    content = models.CharField(max_length = 200)
    stars = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], default = None)
    product_bought = models.ForeignKey(MenuItem, on_delete = models.CASCADE, related_name = "reviews")
    timestamp = models.DateTimeField(auto_now_add=True)

    def serialize(self):
        return {
            "user": self.user.username,
            "content": self.content,
            "stars": self.stars,
            "product_bought": self.product_bought.name,
            "timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p")
        }

class Message (models.Model):
    sender = models.ForeignKey (User, on_delete = models.CASCADE, related_name = "sender")
    receiver = models.ForeignKey(User, on_delete = models.CASCADE, related_name = "receiver")
    content = models.CharField(max_length = 250)
    read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def serialize (self):
        return {
            "sender": self.sender.username,
            "receiver":self.receiver.username,
            "content": self.content,
            "read": self.read,
            "timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p")
        }

class CartEntry(models.Model):
    menu_item = models.ForeignKey(MenuItem, on_delete = models.CASCADE)
    quantity = models.PositiveIntegerField(default = 0)
    item_total = models.DecimalField(max_digits = 6, decimal_places = 2, default = None)
    
class Cart(models.Model):
    user = models.OneToOneField (User, on_delete = models.CASCADE, related_name = "cart")
    items = models.ManyToManyField(CartEntry, default = None, blank = True)
    total_cost = models.DecimalField(max_digits = 6, decimal_places = 2, default = 0)
    order_placed = models.BooleanField(default = False)

class Order(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE, related_name ="order")
    items = models.ManyToManyField(CartEntry, default = None, blank = True)
    total_cost = models.DecimalField(max_digits = 6, decimal_places = 2, default = 0)
    order_completed = models.BooleanField(default = False)
    timestamp = models.DateTimeField(auto_now_add=True)