from django.contrib import admin
from core.models import Product, Catalog, Buyer
from django.utils.html import mark_safe
from django.forms import CheckboxSelectMultiple
from django.db import models


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'visibility']
    list_editable = ['visibility']
    list_filter = ['visibility']


@admin.register(Catalog)
class CatalogAdmin(admin.ModelAdmin):
    list_display = ['name', 'product_list']

    formfield_overrides = {
        models.ManyToManyField: {'widget': CheckboxSelectMultiple},
    }

    def product_list(self, obj):
        product_list_names = []
        for product_name in obj.products.prefetch_related('products').all().values_list('name', flat=True):
            product_list_names.append(product_name)
        return mark_safe("<br>".join(product_list_names))


@admin.register(Buyer)
class BuyerAdmin(admin.ModelAdmin):
    list_display = ['name', 'catalog', 'product_list']
    list_editable = ['catalog']
    list_filter = ['catalog']

    def product_list(self, obj):
        product_list_names = []
        for product_name in obj.products.all().values_list('name', flat=True):
            product_list_names.append(product_name)
        return mark_safe("<br>".join(product_list_names))

