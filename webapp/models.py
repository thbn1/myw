from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.text import slugify 
from django.db.models import Avg
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
    star1=models.IntegerField(default=0)
    star2=models.IntegerField(default=0)
    star3=models.IntegerField(default=0)
    star4=models.IntegerField(default=0)
    star5=models.IntegerField(default=0)
    productratingcount=models.IntegerField(default=0)
    productrating=models.IntegerField(default=0)
    productcards=models.JSONField()
    
    def addstar(self,star):
       
        if star==5:
            self.star5+=1
        elif star==4:
            self.star4+=1

        elif star==3:
            self.star3+=1
         
        elif star==2:
            self.star2+=1
           
        elif star==1:
            self.star1+=1
        self.productratingcount=self.star1+self.star2+self.star3+self.star4+self.star5
        self.productrating= (round(((self.star1)+(self.star2*2)+(self.star3*3)+(self.star4*4)+(self.star5*5))*2/self.productratingcount,0))
        super(Product, self).save(update_fields=["productrating","star"+str(star),"productratingcount"])
        
 

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