from django.db import models

class Product(models.Model):
    image = models.URLField(max_length=200, unique=True)
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    installment = models.CharField(max_length=100)
    link = models.URLField(max_length=999)
    price_without_discount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    delivery_type = models.CharField(max_length=100)
    free_shipping = models.BooleanField(default=False)

    class Meta:
        db_table = 'product_offers'  # Nome da tabela no banco de dados

    def __str__(self):
        return self.name