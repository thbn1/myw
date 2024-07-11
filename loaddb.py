
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
from webapp.models import Product,Image,Review
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import Keys
from multiprocessing import Process
import psycopg2
products=[]
brands=["razer","monster","hp","asus","acer","dell"]


options = webdriver.ChromeOptions() 
#prefs = {"profile.managed_default_content_settings.images": 2}
#options.add_experimental_option("prefs", prefs)
options.add_experimental_option("excludeSwitches", ["enable-logging"])
options.add_argument("--no-sandbox")
options.add_argument("--disable-gpu")
options.add_argument("--headless")
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors')
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument('--window-size=1920,1080')
import urllib
options = webdriver.FirefoxOptions()
driver = webdriver.Firefox(options=options)
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
                    name=WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,'//h1[@id="product-name"]'))).text
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
                    