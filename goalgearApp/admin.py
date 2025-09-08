from django.contrib import admin
from .models import CustomUser,Product,Category,ProductImage,Cart,Order,OrderItem,PaymentMethod,OrderPayment,Contact

admin.site.register(CustomUser)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(ProductImage)
admin.site.register(Cart)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(PaymentMethod)
admin.site.register(OrderPayment)
admin.site.register(Contact)







# Register your models here.
