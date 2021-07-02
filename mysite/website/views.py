from django.http.response import JsonResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.db import IntegrityError
from django import forms
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib.auth.decorators import login_required

from .models import User, Home,About, MenuItem, Review, Message, Cart, CartEntry,Order
# Create your views here.

def index (request):
    return render (request, "website/index.html", {
        "home": Home.objects.get(pk=1)
    })

def about (request):
    about = About.objects.get(pk=1)
    return render (request, "website/about.html",{
        "main_text": about.main_text,
        "side_text": about.side_text,
    })

def menu (request):
    user_auth = request.user.is_authenticated
    return render (request, "website/menu.html", {
        'menu_items': MenuItem.objects.all(),
        'user_auth': user_auth,
    })


def reviews (request):
    user_auth = request.user.is_authenticated
    return render (request, "website/reviews.html", {
        'menu_items': MenuItem.objects.all(),
        'user_auth': user_auth,
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
    user_auth = request.user.is_authenticated
    return render (request, "website/contact.html",{
        'user_auth': user_auth,
    })

def cart (request):
    if not request.user.is_authenticated:
        return render (request, "website/register.html")
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

@csrf_exempt
@login_required
def add_review (request):
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
@login_required
def add_message(request):
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

@login_required
def get_messages (request, user):
    current = User.objects.get(username = user)
    messages_sent = Message.objects.filter(sender = current)
    messages_received = Message.objects.filter(receiver = current)
    messages = messages_sent | messages_received
    messages = messages.order_by("-timestamp").all().reverse()

    return JsonResponse([message.serialize() for message in messages], safe=False)

@csrf_exempt
@login_required
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
@login_required
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
@login_required
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
    data = json.loads(request.body)
    id = data.get("id","")
    order = Order.objects.get(pk = id)
    order.order_completed = data.get("completed", "")
    if order.order_completed == True:
        order.delete()

    return HttpResponse(status=204)

@login_required
def get_unread(request):
    messages = Message.objects.filter(receiver = request.user)
    messages = messages.filter(read = False)

    return JsonResponse([message.serialize() for message in messages], safe = False)

@login_required
def get_user_unread(request, name):
    user = User.objects.get(username = name)
    messages = Message.objects.filter(sender = user, read = False)

    return JsonResponse([message.serialize() for message in messages], safe = False)

@csrf_exempt
@login_required
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
