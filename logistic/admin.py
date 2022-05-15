from django.contrib import admin
from .models import Stock, Product, StockProduct
# Register your models here.

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'description')


class StockProductInline(admin.TabularInline):
    model = StockProduct


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ('address', 'positions')
    inlines = [StockProductInline,]
