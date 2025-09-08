"""
URL configuration for GoalGear project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from goalgearApp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path("",views.home),
    # path("cards",views.cards),
    path("Login", views.login_fun),
    path('logout/', views.logout_fun, name='logout'),
    path("signup",views.signup_fun),
    path("product",views.product_fun, name='product'),
    path("view/<int:product_id>",views.product_view),
    path('category/<int:category_id>/', views.category_products, name='category_products'),
    path("bag/", views.bag, name='bag'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('update-cart/<int:item_id>/', views.update_cart_quantity, name='update_cart'),
    path("about",views.About_fun),
    path("contact",views.Contact_fun, name='contact'),
    path('checkout/address/', views.add_address, name='add_address'),
    path('place_order/<int:address_id>/', views.place_order, name='place_order'),
    path('order-status/', views.order_status_view, name='order_status'),
    path('pay/<int:order_id>/', views.demo_payment, name='demo_payment')
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
