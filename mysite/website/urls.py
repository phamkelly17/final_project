from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path ("", views.index, name = "index"),
    path ("login", views.login_view, name = "login"),
    path ("register", views.register, name = "register"),
    path ("logout", views.logout_view, name = "logout"),
    path ("edit", views.edit, name = "edit"),
    path ("about", views.about, name = "about"),
    path ('menu', views.menu, name = "menu"),
    path ('reviews', views.reviews, name = "reviews"),
    path ('contact', views.contact, name = "contact"),
    path ('editMenu', views.edit_menu, name = "edit_menu"),
    path ('cart', views.cart, name = "cart"),
    path ('orders', views.orders, name = "orders"),

    #API ROUTES
    path ('reviewsAPI', views.add_review, name = "add_review"),
    path('getReviews/all', views.get_review, name = "get_review"),
    path('getReviews/<str:item>', views.reviews_filtered, name = "reviews_filtered"),
    path('messages', views.add_message, name = "add_message"),
    path ('getMessages/<str:user>', views.get_messages, name = "get_messages"),
    path('addCart', views.add_cart, name = "add_cart"),
    path('deleteCart', views.delete_cart, name = "delete_cart"),
    path('placeOrder', views.place_order, name = "place_order"),
    path('completeOrder', views.order_completed, name = "order_completed"),
    path('unread', views.get_unread, name = "get_unread"),
    path('unread/<str:name>', views.get_user_unread, name = "get_user_unread"),
    path('readMessages',views.read_messages, name = "read_messages"),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)