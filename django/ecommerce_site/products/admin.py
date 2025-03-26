from django.contrib import admin
from .models import Product, ProductFile

class ProductFileInline(admin.TabularInline):
    model = ProductFile
    extra = 1

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'is_active', 'created_at')
    inlines = [ProductFileInline]

admin.site.register(ProductFile)
