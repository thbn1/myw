
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'stageproject.settings')
django.setup()



from django.core.asgi import get_asgi_application
# Create your tests here.
from webapp.models import Product,Image,Review
print("HDMI".lower())
listt=["hdmi","ekrankartı","ramsistem","işletimsistemi","işlemcitipi","ssdkapasitesi","bellekhızı","işlemcinesli","ekranpaneltipi","ekranboyutu","ramtipi","renk","cihazağırlığı","type-c","webcam","usb","genişlik","derinlik","stok","garanti","ethernet","optik","emmc","parmak","kartokuyucu"]
products=Product.objects.all()
for i in products:
    dic1=i.productdesc 
    card1=i.productcards
    if len(i.productcards)<8:
        
        for value in dic1:
            if len(card1)==8:
                break
            cont=0
            for listelem in listt:
                
                if listelem in value.lower().replace(" ","").replace("(","").replace(")",""):
                    cont=1
            
            if cont==0:
                card1[value]=dic1[value]

        print(card1)

        i.productcards=card1
        i.save()

                    