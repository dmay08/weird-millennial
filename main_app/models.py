from django.db import models
from django.contrib.auth.models import User 
from datetime import date

SIZES = (
    ('XS', 'Extra Small'),
    ('S', 'Small'),
    ('M', 'Medium'),
    ('L', 'Large'),
    ('XL', 'Extra Large'),
)

class Product(models.Model):
    name = models.CharField(max_length=100)
    image_url = models.CharField(max_length=200, default='https://i.imgur.com/4kKLl9G.png')
    price = models.FloatField()

    def __str__(self): 
        return self.name # this needs to reference a name above

class Order(models.Model):
    date = models.DateField(default=date.today())
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    paid = models.BooleanField(default=False)

    @classmethod
    def cart(cls, user): # cls refers to 'class Order'
        cart, created = cls.objects.get_or_create(
            paid=False,
            user=user # latter user has to match user param above
        )
        return cart #unpaid order for user

class LineItem(models.Model):
    quantity = models.IntegerField(default=1)
    size = models.CharField(
        max_length=2,
        choices=SIZES,
        default=SIZES[3][0]
    )
    # foreign key info: (also imported 'Product' above)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE )
