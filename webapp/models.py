from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.text import slugify 
from django.db.models import Avg, Sum

class Product(models.Model):
    id=models.AutoField(primary_key=True)
    productname = models.CharField(max_length=255,null=False,unique=True)
    productdesc=models.JSONField()
    productcategory=models.CharField(max_length=255)
    productprice=models.FloatField()
    productoldprice=models.FloatField(default=0)
    productseller= models.ForeignKey(User, on_delete=models.CASCADE)    
    slug = models.SlugField(max_length=255,null=True)
    productimage = models.CharField(max_length=255,null=True)  
    productratingcount=models.IntegerField(default=0) #review count
    productrating = models.DecimalField(max_digits=3, decimal_places=1,default=0.0)
    productcards=models.JSONField()
  
    def save(self, *args, **kwargs):
        super(Product, self).save(*args, **kwargs)
        if not self.slug:
            self.slug = slugify(self.productname) + "-" + str(self.id)
            self.save()



class Image(models.Model):
    image = models.ImageField(upload_to='images',null=True)
    product=models.ForeignKey(Product, on_delete=models.CASCADE,null=True)
    
    
    
class Review(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)    
    comment =models.TextField()
    product=models.ForeignKey(Product, on_delete=models.CASCADE)
    rating = models.IntegerField(
    default=1, validators=[MinValueValidator(1), MaxValueValidator(5)] 
    )  
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        product = self.product
        total_reviews = Review.objects.filter(product=product).count()
        total_rating = Review.objects.filter(product=product).aggregate(Sum('rating'))['rating__sum']
        product.productratingcount = total_reviews
        product.productrating = total_rating / total_reviews
        product.save()  
    def delete(self, *args, **kwargs):
        product = self.product
        super().delete(*args, **kwargs)
        total_reviews = Review.objects.filter(product=product).count()
        if total_reviews > 0:
            total_rating = Review.objects.filter(product=product).aggregate(Sum('rating'))['rating__sum']
            product.productratingcount = total_reviews
            product.productrating = total_rating / total_reviews
        else:
            product.productratingcount = 0
            product.productrating = 0
        product.save()