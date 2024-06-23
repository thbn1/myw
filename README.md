### E-Commerce
 
## Used Frameworks and Methods:
- DB: PostgreSQL, Django ORM
- FW: Django
- Methods: Restful API, Custom Slugify, Custom Pagination, Custom infinite scroll, Web scraping and crawling (for database load), ajax frame listing, Authentication


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
