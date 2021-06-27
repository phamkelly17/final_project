from django.contrib import admin
from .models import User, Home, MenuItem, Review, Message, Cart, CartEntry,Order
# Register your models here.

admin.site.register(User)
admin.site.register(Home)
admin.site.register (MenuItem)
admin.site.register (Review)
admin.site.register (Message)
admin.site.register (Cart)
admin.site.register (CartEntry)
admin.site.register(Order)