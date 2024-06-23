from django.shortcuts import render

from django.http.response import HttpResponse

from django.views.generic import TemplateView
from django.shortcuts import render,redirect
from django.utils.safestring import mark_safe
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout

import random
from webapp.models import Product,Image,Review
from django.core.paginator import Paginator

from django.http import JsonResponse

from django.db.models import Avg

def image_upload_view(request):

    if request.method == 'POST':
            return HttpResponse("Yetkiniz yok")
            name=request.POST["name"]
            description=request.POST["description"].replace("\n","<br>")
            category=request.POST["category"] 
            price=request.POST["price"]
            try:
                pimg=request.FILES["photo"]
            except:
                pimg=""
            if name=="":
                formvalid="Ürün ismi gerekli"
                return render(request,"addproduct.html",{"form": formvalid})
            elif price=="":
                formvalid="Ürün fiyatı gerekli"
            elif description=="":
                formvalid="Ürün açıklaması gerekli"
            elif category=="":
                formvalid="Ürün kategorisi gerekli"
            elif pimg=="":
                formvalid="En az bir görsel gerekli"

            foo_instance = Product.objects.create(productname=name, productdesc=description,productprice=price, productcategory=category,productimage=pimg, productseller=request.user)

            
            dictfile={}
            
            for i in range(2,6):
                try:
                    image=request.FILES["images"+str(i)]


                    if image.size>3000000:
                        err="Boyutu 3MB'dan büyük dosya yüklediniz."
                        return render(request, 'addproduct.html', {'err': err})
                    dictfile["image"+str(i)]=image
                except:continue

            if len(dictfile)!=0:

                for i in dictfile:
                    Image.objects.create(image=dictfile[i], product_id=foo_instance.id)
 
            """
            try:
                image1=request.FILES["images1"]
                Image.objects.create(image=image1, product_id=foo_instance.id)
        
                for i in range(2,6):
                    try:
                        Image.objects.create(image=request.FILES["images"+str(i)], product_id=foo_instance.id)
                    except:
                        break
    
            except:
                return render(request, 'addproduct.html',{"err":"Ürün görseli eklenmedi"})

            """
            images = Image.objects.all()
            return render(request, 'addproduct.html', {'images': images})
 
    return render(request, 'addproduct.html')


def index(request):
    try:
        products2=Product.objects.filter()[0:60]
        products = random.sample(products2, 18)
        return render(request, 'index.html', {'products': products})

    except: 
        return render(request,"index.html")


def register(request):
    rdata={} 
    if request.method =="POST":
        
        username= request.POST["username"]
        password= request.POST["password"]
        password2= request.POST["password2"]
        email= request.POST["email"]
        if len(username)<5:

            rdata["error"]="kullanıcı adınız 5 haneden kısa"
        if len(password)<8:
            rdata["error"]="Şifreniz 8 haneden kısa"
        elif User.objects.filter(username=username).exists():
            rdata["error"]="Kullanıcı adı kullanımda."
        else:
            user =User.objects.create_user(username=username,email=email,password=password)
            user.save()
            user = authenticate(request,username = username,password = password)
            if user is not None:
                login(request,user)
                return redirect("/index")
    
    return render(request,"register.html",rdata)


def Login(request):
    rdata={}
    if request.method =="POST":
        
        username= request.POST["username"]
        
        password= request.POST["password"]
        if len(username)==0:
            rdata["error"]="Kullanıcı adı boş bırakılamaz."
        if len(password)==0:
            rdata["error"]="Şifre boş bırakılamaz."
        else:
            user = authenticate(request,username = username,password = password)
            if user is not None:
                login(request,user)
                return redirect("/index")
            else:
                rdata["error"]="Kullanıcı adı veya şifre yanlış."
    return render(request,"login.html",rdata)


def addproduct(request):

    if request.user.is_authenticated:
        return render(request,"addproduct.html")
    else:
        return render(request,"index.html")


def review(request):
    #page_obj=Product.objects.annotate(rating = Avg("review__rating")).order_by('-rating')
    #print(page_obj.get(id=53354).rating)
    if request.method == 'POST':

        pname=request.POST["name"]
        comment=request.POST["description"]
    
        cstar=int(request.POST["price"])

        prd=Product.objects.get(productname=pname)
        prd.addstar(cstar)
        foo_instance = Review.objects.create(comment=comment, rating=cstar, product=prd)
       
    return render(request,"addrev.html")


def testing(request):
    return render(request,"index.html")



    
def ajaxlist(request):
    if request.method == "GET":
        page_number = request.GET.get("cpage")
        searchtext=request.GET.get("searchtext")
        print(page_number)
        if page_number=="":
            page_number = 1
            
        else:
            try:
                page_number = int(page_number)
            except:
                page_number=1   
        offset=(page_number-1) * 16 # product per page

        page_obj=list(Product.objects.filter(productname__icontains=searchtext)[offset:offset+16].values("productname","productprice","productimage","productrating","productratingcount","slug"))

        #page_obj=Product.objects.annotate(rating = Avg("review__rating")).order_by('-rating')
        #page_obj=Product.objects.filter(id__gt=8910)[:16]
        #page_obj2=serializers.serialize("json",page_obj)


 
        # if nick_name found return not valid new friend

        return JsonResponse({"object":page_obj} )
        
    else:
        # if nick_name not found, then user can create a new friend.
        return JsonResponse({"valid":True}, status = 200)
    
    if page_number.isdigit():
        page_number = int(page_number)
    else: page_number = 1
    offset=(page_number-1) * 16 # product per page
    page_obj=Product.objects.filter(productname__icontains="fgjhrdg")[offset:offset+16]
    #page_obj=Product.objects.filter(id__gt=8910)[:16]
    return render(request,"listing.html",{"products": page_obj})


def listview(request):
    
    page_number = request.GET.get("page")

    if page_number=="":
        page_number = 1
        
    else:
        try:
            page_number = int(page_number)
        except:
            page_number=1
    offset=(page_number-1) * 16 # product per page
    page_obj=Product.objects.all()[offset:offset+16].values("productname","productprice","productimage","productrating","productratingcount","slug")

    return render(request,"listing.html",{"products": page_obj})


def listview2(request):
    page_number = request.GET.get("page")
    if page_number=="":
        page_number = 1  
    else:
        try:
            page_number = int(page_number)
        except:
            page_number=1
    offset=(page_number-1) * 16 # product per page
    page_obj=Product.objects.all()[offset:offset+16].values("productname","productprice","productimage","productrating","productratingcount","slug")
  
    return render(request,"listing.html",{"products": page_obj})


def listview_with_pagination(request):

    products=Product.objects.all()
   


    

    products=Product.objects.all().prefetch_related('image_set')
    #print(products2[1].image_set.all()[0].image)

    products = page_obj=Product.objects.filter(productcategory="Telefon",productname__contains="deneme").annotate(Avg("review__set")).values("productname","productprice","productimage","productrating","productratingcount")
    
    #        Prefetch("image_set",          
    #        queryset=Image.objects.select_related("product"))).get(pk=1)
    #print(product5.image_set.all().first().image)

    i=0

    
    
    #products3=Image.objects.values("product").annotate(id=Min("id"))
 

    p = Paginator(products, 16)
    page_number = request.GET.get("page")

    page_obj = p.get_page(page_number)
    return render(request,"listtest.html",{"products": page_obj})


def productpage(request,slug):

    
    product=Product.objects.get(slug=slug)
    productimage=product.image_set.all()
    print(productimage)
    rate=""
    if product.productrating!=0:
        rate=product.productrating
    return render(request,"product.html",{"product": product,"seller":product.productseller,"rate":rate,"ratecount":product.productratingcount,"cards":product.productcards})


def search(request):
    
    #products=Product.objects.filter(productname="")


    
    #products=Product.objects.raw("SELECT * FROM 'webapp_product' WHERE productname=''")
    

    #products2=Image.objects.select_related("product").all()
    #products=Product.objects.all().prefetch_related('image_set')
    #print(products2[1].image_set.all()[0].image) 

    #product5 = Product.objects.prefetch_related(
    #        Prefetch("image_set",          
    #        queryset=Image.objects.select_related("product"))).get(pk=1)
    #print(product5.image_set.all().first().image)


    
    
    #products3=Image.objects.values("product").annotate(id=Min("id"))
    searchtext=request.GET.get("q")
    page_number = request.GET.get("page")

    if page_number=="":
        page_number = 1
        
    else:
        try:
            page_number = int(page_number)
        except:
            page_number=1
    offset=(page_number-1) * 16 # product per page
    page_obj=Product.objects.filter(productname__icontains=searchtext)[offset:offset+16].values("productname","productprice","productimage","productrating","productratingcount","slug")
    #page_obj=Product.objects.annotate(rating = Avg("review__rating"))[:16].values("productname","productprice","productimage","rating")
    
    #page_obj=Product.objects.filter(id__gt=8910)[:16]
    return render(request,"listing.html",{"products": page_obj,"stext":searchtext})


def pdpage(request,str):
    if str=="installment":
        return HttpResponse("<div id='tabinstallment' style class='p-4'><div class='alert alert-danger'>Taksit bilgileri listelenecek</div></div>")
    if str=="return":
        
        return HttpResponse("<div id='tabreturn' style class='p-4'><div class='alert alert-warning'>İade bilgileri listelenecek</div></div>")
    if str=="seller":
        
        return HttpResponse("<div  id='tabseller' style class='p-4'><div class='alert alert-primary'>Farklı satıcılar listelenecek</div></div>")
    if str=="desc":
        
        return HttpResponse("<div id='tabdesc' class='p-4'><div class='alert alert-secondary'>Açıklama listelenecek</div></div>")
    if str=="comment":
        
        return HttpResponse("""<div id='tabcomment'>
    <div id="comrating" class="p-5 bg-white p-5">
        <div class="d-flex justify-content-between align-items-center"> 
            <div class="stardiv d-flex ">
                <div>
                    <svg style="fill:orange" id="str" height="1em" viewBox="0 0 576 512"><path d="M259.3 17.8L194 150.2 47.9 171.5c-26.2 3.8-36.7 36.1-17.7 54.6l105.7 103-25 145.5c-4.5 26.3 23.2 46 46.4 33.7L288 439.6l130.7 68.7c23.2 12.2 50.9-7.4 46.4-33.7l-25-145.5 105.7-103c19-18.5 8.5-50.8-17.7-54.6L382 150.2 316.7 17.8c-11.7-23.6-45.6-23.9-57.4 0z"/></svg>
                    <svg style="fill:orange" id="str" height="1em" viewBox="0 0 576 512"><path d="M259.3 17.8L194 150.2 47.9 171.5c-26.2 3.8-36.7 36.1-17.7 54.6l105.7 103-25 145.5c-4.5 26.3 23.2 46 46.4 33.7L288 439.6l130.7 68.7c23.2 12.2 50.9-7.4 46.4-33.7l-25-145.5 105.7-103c19-18.5 8.5-50.8-17.7-54.6L382 150.2 316.7 17.8c-11.7-23.6-45.6-23.9-57.4 0z"/></svg>
                    <svg style="fill:orange" id="str" height="1em" viewBox="0 0 576 512"><path d="M259.3 17.8L194 150.2 47.9 171.5c-26.2 3.8-36.7 36.1-17.7 54.6l105.7 103-25 145.5c-4.5 26.3 23.2 46 46.4 33.7L288 439.6l130.7 68.7c23.2 12.2 50.9-7.4 46.4-33.7l-25-145.5 105.7-103c19-18.5 8.5-50.8-17.7-54.6L382 150.2 316.7 17.8c-11.7-23.6-45.6-23.9-57.4 0z"/></svg>
                    <svg style="fill:orange" id="str" height="1em" viewBox="0 0 576 512"><path d="M259.3 17.8L194 150.2 47.9 171.5c-26.2 3.8-36.7 36.1-17.7 54.6l105.7 103-25 145.5c-4.5 26.3 23.2 46 46.4 33.7L288 439.6l130.7 68.7c23.2 12.2 50.9-7.4 46.4-33.7l-25-145.5 105.7-103c19-18.5 8.5-50.8-17.7-54.6L382 150.2 316.7 17.8c-11.7-23.6-45.6-23.9-57.4 0z"/></svg>
                    <svg style="fill:orange" id="str" height="1em" viewBox="0 0 576 512"><path d="M259.3 17.8L194 150.2 47.9 171.5c-26.2 3.8-36.7 36.1-17.7 54.6l105.7 103-25 145.5c-4.5 26.3 23.2 46 46.4 33.7L288 439.6l130.7 68.7c23.2 12.2 50.9-7.4 46.4-33.7l-25-145.5 105.7-103c19-18.5 8.5-50.8-17.7-54.6L382 150.2 316.7 17.8c-11.7-23.6-45.6-23.9-57.4 0z"/></svg>
                </div>
                <div class="ps-2 d-flex">
                    <span class="text-secondary" style="font-size:14px !important;font-weight:600 !important">&nbsp;4,6</span>
                </div>
            </div>
            <div class="py-auto bg-blue-300 d-flex" style="align-items:center !important">
                <label class="text-secondary m-auto" style="font-size:13px !important;font-weight:600 !important; vertical-align:bottom !important">554 Değerlendirme</label> 
            </div>
            <div>
                <div>
                    <select style="font-size:12px !important;font-weight:500 !important" class="form-select" aria-label="Default select example">
                        <option selected>minimum 1 yıldız</option>
                        <option selected>minimum 2 yıldız</option>
                        <option value="1">minimum 3 yıldız</option>
                        <option value="2">minimum 4 yıldız</option>
                        <option value="3">minimum 4,5 yıldız</option>
                    </select>
                </div>
            </div>
            <div>
                <div>
                    <select style="font-size:12px !important;font-weight:500 !important" class="form-select" aria-label="Default select example">
                        <option selected>Sıralama</option>
                        <option value="1">Yüksek puan üstte</option>
                        <option value="2">Düşük puan üstte</option>
                        <option value="3">En yeni üstte</option>
                    </select>
                </div>
            </div>
        </div>
        <hr class="mt-2 mb-4">
        <div>
        <div class="p-5 py-2">
            <div class="rounded-2 border border-1 p-3">
                <div class="d-flex align-items-center">
                    <div>
                        <svg style="fill:orange" id="str" height="0.9em" viewBox="0 0 576 512"><path d="M259.3 17.8L194 150.2 47.9 171.5c-26.2 3.8-36.7 36.1-17.7 54.6l105.7 103-25 145.5c-4.5 26.3 23.2 46 46.4 33.7L288 439.6l130.7 68.7c23.2 12.2 50.9-7.4 46.4-33.7l-25-145.5 105.7-103c19-18.5 8.5-50.8-17.7-54.6L382 150.2 316.7 17.8c-11.7-23.6-45.6-23.9-57.4 0z"/></svg>
                        <svg style="fill:orange" id="str" height="0.9em" viewBox="0 0 576 512"><path d="M259.3 17.8L194 150.2 47.9 171.5c-26.2 3.8-36.7 36.1-17.7 54.6l105.7 103-25 145.5c-4.5 26.3 23.2 46 46.4 33.7L288 439.6l130.7 68.7c23.2 12.2 50.9-7.4 46.4-33.7l-25-145.5 105.7-103c19-18.5 8.5-50.8-17.7-54.6L382 150.2 316.7 17.8c-11.7-23.6-45.6-23.9-57.4 0z"/></svg>
                        <svg style="fill:orange" id="str" height="0.9em" viewBox="0 0 576 512"><path d="M259.3 17.8L194 150.2 47.9 171.5c-26.2 3.8-36.7 36.1-17.7 54.6l105.7 103-25 145.5c-4.5 26.3 23.2 46 46.4 33.7L288 439.6l130.7 68.7c23.2 12.2 50.9-7.4 46.4-33.7l-25-145.5 105.7-103c19-18.5 8.5-50.8-17.7-54.6L382 150.2 316.7 17.8c-11.7-23.6-45.6-23.9-57.4 0z"/></svg>
                        <svg style="fill:orange" id="str" height="0.9em" viewBox="0 0 576 512"><path d="M259.3 17.8L194 150.2 47.9 171.5c-26.2 3.8-36.7 36.1-17.7 54.6l105.7 103-25 145.5c-4.5 26.3 23.2 46 46.4 33.7L288 439.6l130.7 68.7c23.2 12.2 50.9-7.4 46.4-33.7l-25-145.5 105.7-103c19-18.5 8.5-50.8-17.7-54.6L382 150.2 316.7 17.8c-11.7-23.6-45.6-23.9-57.4 0z"/></svg>
                        <svg style="fill:orange" id="str" height="0.9em" viewBox="0 0 576 512"><path d="M259.3 17.8L194 150.2 47.9 171.5c-26.2 3.8-36.7 36.1-17.7 54.6l105.7 103-25 145.5c-4.5 26.3 23.2 46 46.4 33.7L288 439.6l130.7 68.7c23.2 12.2 50.9-7.4 46.4-33.7l-25-145.5 105.7-103c19-18.5 8.5-50.8-17.7-54.6L382 150.2 316.7 17.8c-11.7-23.6-45.6-23.9-57.4 0z"/></svg>
                    </div>
                    <div>
                        <span class="text-secondary" style="font-size:13px !important;font-weight:400 !important">&nbsp;&nbsp;&nbsp;&nbsp;Ahmet E****</span>
                    </div>
                </div>
                <hr class="my-2">
                <div class="p-2">
                    <p style="font-size:12px !important">
                        10 yıllık MSI kullanıcısıyım ve eski bilgisayarımın hala yeni gibi olması ve hiç sorun yaratmaması sebebiyle 2. bilgisayarımı da MSI almaya karar verdim. Ürünü kullandıktan alacak olanlara fikir oluşturması açısından artılarını eksilerini yazıyorum. 
                    * Ürünün kasa kalitesi çok iyi. Özellikle tek elle ekranı açabiliyorsunuz.
                    * Ekranın ince olması sayesinde 17 inch olsa da biraz daha küçük geldi benim gözüme.
                    * Yeni tip ekranlarda IPS Glow olayı olduğunu biliyorudum. Ancak biraz ışık sızması var. Ama beni rahatsız edici düzeyde değil. Sonuçta sorunsuz ekran bulmak imkansız gibi bir şey. Telefonla fotoğrafını çektim ekledim. Bu görüntü sizi korkutmasın. Telefonla çekince çokmuş gibi gözüküyor.
                    * Oyun oynarken klavyenin ortasında ısınma oluyor. Fanı açınca az da olsa faydası oluyor. Ama fan süper üflüyor bu özellikteki bir bilgisayarın bu kadar ısınması normal gibi geliyor bana.
                    * Klavye ışıklandırması çok güzel. Tuşların kullanımı rahat.
                    * WIFI 6 olması modemden tam verim almamı sağladı.
                    * Pil oyun oynamadığımda çok uzun süre gidiyor. AI sayesinde optimize ediyor.
                    Kısacası tavsiye edeceğim bir bilgisayar.
                    </p>
                </div>
            </div>
        </div>
        <div class="p-5 py-2">
            <div class="rounded-2 border border-1 p-3">
                <div class="d-flex align-items-center">
                    <div>
                        <svg style="fill:orange" id="str" height="0.9em" viewBox="0 0 576 512"><path d="M259.3 17.8L194 150.2 47.9 171.5c-26.2 3.8-36.7 36.1-17.7 54.6l105.7 103-25 145.5c-4.5 26.3 23.2 46 46.4 33.7L288 439.6l130.7 68.7c23.2 12.2 50.9-7.4 46.4-33.7l-25-145.5 105.7-103c19-18.5 8.5-50.8-17.7-54.6L382 150.2 316.7 17.8c-11.7-23.6-45.6-23.9-57.4 0z"/></svg>
                        <svg style="fill:orange" id="str" height="0.9em" viewBox="0 0 576 512"><path d="M259.3 17.8L194 150.2 47.9 171.5c-26.2 3.8-36.7 36.1-17.7 54.6l105.7 103-25 145.5c-4.5 26.3 23.2 46 46.4 33.7L288 439.6l130.7 68.7c23.2 12.2 50.9-7.4 46.4-33.7l-25-145.5 105.7-103c19-18.5 8.5-50.8-17.7-54.6L382 150.2 316.7 17.8c-11.7-23.6-45.6-23.9-57.4 0z"/></svg>
                        <svg style="fill:orange" id="str" height="0.9em" viewBox="0 0 576 512"><path d="M259.3 17.8L194 150.2 47.9 171.5c-26.2 3.8-36.7 36.1-17.7 54.6l105.7 103-25 145.5c-4.5 26.3 23.2 46 46.4 33.7L288 439.6l130.7 68.7c23.2 12.2 50.9-7.4 46.4-33.7l-25-145.5 105.7-103c19-18.5 8.5-50.8-17.7-54.6L382 150.2 316.7 17.8c-11.7-23.6-45.6-23.9-57.4 0z"/></svg>
                        <svg style="fill:orange" id="str" height="0.9em" viewBox="0 0 576 512"><path d="M259.3 17.8L194 150.2 47.9 171.5c-26.2 3.8-36.7 36.1-17.7 54.6l105.7 103-25 145.5c-4.5 26.3 23.2 46 46.4 33.7L288 439.6l130.7 68.7c23.2 12.2 50.9-7.4 46.4-33.7l-25-145.5 105.7-103c19-18.5 8.5-50.8-17.7-54.6L382 150.2 316.7 17.8c-11.7-23.6-45.6-23.9-57.4 0z"/></svg>
                        <svg style="fill:orange" id="str" height="0.9em" viewBox="0 0 576 512"><path d="M259.3 17.8L194 150.2 47.9 171.5c-26.2 3.8-36.7 36.1-17.7 54.6l105.7 103-25 145.5c-4.5 26.3 23.2 46 46.4 33.7L288 439.6l130.7 68.7c23.2 12.2 50.9-7.4 46.4-33.7l-25-145.5 105.7-103c19-18.5 8.5-50.8-17.7-54.6L382 150.2 316.7 17.8c-11.7-23.6-45.6-23.9-57.4 0z"/></svg>
                    </div>
                    <div>
                        <span class="text-secondary" style="font-size:13px !important;font-weight:400 !important">&nbsp;&nbsp;&nbsp;&nbsp;Ahmet E****</span>
                    </div>
                </div>
                <hr class="my-2">
                <div class="p-2">
                    <p style="font-size:12px !important">
                        Ürün elime geleli 1 hafta oldu. Hızlı, akıcı ve profesyonel bir bilgisayar benim için. Oyun performansı açıkçası beklediğimden de iyiydi. Zaten işlemci, ekran kartı ve rami üst seviye. 17.3 inch ekran da gayet yeterli. Ben çok memnunum ve mutlulukla kullanıyorum.
                    </p>
                </div>
            </div>
        </div>
        <div class="p-5 py-2">
            <div class="rounded-2 border border-1 p-3">
                <div class="d-flex align-items-center">
                    <div>
                        <svg style="fill:orange" id="str" height="0.9em" viewBox="0 0 576 512"><path d="M259.3 17.8L194 150.2 47.9 171.5c-26.2 3.8-36.7 36.1-17.7 54.6l105.7 103-25 145.5c-4.5 26.3 23.2 46 46.4 33.7L288 439.6l130.7 68.7c23.2 12.2 50.9-7.4 46.4-33.7l-25-145.5 105.7-103c19-18.5 8.5-50.8-17.7-54.6L382 150.2 316.7 17.8c-11.7-23.6-45.6-23.9-57.4 0z"/></svg>
                        <svg style="fill:orange" id="str" height="0.9em" viewBox="0 0 576 512"><path d="M259.3 17.8L194 150.2 47.9 171.5c-26.2 3.8-36.7 36.1-17.7 54.6l105.7 103-25 145.5c-4.5 26.3 23.2 46 46.4 33.7L288 439.6l130.7 68.7c23.2 12.2 50.9-7.4 46.4-33.7l-25-145.5 105.7-103c19-18.5 8.5-50.8-17.7-54.6L382 150.2 316.7 17.8c-11.7-23.6-45.6-23.9-57.4 0z"/></svg>
                        <svg style="fill:orange" id="str" height="0.9em" viewBox="0 0 576 512"><path d="M259.3 17.8L194 150.2 47.9 171.5c-26.2 3.8-36.7 36.1-17.7 54.6l105.7 103-25 145.5c-4.5 26.3 23.2 46 46.4 33.7L288 439.6l130.7 68.7c23.2 12.2 50.9-7.4 46.4-33.7l-25-145.5 105.7-103c19-18.5 8.5-50.8-17.7-54.6L382 150.2 316.7 17.8c-11.7-23.6-45.6-23.9-57.4 0z"/></svg>
                        <svg style="fill:orange" id="str" height="0.9em" viewBox="0 0 576 512"><path d="M259.3 17.8L194 150.2 47.9 171.5c-26.2 3.8-36.7 36.1-17.7 54.6l105.7 103-25 145.5c-4.5 26.3 23.2 46 46.4 33.7L288 439.6l130.7 68.7c23.2 12.2 50.9-7.4 46.4-33.7l-25-145.5 105.7-103c19-18.5 8.5-50.8-17.7-54.6L382 150.2 316.7 17.8c-11.7-23.6-45.6-23.9-57.4 0z"/></svg>
                        <svg style="fill:orange" id="str" height="0.9em" viewBox="0 0 576 512"><path d="M259.3 17.8L194 150.2 47.9 171.5c-26.2 3.8-36.7 36.1-17.7 54.6l105.7 103-25 145.5c-4.5 26.3 23.2 46 46.4 33.7L288 439.6l130.7 68.7c23.2 12.2 50.9-7.4 46.4-33.7l-25-145.5 105.7-103c19-18.5 8.5-50.8-17.7-54.6L382 150.2 316.7 17.8c-11.7-23.6-45.6-23.9-57.4 0z"/></svg>
                    </div>
                    <div>
                        <span class="text-secondary" style="font-size:13px !important;font-weight:400 !important">&nbsp;&nbsp;&nbsp;&nbsp;Ahmet E****</span>
                    </div>
                </div>
                <hr class="my-2">
                <div class="p-2">
                    <p style="font-size:12px !important">
                        MSI dünyasını yeni keşfetmeye başlıyorum. Ürünü ön sipariş ile aldım ve hemen 10 Mart itibariyle yollandı. 

Ürün 17 inch olmasına rağmen oldukça zarif.
İşlemci ve genel donanıma denilebilecek 1 şey var;müthiş. Tek tavsiyem ssd 2 tb olabilirdi.

Ekran yenileme hızı ve ekran kartı performansı son derece iyi. 

Günlük kullanım yanı sıra; oyun ve grafik tasarım için kullanıyorum ve bu ağır oyun ve programları extreme edition moduna geçerek sorunsuz çalıştırıyor.

Kısacası teşekkürler MSI, teşekkürler Hepsiburada.
                    </p>
                </div>
            </div>
        </div>
    </div>
</div>""")
    


def loaddatabase(request):
    pass


def register_request(request):
    if request.user.is_authenticated:
        return redirect("/index")
    else:
        if request.method=="POST":
            username = request.POST['username']
        #   email = request.POST['email']
            firstname = request.POST['firstname']
            lastname = request.POST['lastname']
            #password = request.POST['password']
            #repassword = request.POST['repassword']
            password="test123"
            repassword="test123"
            if password == repassword:
                if len(firstname)<2:
                    return render(request,"login.html",{"error":"isim uygun değil"})
                if len(lastname)<2:
                    return render(request,"login.html",{"error":"soyisim uygun değil"})
        #       if len(email)<8 and "@" not in email:
        #           return render(request,"blog/register.html",{"error":"mail adresiniz geçersiz"})
                if len(username)<5:
                    return render(request,"login.html",{"error":"kullanıcı adınız 5 haneden kısa"})
                #if len(password)<8:
                #    return render(request,"blog/register.html",{"error":"Şifreniz 8 haneden kısa"})
                if User.objects.filter(username=username).exists():
                    return render(request,"login.html",{"error":"Kullanıcı adı kullanımda."})
                else:
                    #if User.objects.filter(email=email).exists():
                    #    return render(request,"blog/register.html",{"error":"email kullanımda."})
                    
                        user =User.objects.create_user(username=username,email="test@test.com",first_name=firstname,last_name=lastname,password=password)
                        user.save()
                        user = authenticate(request,username = username,password = "test123")
                        if user is not None:
                            login(request,user)
                        return redirect("/index")
                        
            else:
                return render(request,"login.html",{"error":"parola eşleşmiyor."})
        else:
            return render(request,'login.html')
def getproducts(request):
    pass

def login_request(request):
    if request.user.is_authenticated:
        return redirect("/index")
    else:
        print(str(request))
        print(type(request))
        if request.method =="POST":
            print("a")
            username = request.POST["username"]
            print("b")
            password = request.POST["password"]
            print("c")
            user = authenticate(request,username = username,password = "test123")
            print("d")
            if user is not None:
                print("zuhaha")
                login(request,user)
                return redirect("/index")
            else:
                print(request)
            
                return render(request,"login.html")
        else:
            return redirect(request,"login.html")
        
def logout_request(request):
    logout(request)
    return redirect("/index")