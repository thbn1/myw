### E-Commerce
 In this project, I created a fully dynamic e-commerce site to improve my skills and put my learning into practice. I used the Django framework and applied various software techniques.
## Used Frameworks and Methods:
- DB: PostgreSQL, Django ORM
- FW: Django
- Methods: Restful API, Custom Slugify, Custom Pagination, Custom infinite scroll, Web scraping and crawling (for database load), ajax frame listing, Authentication


1. Restful API
I implemented RESTful APIs to facilitate secure and efficient management of products and user information through various CRUD (Create, Read, Update, Delete) operations.

2. Big Data
Utilizing big data techniques, I collected and analyzed user activities and sales data to optimize the website for better user experience and performance.

3. Web Scraping
I employed web scraping techniques to gather data from various e-commerce sites. This data was used for load database.

5. Custom Slug
I implemented custom slugs for SEO purposes, ensuring that product and category pages have readable and search engine-friendly URLs.

5. Custom Page Listing
I created custom lists of products and categories to enhance user engagement and facilitate easier navigation through the site.


## Some codes from the website

#I converted the product title to a URL unicode and combined it with the product ID to create the product page slug. This way, I generated a unique slug. When a product is added to the database, the slug will be created within the save method. line 44-48

some codes from models.py
```sh
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
        match star:
            case 5: self.star5+=1
            case 4: self.star4+=1
            case 3: self.star3+=1
            case 2: self.star2+=1
            case 1: self.star1+=1
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
```



#Using a RESTful API, I fetched the next products from the database via an AJAX GET method when the page was scrolled.

some codes from views.py
```sh
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
        return JsonResponse({"object":page_obj} )    
    else:
        return JsonResponse({"valid":True}, status = 200)
    
    if page_number.isdigit():
        page_number = int(page_number)
    else: page_number = 1
    offset=(page_number-1) * 16 # product per page
    page_obj=Product.objects.filter(productname__icontains="fgjhrdg")[offset:offset+16]
    #page_obj=Product.objects.filter(id__gt=8910)[:16]
    return render(request,"listing.html",{"products": page_obj})
```
some codes from ajaxlisting.js
```sh
$( document ).ready(function() {
  showstar();
});

function showstar(){
    z=0
    
    const elems=document.getElementsByClassName("ratings")
    var elemslength = elems.length;
    
    for (var elm = 0; elm < elemslength; elm++){
        var rating=parseFloat(elems[elm].getAttribute("id"))/2;
        
        var child=elems[elm].children;
        
        for (var childelm = 0; childelm < rating; childelm+=1){
            
            if (childelm==rating-0.5){
                child[childelm].querySelector('svg').insertAdjacentHTML("beforeend",'<path d="M288 0c-12.2 .1-23.3 7-28.6 18L195 150.3 51.4 171.5c-12 1.8-22 10.2-25.7 21.7s-.7 24.2 7.9 32.7L137.8 329 113.2 474.7c-2 12 3 24.2 12.9 31.3s23 8 33.8 2.3L288 439.8V0zM429.9 512c1.1 .1 2.1 .1 3.2 0h-3.2z" fill="orange"/>')
            }
            else{
                child[childelm].setAttribute("style", "fill:orange;");
            };
        };
     
    }
    Array.from(elems).forEach(b=>b.removeAttribute('class'));
    
};
var step = 1;
var loading = false;
function getDocumentHeight() {
    return Math.max(
        Math.max(document.body.scrollHeight, document.documentElement.scrollHeight),
        Math.max(document.body.offsetHeight, document.documentElement.offsetHeight),
        Math.max(document.body.clientHeight, document.documentElement.clientHeight)
    );
    }
$(window).on("scroll.once", function() {
    setTimeout(async () => {

            var docHeight = getDocumentHeight();
            if(loading === false){
    if ($(window).scrollTop() + window.innerHeight >= docHeight-5){

            loading = true;
            const url = new URL(window.location);
            page=url.searchParams.get("page");
            if (page==null){
                page=1;
            };
            let c =parseInt(page)+1;
            st=url.searchParams.get("q");
            $.ajax({
                
                type: 'GET',
                url: "ajaxlisting",
                data: {"cpage": c,"searchtext":st},
                success: function (response) {
    
    
    
                    for (var key in response) {
                        for (var i = 0; i < response[key].length; i++) {
                            var pname = response[key][i].productname;
                            var price = response[key][i].productprice;
                            var image = response[key][i].productimage;
                            var rating = response[key][i].productrating;
                            var ratingcount = response[key][i].productratingcount;
                            var slug = response[key][i].slug;
```


## Some screenshots from the website


![Screenshots](https://github.com/thbn1/E-Commerce/blob/main/forgithub/ss3.png)
![Screenshots](https://github.com/thbn1/E-Commerce/blob/main/forgithub/ss2.png)
![Screenshots](https://github.com/thbn1/E-Commerce/blob/main/forgithub/ss1.png)
![Screenshots](https://github.com/thbn1/E-Commerce/blob/main/forgithub/ss5.png)




##Selenium web scraping codes (for load database)
```ssh
for brand in brands:
    listlk=[]
    wpage=0
    notsameproduct=1
    print("************** "+brand+" **************")
    for i in range(1,6):
        productslink=[]
        if notsameproduct!=1:
            break
        wpage+=1
        link="https://www.hepsiburada.com/"+brand+"/laptop-notebook-dizustu-bilgisayarlar-c-98?sayfa="+str(i)
        driver.get(link)
        print("-----------"+link+"------------")
        while True:

            try:
                p_class= driver.find_elements(By.XPATH, '//li[@class="productListContent-zAP0Y5msy8OHn5z7T_K_"]')
                print(len(p_class))
                break
            except:
                time.sleep(2)
                pass


        if wpage==1:
            page1product1=driver.find_element(By.XPATH,'//ul/li/div/a[@href]').get_attribute('href')                                                      
        for product in p_class:
            
            try:
                url=product.find_element(By.XPATH,'.//a[@target="_blank"]')
                link2=url.get_attribute('href')  


                if wpage!=1 and link2==page1product1:
                    notsameproduct=0
                    print(page1product1)
                    break
                
                site="HepsiBurada"
            except Exception as error:
                print(error)
                continue
            if link2 in listlk:
                continue
            productslink.append([link2,brand])
            print("added link")
            listlk.append(link2)
        for productlink in productslink:
            print("add product")
            plink=productlink[0]
            driver.get(plink)
            time.sleep(1)
            h=0
            while True:
                h+=1
                try:
                    if h==3:
                        break
                    name=driver.find_element(By.XPATH,'//h1[@id="product-name"]').text
                    price=driver.find_element(By.XPATH,"""//span[@data-bind="markupText:'currentPriceBeforePoint'"]""").text.replace(".","")
                    desctable=driver.find_element(By.XPATH,'//table[@class="data-list tech-spec"]').get_attribute("innerHTML").replace("<a ","<span ").replace("</a>","</span>")
                    imgsrc=driver.find_element(By.XPATH,'//picture/source[@class="product-image"]').get_attribute("srcset").split(" ")[0]
                    
                    tablerows=driver.find_elements(By.XPATH,'//table[@class="data-list tech-spec"]/tbody/tr')
                    cards={}
                    desctable={}
                    for i in tablerows:
                        need2=i.find_element(By.TAG_NAME,"th").text
                        need=need2.lower().replace(" ","").replace("(","").replace(")","")
                        ram2=i.find_element(By.TAG_NAME,"td").text
                        desctable[need2]=ram2
                        if "ekrankartı"==need:  
                            ram=i.find_element(By.TAG_NAME,"td").text.strip().upper()
                            if ram!="BELIRTILMEMIŞ": 
                                cards["Ekran Kartı"]=ram
                        elif "ramsistem" in need:
                            ram=i.find_element(By.TAG_NAME,"td").text.upper().strip()
                            if ram!="BELIRTILMEMIŞ": 
                                cards["RAM"]=ram
                        elif "işletimsistemi" in need:
                            ram=i.find_element(By.TAG_NAME,"td").text.upper().strip()
                            if "Yok" in ram:
                                ram="Free Dos"
                            if ram!="BELIRTILMEMIŞ": 
                                cards["İşletim Sistemi"]=ram
                        elif "işlemcitipi" in need:
                            ram=i.find_element(By.TAG_NAME,"td").text.upper().strip()
                            if ram!="BELIRTILMEMIŞ": 
                                cards["İşlemci Tipi"]=ram
                        elif "ssdkapasitesi" in need:
                            ram=i.find_element(By.TAG_NAME,"td").text.upper().strip()
                            if ram!="BELIRTILMEMIŞ": 
                                cards["SSD"]=ram
                        elif "bellekhızı" in need:
                            ram=i.find_element(By.TAG_NAME,"td").text.upper().strip()
                            if ram!="BELIRTILMEMIŞ": 
                                cards["Ram Hızı"]=ram
                        elif "işlemcinesli" in need:
                            ram=i.find_element(By.TAG_NAME,"td").text.upper().strip()
                            if ram!="BELIRTILMEMIŞ": 
                                cards["İşlemci Nesli"]=ram
                    for i in tablerows:
                        need2=i.find_element(By.TAG_NAME,"th").text
                        
                        if len(cards)==8:
                            break
                        need=need2.lower().replace(" ","").replace("(","").replace(")","")
                        if "ekranpaneltipi" in need:
                            ram=i.find_element(By.TAG_NAME,"td").text.upper().strip()
                            if ram!="BELIRTILMEMIŞ": 
                                cards["Panel"]=ram
                        elif "ekranboyutu" in need:
                            ram=i.find_element(By.TAG_NAME,"td").text.upper().strip()
                            if ram!="BELIRTILMEMIŞ": 
                                cards["Ekran Boyutu"]=ram
                        elif "ramtipi" in need:
                            ram=i.find_element(By.TAG_NAME,"td").text.upper().strip()
                            if ram!="BELIRTILMEMIŞ": 
                                cards["RAM Tipi"]=ram
                        elif "renk" in need:
                            ram=i.find_element(By.TAG_NAME,"td").text.upper().strip()
                            if ram!="BELIRTILMEMIŞ": 
                                cards["Renk"]=ram
                        elif "cihazağırlığı" in need:
                            ram=i.find_element(By.TAG_NAME,"td").text.upper().strip()
                            if ram!="BELIRTILMEMIŞ": 
                                cards["Ağırlık"]=ram
                    try:
                        Product.objects.create(productname=name, productdesc=desctable,productprice=price, productcategory="Bilgisayar",productimage=imgsrc,productcards=cards, productseller_id=2)
                        print("------------success------------")
                    except:
                        pass
                    break

                except Exception as error:
                    print(error)
                    time.sleep(1)
                    
```


###How to Use the Project

#Clone this repository:
```sh
git clone https://github.com/thbn1/E-Commerce.git
```

#Install dependencies:
```sh
pip install -r requirements.txt
```

#Apply database migrations:
```sh
python manage.py migrate
```

#Start the development server:
```sh
python manage.py runserver
```
