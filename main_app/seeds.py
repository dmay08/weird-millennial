from .models import Product

shirts = [
    ('ALOE! AZ', 29.99, 'https://i.imgur.com/4kKLl9G.png'),
    ('CACTUS! AZ', 29.99, 'https://i.imgur.com/L2envAo.png'),
    ('KOKOPELLI! AZ', 29.99, 'https://i.imgur.com/G9cGesD.png'),
    ('ALOE! CA', 29.99, 'https://i.imgur.com/pTX2oAk.png'),
    ('CACTUS! CA', 29.99, 'https://i.imgur.com/L2envAo.png'),
    ('KOKOPELLI! CA', 29.99, 'https://i.imgur.com/G9cGesD.png'),
]

sizes = ['XS', 'S', 'M', 'L', 'XL']

def create_products():
    Product.objects.all().delete()
    for shirt in shirts:
        for size in sizes:
            Product.objects.create(name=f"{shirt[0]} - {size}", price=shirt[1], image_url=shirt[2])