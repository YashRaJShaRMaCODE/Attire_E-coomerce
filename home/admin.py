from django.contrib import admin
from home.models import (
    Contact,
    Feedback,
    Category,
    Product,
    Address,
    CartItem,
    Order,
    OrderItem,
)

admin.site.register(Contact)
admin.site.register(Feedback)
admin.site.register(Category)
admin.site.register(Address)
admin.site.register(CartItem)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "price", "stock", "is_active")
    list_filter = ("category", "is_active")
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "total_price", "status", "created_at")
    list_filter = ("status",)
    inlines = [OrderItemInline]
