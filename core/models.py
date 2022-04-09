from django.db import models


class Product(models.Model):

    class Visibility(models.TextChoices):
        DEFAULT = 'default'
        CATALOG_MEMBERS = 'catalog_members'

    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    visibility = models.CharField(max_length=15, choices=Visibility.choices, default=Visibility.DEFAULT)

    @property
    def to_dict(self):
        return {
            'name': self.name,
            'price': self.price,
            'visibility': self.visibility,
        }

    def __str__(self):
        return self.name


class Catalog(models.Model):
    name = models.CharField(max_length=255)
    products = models.ManyToManyField(Product)

    @property
    def to_dict(self):
        return {
            'name': self.name,
        }

    def __str__(self):
        return self.name


class Buyer(models.Model):
    name = models.CharField(max_length=255)
    catalog = models.ForeignKey(Catalog, null=True, blank=True, on_delete=models.CASCADE)

    @property
    def products(self):
        return Product.objects.filter(
            models.Q(
                pk__in=models.Subquery(
                    self.catalog.products.prefetch_related('products').all().values_list('pk', flat=True)
                )
            ) |
            models.Q(visibility=Product.Visibility.DEFAULT)
        )

    @property
    def to_dict(self):
        return {
            'name': self.name,
            'catalog': self.catalog.to_dict,
            'products': [product.to_dict for product in self.products]
        }

