from django.urls import path
from organicapp import views

urlpatterns = [
    path('',views.index),
    path('about',views.about),
    path('register',views.user_register),
    path('login',views.user_login),
    path('logout',views.user_logout),
    path('cart/<pid>',views.addtocart),
    path('pdetails/<pid>',views.product_details),
    path('viewcart',views.viewcart),
    path('changeqty/<pid>/<f>',views.changeqty),
    path('placeorder',views.placeorder),
    path('payment',views.makepayment),
    path('store',views.storedetails),
    path('verifyscreen/<rid>',views.verifyscreen),
    path('verifyotp/<rid>',views.verifyotp),
    path('products',views.product),
    path('sort/<sv>',views.sort),
    path('catfilter/<catv>',views.catfilter),
    path('pricerange',views.pricerange),
    path('pricefilter/<pv>',views.pricefilter),
    path('contact',views.contact),
]
