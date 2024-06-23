import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'stageproject.settings')
django.setup()
from django.core.asgi import get_asgi_application
import random
from webapp.models import Product,Image,Review

objects=Product.objects.all()

for obj in objects:
    for i in range(0,random.randint(0, 150)):
        star=random.randint(1,5)
        obj.addstar(star)
        foo_instance = Review.objects.create(comment="asdlkashjalsdfgd", rating=star, product=obj,user_id=1)