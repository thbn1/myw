
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'stageproject.settings')
django.setup()
from django.core.asgi import get_asgi_application
# Create your tests here.
from selenium import webdriver
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import re
from webapp.models import Product,Image,Review,User
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import Keys
from multiprocessing import Process
import psycopg2

#Product.objects.create(productname="DENEME1", productdesc="",productprice=123123, productcategory="Bilgisayar",productimage="",productcards={}, productseller_id=2)
urun=Product.objects.get(productname="DENEME1")
user=User.objects.get(id=1)
Review.objects.create(user=user,comment="asdf", rating=5, product=urun)