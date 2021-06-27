from django.http.response import JsonResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.db import IntegrityError
from django import forms
from django.views.decorators.csrf import csrf_exempt
import json

from .models import User, Home, MenuItem, Review, Message, Cart, CartEntry,Order
# Create your views here.

class EditForm (forms.Form):
    slide_img1 = forms.ImageField(required = False)
    slide_img2 = forms.ImageField(required = False)
    slide_img3 = forms.ImageField(required = False)
    slide_img4 = forms.ImageField(required = False)
    slide_img5 = forms.ImageField(required = False)
    about_img = forms.ImageField(required = False)
    menu_img = forms.ImageField(required = False)

class EditMenu (forms.Form):
    name = forms.CharField (widget = forms.TextInput(
        attrs = {'type':'text','name':'name', 'placeholder': 'Item Name'}))
    description = forms.CharField (widget = forms.TextInput(
        attrs = {'type':'text','name':'description', 'placeholder': 'Item Description'}))
    price = forms.DecimalField (widget = forms.NumberInput (
        attrs={'type':'number', 'name':'price', 'placeholder':'Price'}))
    image = forms.ImageField(required = True)
    vegan = forms.BooleanField(required = False)


def index (request):
    return render (request, "website/index.html", {
        "home": Home.objects.get(pk=1)
    })

def about (request):
    return render (request, "website/about.html")

def menu (request):
    return render (request, "website/menu.html", {
        'menu_items': MenuItem.objects.all(),
    })

def edit_menu (request):
    if request.method == "POST":
        form = EditMenu(request.POST, request.FILES)
        if form.is_valid():
            if MenuItem.objects.filter(name = form.cleaned_data["name"]).length > 0:
                return JsonResponse({"error": "Item already exists."}, status=400)
            menu_item = MenuItem()
            menu_item.name = form.cleaned_data["name"]
            menu_item.description = form.cleaned_data["description"]
            menu_item.price = form.cleaned_data["price"]
            menu_item.image = form.cleaned_data["image"]
            menu_item.vegan = form.cleaned_data["vegan"]
            menu_item.save()

    return render (request, "website/editMenu.html", {
        'form': EditMenu()
    })

def reviews (request):
    return render (request, "website/reviews.html", {
        'menu_items': MenuItem.objects.all(),
    })

def contact (request):
    if request.user.username == 'kellysuperuser':
        messages = Message.objects.filter(receiver = request.user)
        sender_list = set()
        for message in messages:
            sender_list.add(message.sender.username)

        return render (request, "website/contactSuper.html",{
            "sender_list": sender_list
        })
    return render (request, "website/contact.html")

def cart (request):
    cart = request.user.cart
    total = cart.total_cost
    entries = cart.items.all()
    orders = Order.objects.filter(user = request.user, order_completed = False)
    return render (request, "website/cart.html", {
        "total": total,
        "entries": entries,
        "orders": orders
    })

def orders (request):
    orders = Order.objects.filter(order_completed = False)

    return render (request, "website/orders.html", {
        "orders": orders
    })

def login_view (request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login (request, user)
            return HttpResponseRedirect (reverse("index"))
        else:
            return render (request, "website/login.html", {
                "message": "Incorrect username and/or password."
            })

    else:
        return render (request, "website/login.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def register (request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        #check if passwords are the same
        password = request.POST["password"]
        confirmation =  request.POST['confirmation']

        if password != confirmation:
            return render (request, "website/register.html", {
                "message": "Passwords do not match."
            })
        else:
            #try to make new user
            try:
                user = User.objects.create_user(username,email,password) 
                user.save()
            except IntegrityError: 
                return render(request, "website/register.html", {
                    "message": "Username already taken."
                })
            user.cart = Cart()
            cart = user.cart
            cart.save()
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
    else:
        return render (request, "website/register.html")

def edit (request):
    if request.method ==  "POST":
        form = EditForm (request.POST, request.FILES)
        home = Home.objects.get(pk=1)
        if form.is_valid():
            if check_image ("slide_img1", form):
                home.slide_img1 = form.cleaned_data["slide_img1"]
            if check_image ("slide_img2", form):
                home.slide_img2 = form.cleaned_data["slide_img2"]
            if check_image ("slide_img3", form):
                home.slide_img3 = form.cleaned_data["slide_img3"]
            if check_image ("slide_img4", form):
                home.slide_img4 = form.cleaned_data["slide_img4"]
            if check_image ("slide_img5", form):
                home.slide_img5 = form.cleaned_data["slide_img5"]
            if check_image ("about_img", form):
                home.about_img = form.cleaned_data["about_img"]
            if check_image ("menu_img", form):
                home.menu_img = form.cleaned_data["menu_img"]
            home.save()

            return HttpResponseRedirect(reverse("index"))
        
    else:
        return render (request, "website/edit.html", {
            "form": EditForm(),
            "home": Home.objects.get(pk=1)
        })

def check_image (name, form):
    if form.cleaned_data[name] is not None:
        return True
    return False

@csrf_exempt
def add_review (request):
    print ("in add_review")

    if (request.method != 'POST'): 
        return JsonResponse({"error": "POST request required."}, status=400)

    data = json.loads(request.body)
    name = data.get("name", "")
    content = data.get ("content", "")
    product_bought = data.get("product_bought", "")
    stars = data.get("stars","")

    review = Review()
    review.user = User.objects.get(username = name)
    review.content = content
    review.product_bought = MenuItem.objects.get(name = product_bought)
    review.stars = stars
    review.save()
        
    return HttpResponse(status = 201)

def get_review (request):
    reviews = Review.objects.all()
    reviews = reviews.order_by("-timestamp").all()
    return JsonResponse([review.serialize() for review in reviews], safe = False)

def reviews_filtered(request, item):
    item = MenuItem.objects.get(name = item)
    reviews = Review.objects.filter(product_bought = item)
    return JsonResponse([review.serialize() for review in reviews], safe = False)

@csrf_exempt
def add_message(request):
    print("in add message")
    if (request.method != 'POST'): 
        return JsonResponse({"error": "POST request required."}, status=400)

    data = json.loads(request.body)
    sender = data.get("sender","")
    receiver = data.get("receiver", "")
    content = data.get("content", "")

    message = Message()
    message.sender = User.objects.get(username = sender)
    message.receiver = User.objects.get(username = receiver)
    message.content = content
    message.save()

    return HttpResponse (status = 201)

def get_messages (request, user):
    current = User.objects.get(username = user)
    messages_sent = Message.objects.filter(sender = current)
    messages_received = Message.objects.filter(receiver = current)
    messages = messages_sent | messages_received
    messages = messages.order_by("-timestamp").all().reverse()
    #print(messages[0])
    return JsonResponse([message.serialize() for message in messages], safe=False)

@csrf_exempt
def add_cart (request):
    cart = request.user.cart
    data = json.loads(request.body)
    item_name = data.get("item","")
    quantity = int(data.get("quantity", ""))
    item = MenuItem.objects.get(name = item_name)
    in_cart = False

    for entry in cart.items.all():
        if entry.menu_item == item:
            entry.quantity += quantity
            entry.item_total = entry.quantity * item.price
            entry.save()
            cart.total_cost += quantity * item.price
            in_cart = True
            break
    if in_cart == False:
        entry = CartEntry()
        entry.menu_item = item
        entry.quantity = quantity
        entry.item_total = entry.quantity * item.price
        entry.save()
        cart.items.add (entry)
        cart.total_cost += entry.item_total

    cart.save()
    
    return HttpResponse (status = 201)

@csrf_exempt
def delete_cart (request):
    data = json.loads(request.body)
    name = data.get("item","")
    item = MenuItem.objects.get(name = name)

    cart = request.user.cart
    entries = cart.items.all()
    for entry in entries:
        if entry.menu_item == item:
            cart.total_cost = cart.total_cost - entry.item_total
            entry.delete()
            cart.save()
            break

    return HttpResponse(status=204)

@csrf_exempt
def place_order (request):
    data = json.loads(request.body)
    cart = request.user.cart
    cart.order_placed = data.get("read","")

    if cart.order_placed == True:
        order = Order()
        order.user = cart.user
        order.save()
        for item in cart.items.all():
            order.items.add(item)
            #empty cart
        cart.items.clear()
        order.total_cost = cart.total_cost
        #clear cart
        cart.total_cost = 0
        cart.order_placed = False
        cart.save()
        order.save()

    else:
        return JsonResponse({"error": "Order is not placed"}, status=400)

    return HttpResponse(status=204)

@csrf_exempt
def order_completed (request):
    print ("order completed")
    data = json.loads(request.body)
    id = data.get("id","")
    order = Order.objects.get(pk = id)
    order.order_completed = data.get("completed", "")
    if order.order_completed == True:
        order.delete()

    return HttpResponse(status=204)

def get_unread(request):
    messages = Message.objects.filter(receiver = request.user)
    messages = messages.filter(read = False)

    return JsonResponse([message.serialize() for message in messages], safe = False)

def get_user_unread(request, name):
    user = User.objects.get(username = name)
    messages = Message.objects.filter(sender = user, read = False)

    return JsonResponse([message.serialize() for message in messages], safe = False)

@csrf_exempt
def read_messages(request):
    if request.method == "PUT":
        data = json.loads(request.body)
        sender = data.get ("sender", "")
        sender_user = User.objects.get(username = sender)
        receiver = data.get ("receiver", "")
        receiver_user = User.objects.get(username = receiver)

        messages = Message.objects.filter(sender = receiver_user, receiver = sender_user)
        for message in messages:
            message.read = True
            message.save()
        return HttpResponse(status = 204)

    # Email must be via GET or PUT
    else:
        return JsonResponse({
            "error": "GET or PUT request required."
        }, status=400)